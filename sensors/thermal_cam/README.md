# MLX90640

Real-time posture detection based on thermal camera outputs

## Description

- `/Seeed_Python_MLX90640x` folder contains the starting codebase for the MLX90640 thermal camera
  - To set up mlx90640 thermal camera and its libraries, follow the RPI section of this guide: https://wiki.seeedstudio.com/Grove-Thermal-Imaging-Camera-IR-Array/
  - To test: `sudo ircamera I2C MLX90640`
- `/data_collection` folder contains the code to collect labeled sequences of data
- `Dataset Splitting.ipynb` performs a stratified train-validation-test split on the collected data, which can be used for the video action recognition classification task
- `/action_recognition` folder contains the Pytorch code for the CNN-LSTM model development for the video action recognition task
  - You can retrive the best saved weights from here for model prediction
