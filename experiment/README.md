# Installation Guide on Raspberry Pi 4B

1. To set up mlx90640 thermal camera and its libraries, follow the RPI section of this guide: https://wiki.seeedstudio.com/Grove-Thermal-Imaging-Camera-IR-Array/
2. To install torch libraries, follow this guide: https://medium.com/analytics-vidhya/quick-setup-instructions-for-installing-pytorch-and-fastai-on-raspberry-pi-4-5ffbe45e0ae3
3. Run this command to ensure that all other requirements are installed: `pip3 install -r requirements.txt`
4. To use CV2 library, run this command: `sudo apt-get install libatlas-base-dev` (required for shared object libcblas.so.3 to work)

# Run the code

1. `python3 experiment.py`: collects real-time sensor outputs from thermal camera, weight sensors and vibration sensors along with user-controlled true labels in `data.csv`
2. The data format is as follows: `timestamp, expt_no, sit, stand, bend, tampered, inaction, w_br, w_bl, w_fr, w_fl, v_b, v_t, label`

Refer to `/rule-based_algo` folder for the analysis.
