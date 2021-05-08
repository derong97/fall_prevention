import seeed_mlx9064x
import time
import numpy as np
import os
import sys

def take_n_frames(mlx, frame, count=10):

    for i in range(count):
        try:
            mlx.getFrame(frame)
        except ValueError:
            raise ValueError
        frame = np.array(frame)
        if i == 0:
            frames = frame
        else:
            frames = np.vstack((frames, frame))
        print("frame", (i + 1), " captured")
        
    return frames 
   
if __name__  == '__main__':
    # Parsing the argument
    if len(sys.argv) < 2:
        print('You need to specify the path to be saved. For example: python collect_data.py posture_data/sit')
        sys.exit()
        
    root_dir = sys.argv[1]
    save_index = len(os.listdir(root_dir))
    action = os.path.basename(os.path.normpath(root_dir))
    
    # MLX90640
    mlx = seeed_mlx9064x.grove_mxl90640()
    frame = [0] * 768
    mlx.refresh_rate = seeed_mlx9064x.RefreshRate.REFRESH_8_HZ
    
    while True:
        try:
            frames = take_n_frames(mlx, frame, 10)
            save_filepath = root_dir + "/{}_".format(action) + str(save_index+1)
            np.save(save_filepath, frames)
            print(save_filepath, "saved")
            save_index += 1

        except KeyboardInterrupt:
            break
