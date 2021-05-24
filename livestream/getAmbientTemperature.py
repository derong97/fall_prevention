import numpy as np
import seeed_mlx9064x

mlx = seeed_mlx9064x.grove_mxl90640()
frame =  [0] * 768

while True:
    mlx.getFrame(frame)
    temp = np.percentile(frame,90)

    print(temp)