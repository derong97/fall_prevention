import seeed_mlx9064x
import time
import numpy as np
import matplotlib.pyplot as plt


CHIP_TYPE = 'MLX90640'

def format_frame(frame):
    formatted_frame = np.zeros((24,32))
    column = 0
    row = 0 #24 rows total 
    for i in frame: #i is the temperature 
        if column < 31: #still along the same row 
            formatted_frame[row, column] = i
            column += 1 
        elif column == 31: #reset row after adding entry
            formatted_frame[row, column] = i
            row += 1
            column = 0

    return formatted_frame

def main():
    if CHIP_TYPE == 'MLX90641':
        mlx = seeed_mlx9064x.grove_mxl90641()
        frame = [0] * 192
    elif CHIP_TYPE == 'MLX90640':
        mlx = seeed_mlx9064x.grove_mxl90640()
        frame = [0] * 768       
    time.sleep(1) 
    while True:
        start = time.time()
        try:
            mlx.getFrame(frame)
        except ValueError:
            continue
        print(frame)
        frame_formatted = format_frame(frame)
        plt.imshow(frame_formatted, cmap='hot', interpolation='nearest')
        plt.show()
        end = time.time()
        print("The time: %f"%(end - start))
if __name__  == '__main__':
    main()

