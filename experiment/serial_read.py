#!/usr/bin/env python3
import serial
import csv
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii', errors='replace').rstrip()
            print(line)