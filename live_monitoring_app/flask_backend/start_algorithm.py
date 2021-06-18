from utils import * 
from model import * 
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
# from sqlalchemy import create_engine

runAlgo = True

baseURL = "http://127.0.0.1:5000"
endpoint = "/patient-information"
apiURL = baseURL + endpoint

# engine = create_engine("mysql+pymysql://raspberry:password123^@localhost/post_monitoring_db")
# conn = engine.connect()

def updateFallRiskStatus(final_label):
    updated_label = {'fall_risk_status': final_label}
    requests.patch(apiURL, json = updated_label)

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


def startAlgo():
    global runAlgo
    runAlgo = True

    label = '0' 
    last_serial_readings = '0.0,0.0,0.0,0.0,0.0,0.0'

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

    while runAlgo:
          # get the first 10 frames
        frames = np.zeros((NUM_FRAMES, 96, 72))
        for i in range(NUM_FRAMES):
            frames[i] = get_frame(mlx, frame)
        
        initial_temp = np.percentile(frame, 30) + 1.5
        print('Initial temp: {}'.format(initial_temp))
                
        while True:
            # Thermal Camera sensor
            # replace the last 2 frames with the incoming frames and predict
            frames[:-2], frames[-2], frames[-1] = frames[2:], get_frame(mlx, frame), get_frame(mlx, frame)
            
            # get 95th percentile ambient temperature
            temp = np.percentile(frame, 95) 
            
            if initial_temp > temp:
                inaction = 0
                tam_count += 1
                sit, stand, bend, tampered = -20, -20, -20, -20 # set to low log-softmax scores
            else:
                inaction = -20
                arr = np.expand_dims(frames, axis=0)
                arr = torch.from_numpy(arr).float()

                # return the predicted log softmax scores
                output = model(arr)
                sit, stand, bend, tampered = output.squeeze().tolist()
            
            # Weight sensor & Vibration sensor 
            w_br, w_bl, w_fr, w_fl, v_b, v_t = last_serial_readings.split(',')

            posture_label, previous_state_w_b, previous_state_w_f = get_posture_label(sit, bend, stand, tampered, inaction, w_bl, w_br, w_fl, w_fr, previous_state_w_b, previous_state_w_f )
            if preemptive_label == 0:
                preemptive_label = get_preemptive_label(v_b, v_t)

            if tam_count > 30:
                final_label = "tam"
                updateFallRiskStatus(final_label) 
                return 
            
            final_label = get_alert(posture_label, preemptive_label)
            updateFallRiskStatus(final_label)
       
def stopAlgo():
    global runAlgo
    runAlgo = False
    print("algorithm stop called")
