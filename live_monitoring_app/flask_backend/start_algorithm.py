from utils import * 
from model import *
import data
from flask import jsonify
import requests
import seeed_mlx9064x
from threading import Thread
import serial
import csv 
from pathlib import Path
import numpy as np
import cv2
import os
import sys
import time 
from sqlalchemy import create_engine
from datetime import datetime, timedelta

runAlgo= True 

baseURL = "http://127.0.0.1:5000"
endpoint = "/patient-information"
apiURL = baseURL + endpoint

sql_engine = create_engine("mysql+pymysql://raspberry:password@10.21.147.2/post_monitoring_db")
sql_conn = sql_engine.connect()


def get_frame(mlx, frame): 
    """
    Get 1 frame from MLX90640 camera
    """
    try:
        mlx.getFrame(frame)
    except ValueError:
        raise ValueError
    frame = np.array(frame).astype('float')
    frame = frame.reshape((24,32))
    frame = cv2.resize(frame, (72,96))
    
    return frame / 255

def receiving(ser):
    """
    Receives continuous byte data from Arduino
    """
    global last_serial_readings

    while True:
        if ser.in_waiting > 0: 
            last_serial_readings = ser.readline().decode('ascii', errors='replace').rstrip()


def startAlgo(bed_number, patient_accompanied):
#     global BED_NUMBER, TIME_STARTED, TIME_STOPPED, HFR_COUNT, PATIENT_ACCOMPANIED, FALL_RISK_STATUS, HFR_COUNT
        
    data.BED_NUMBER = bed_number
    data.TIME_STARTED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.TIME_STOPPED = 0
    data.HFR_COUNT = 0
    data.PATIENT_ACCOMPANIED = patient_accompanied 
    data.FALL_RISK_STATUS = "low"
    data.HFR_COUNT = 0
    
    print("start algo called")
    
    global runAlgo
    runAlgo = True

    label = '0' 
    last_serial_readings = '0.0,0.0,0.0,0.0,0,0'

    previous_state_w_b = 0
    previous_state_w_f = 0 
    posture_label = 0
    preemptive_label = 0

    tam_count = 0 

     ######################################
    ######      THERMAL CAMERA     #######
    ######################################
    
    MODEL_PATH = 'custom.pt'
    DEVICE = torch.device("cpu")
    NUM_FRAMES = 5
    
    # load model
    model = CNN_LSTM().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    
    model.eval()
    
    # MLX90640
    mlx = seeed_mlx9064x.grove_mxl90640()
    frame = [0] * 768
    mlx.refresh_rate = seeed_mlx9064x.RefreshRate.REFRESH_8_HZ
    
    ######################################
    ######       WEIGHT SENSOR     #######
    ######################################
    
    # Serial Output from Arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    
    
    t2 = Thread(target=receiving, args=(ser,))
    t2.daemon = True
    t2.start()
    
    NUM_FRAMES = 5
    # get the first 10 frames
    frames = np.zeros((NUM_FRAMES, 96, 72))
    for i in range(NUM_FRAMES):
        frames[i] = get_frame(mlx, frame)
    
    initial_temp = np.percentile(frame, 30) + 1.5
    print('Initial temp: {}'.format(initial_temp))
            
    while runAlgo:
        # Thermal Camera sensor
        # replace the last 2 frames with the incoming frames and predict
        frames[:-2], frames[-2], frames[-1] = frames[2:], get_frame(mlx, frame), get_frame(mlx, frame)
        
        # get 95th percentile ambient temperature
        temp = np.percentile(frame, 95) 
        
        if initial_temp > temp:
            inaction = 0
            sit, stand, bend, tampered = -20, -20, -20, -20 # set to low log-softmax scores
            #print("TC: inaction")
        
        else:
            inaction = -20
            arr = np.expand_dims(frames, axis=0)
            arr = torch.from_numpy(arr).float()

            # return the predicted log softmax scores
            output = model(arr)
            sit, stand, bend, tampered = output.squeeze().tolist()
            
            pred = output.argmax(dim=1, keepdim=True).item()
            classes = ['sit', 'stand', 'bend', 'tampered']
            #print("TC: {}".format(classes[pred]))
        
            if classes[pred] == "tampered":
                tam_count += 1
                print("tampered")
                
                if tam_count > 30:
                    final_label = "tam"
                    data.FALL_RISK_STATUS = final_label
                    return
                
                continue
        
        # Weight sensor & Vibration sensor 
        w_br, w_bl, w_fr, w_fl, v_b, v_t = last_serial_readings.split(',')

        posture_label, previous_state_w_b, previous_state_w_f = get_posture_label(sit, bend, stand, tampered, inaction, 
                                                                                  float(w_bl), float(w_br), float(w_fl), float(w_fr),
                                                                                  previous_state_w_b, previous_state_w_f)
        if preemptive_label == 0:
            preemptive_label = get_preemptive_label(int(v_b), int(v_t))
        
        
        final_label = get_alert(posture_label, preemptive_label)
        data.FALL_RISK_STATUS = final_label
        
        if final_label == "high" or final_label == "fall":
            data.HFR_COUNT += 1 
        
        print("start algo", final_label, data.FALL_RISK_STATUS)
       
def stopAlgo():
    global runAlgo
    runAlgo = False
    
    data.TIME_STOPPED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    if data.HFR_COUNT > 10:
        hfr_boolean = 1
    else:
        hfr_boolean = 0
    
    new_log = sql_conn.execute("INSERT INTO  `post_monitoring_db`.`current_patient_logs` (bed_number,timestamp_start,timestamp_end,accompanied,hfr_count) \
              VALUES ('{}','{}','{}','{}','{}');".format(data.BED_NUMBER, data.TIME_STARTED,
                                             data.TIME_STOPPED, data.PATIENT_ACCOMPANIED,
                                             hfr_boolean))
    #add to post monitoring logs 
    #new_log = sql_conn.execute("INSERT INTO  `post_monitoring_db`.`current_patient_logs` (bed_number,timestamp_start,timestamp_end,accompanied,hfr_count) \
     #             VALUES ({},{},{},{},{})".format(bed_number, timestamp_start, timestamp_end, accompanied, hfr_count))
    print("algorithm stop called")
