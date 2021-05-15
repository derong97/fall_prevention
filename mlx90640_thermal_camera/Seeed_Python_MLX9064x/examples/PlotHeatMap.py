import seeed_mlx9064x
import time
import numpy as np
import matplotlib.pyplot as plt

#code only outputs first temperature reading + matplotlib plot


CHIP_TYPE = 'MLX90640'

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
        frame = np.array(frame)
        frame_formatted = np.reshape(frame,(24, 32)) 
        plt.imshow(frame_formatted, cmap='hot', interpolation='nearest')
        plt.show()
        end = time.time()
        print("The time: %f"%(end - start))
if __name__  == '__main__':
    main()

