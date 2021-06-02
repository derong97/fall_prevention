from threading import Thread
from model import *
import seeed_mlx9064x
import numpy as np
import cv2
import serial
import csv 
import time
from pathlib import Path
import sys
import os

label = '0' 
last_serial_readings = '0.0,0.0,0.0,0.0,0.0,0.0'

def scanning():
    """
    Continuously scans for user input``
    """
    global label
    
    label2action = {'0': 'sit', '1': 'standing', '2': 'stand', '3': 'fell'}
    while True:
        user_input = input()
        if user_input in label2action.keys():
            label = user_input
            print("Changed label to {} -> {}".format(label, label2action[user_input]))
        else:
            print("Invalid input")

def receiving(ser):
    """
    Receives continuous byte data from Arduino
    """
    global last_serial_readings

    while True:
        if ser.in_waiting > 0: 
            last_serial_readings = ser.readline().decode('ascii', errors='replace').rstrip()

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

if __name__  == '__main__':
    
    print("Starting livestream...")
    
    # Continuously scans for user input
    t1 = Thread(target=scanning)
    t1.daemon = True
    t1.start()
        
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
    #ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    #ser.flush()
    
    #t2 = Thread(target=receiving, args=(ser,))
    #t2.daemon = True
    #t2.start()
    
    
    ######################################
    ######      DATA COLLECTION    #######
    ######################################
    
    FILENAME = 'data.csv'
    Path(FILENAME).touch(exist_ok=True)
    
    with open(FILENAME, "r+", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        
        if os.stat(FILENAME).st_size == 0:
            headers = ['timestamp', 'expt_no', 'sit_score', 'stand_score', 'bend_score', 'tampered_score', 'inaction_score', 'w_bl', 'w_br', 'w_fl', 'w_fr', 'v_bidet', 'v_tissue', 'label']
            writer.writerow(headers)
            expt_no = 0
        else:
            last_line = csv_file.readlines()[-1].split(',')
            expt_no = int(last_line[1]) + 1
        
        print("Experiment number: {}".format(expt_no))
        
        # get the first 10 frames
        frames = np.zeros((NUM_FRAMES, 96, 72))
        for i in range(NUM_FRAMES):
            frames[i] = get_frame(mlx, frame)
        
        initial_temp = np.percentile(frame, 50) + 2
        print('Initial temp: {}'.format(initial_temp))
                
        while True:
            try:
                # Thermal Camera sensor
                # replace the last 2 frames with the incoming frames and predict
                frames[:-2], frames[-2], frames[-1] = frames[2:], get_frame(mlx, frame), get_frame(mlx, frame)
                
                # get 95th percentile ambient temperature
                temp = np.percentile(frame, 95) 
                
                if initial_temp > temp:
                    inaction = 0
                    sit, stand, bend, tampered = -20, -20, -20, -20 # set to low log-softmax scores
                    #print("inaction")
                else:
                    inaction = -20
                    arr = np.expand_dims(frames, axis=0)
                    arr = torch.from_numpy(arr).float()

                    # return the predicted log softmax scores
                    output = model(arr)
                    sit, stand, bend, tampered = output.squeeze().tolist()
                
                    #pred = output.argmax(dim=1, keepdim=True).item()
                    #classes = ['sit','stand','bend','tampered']
                    #print(classes[pred])

                # Weight sensor
                w_br, w_bl, w_fr, w_fl, v_b, v_t = last_serial_readings.split(',')
            
                timestamp = time.strftime('%d-%m-%Y %H:%M:%S')
                new_entry = [timestamp, expt_no, sit, stand, bend, tampered, inaction, w_br, w_bl, w_fr, w_fl, v_b, v_t, label]
                writer.writerow(new_entry)
                print(new_entry)
                
            except KeyboardInterrupt:
                csv_file.close()
                sys.exit()
