from model import *
import seeed_mlx9064x
import numpy as np
import cv2

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

def predict(model, data, classes):
    """
    Predict the class label of the video
    """
    output = model(data)
    pred = output.argmax(dim=1, keepdim=True).item()
    prediction = classes[pred]
    return prediction

if __name__  == '__main__':
    # User defined variables
    MODEL_PATH = 'custom.pt'
    DEVICE = torch.device("cpu")
    NUM_FRAMES = 10
    CLASSES = {0: 'sit', 1: 'stand', 2: 'bend', 3: 'inaction', 4: 'tampered'}
    
    # load model
    model = CNN_LSTM().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    
    model.eval()
    
    print("Starting livestream...")
    
    # MLX90640
    mlx = seeed_mlx9064x.grove_mxl90640()
    frame = [0] * 768
    mlx.refresh_rate = seeed_mlx9064x.RefreshRate.REFRESH_8_HZ
    
    # get the first 10 frames
    frames = np.zeros((NUM_FRAMES, 96, 72))
    for i in range(NUM_FRAMES):
        frames[i] = get_frame(mlx, frame)
    
    while True:
        try:
            # replace the last frame with the incoming frame and predict
            frames[:-1], frames[-1] = frames[1:], get_frame(mlx, frame)
            arr = np.expand_dims(frames, axis=0)
            arr = torch.from_numpy(arr).float()
            print(predict(model, arr, CLASSES))

        except KeyboardInterrupt:
            break
