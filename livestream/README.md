# Installation Guide on Raspberry Pi 4B
1. To set up mlx90640 thermal camera and its libraries, follow the RPI section of this guide: https://wiki.seeedstudio.com/Grove-Thermal-Imaging-Camera-IR-Array/
2. To install torch libraries, follow this guide: https://medium.com/analytics-vidhya/quick-setup-instructions-for-installing-pytorch-and-fastai-on-raspberry-pi-4-5ffbe45e0ae3
3. Run this command to ensure that all requirements are installed: `pip3 install -r requirements.txt`
4. To use CV2 library, run this command: `sudo apt-get install libatlas-base-dev` (required for shared object libcblas.so.3 to work)