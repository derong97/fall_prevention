from threading import Thread
from model import *
import seeed_mlx9064x
import numpy as np
import cv2
import serial
import csv 
import time
import sys

label = '0' 
last_weight_readings = '0.0,0.0,0.0,0.0'

def scanning():
    """
    Continuously scans for user input
    """
    global label
    
    label2action = {'0': 'sit', '1': 'stand', '2': 'fell'}
    while True:
        user_input = input()
        if user_input in ['0','1','2']:
            label = user_input
            print("Changed label to {} -> {}".format(label, label2action[user_input]))

def receiving(ser):
    """
    Receives continuous byte data from Arduino
    """
    global last_weight_readings

    while True:
        if ser.in_waiting > 0: 
            last_weight_readings = ser.readline().decode('utf-8').rstrip()
            
def get_frame(mlx, frame): 
    """
    Get 1 frame from MLX90640 camera
    """
    try:
        mlx.getFrame(frame)
    except ValueError:
        raise ValueError
    frame = np.array(frame).astype('float') / 255
    frame = frame.reshape(24,32)
    frame = cv2.resize(frame, (72,96))
    return frame

if __name__  == '__main__':
    # Parsing the argument
    if len(sys.argv) < 2:
        print('You need to specify the experiment number')
        sys.exit()
    
    exp_no = sys.argv[1]
    
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
    NUM_FRAMES = 10
    
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
    
    with open("data.csv", "a", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        
        if csv_file.tell() == 0:
            headers = ['timestamp', 'exp_no', 'sit_score', 'stand_score', 'bend_score', 'inaction_score', 'tampered_score', 'w1_voltage', 'w2_voltage', 'w3_voltage', 'w4_voltage', 'label']
            writer.writerow(headers)
        
        # get the first 10 frames
        frames = np.zeros((NUM_FRAMES, 96, 72))
        for i in range(NUM_FRAMES):
            frames[i] = get_frame(mlx, frame)
            
        while True:
            try:
                # Thermal Camera sensor
                # replace the last frame with the incoming frame and predict
                frames[:-1], frames[-1] = frames[1:], get_frame(mlx, frame)
                arr = np.expand_dims(frames, axis=0)
                arr = torch.from_numpy(arr).float()
                
                # return the predicted log softmax scores
                output = model(arr) 
                sit, stand, bend, inaction, tampered = output.squeeze().tolist()

                # Weight sensor
                w1, w2, w3, w4 = last_weight_readings.split(',')
            
                timestamp = time.strftime('%d-%m-%Y %H:%M:%S')
                new_entry = [timestamp, exp_no, sit, stand, bend, inaction, tampered, w1, w2, w3, w4, label]
                writer.writerow(new_entry)
                print(new_entry)
                
            except KeyboardInterrupt:
                sys.exit()
