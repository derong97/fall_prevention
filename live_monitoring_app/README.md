# Live Monitoring App

The live monitoring app is a way for the nurses to communicate with the rest of the system. 

## 1. Home Screen
![alt text](https://github.com/derong97/fall_prevention/tree/main/live_monitoring_app/images/home_screen.png)

## 2. Enter bed number screen
![alt text](https://github.com/derong97/fall_prevention/tree/main/live_monitoring_app/images/enter_bed_number.png)

## 3. Notification Screen
No Action Needed notification 
![alt text](https://github.com/derong97/fall_prevention/tree/main/live_monitoring_app/images/no_action_needed.png)

Get Ready notification 
![alt text](https://github.com/derong97/fall_prevention/tree/main/live_monitoring_app/images/get_ready.png)

Come Now notification 
![alt text](https://github.com/derong97/fall_prevention/tree/main/live_monitoring_app/images/come_now.png)

Fall notification
![alt text](https://github.com/derong97/fall_prevention/tree/main/live_monitoring_app/images/fall.png)

# Installation Guide on Raspberry Pi 4B

Make sure you are in the live_monitoring_app folder before completing this guide. 
`cd posture-detection/live_monitoring_app`

## Installing backend dependencies 
1. Navigate to the backend folder `cd flask_backend`
2. To set up mlx90640 thermal camera and its libraries, follow the RPI section of this guide: https://wiki.seeedstudio.com/Grove-Thermal-Imaging-Camera-IR-Array/
3. To install torch libraries, follow this guide: https://medium.com/analytics-vidhya/quick-setup-instructions-for-installing-pytorch-and-fastai-on-raspberry-pi-4-5ffbe45e0ae3
4. Run this command to ensure that all other requirements are installed: `pip3 install -r requirements.txt`
5. To use CV2 library, run this command: `sudo apt-get install libatlas-base-dev` (required for shared object libcblas.so.3 to work)
6. Create a `.env` file. Copy and paste the required environment variables from env_template, and insert the details of the private SQL database into that file. 

## Installing frontend dependencies 
1. Navigate to the frontend folder `cd live_monitoring_frontend`
2. Install frontend dependencies `yarn install` 
3. Once all the hardware has been connected, you can build and launch the app using `./runApp.sh`

