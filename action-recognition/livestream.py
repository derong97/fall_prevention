from model import *
import numpy as np
import cv2

def get_frame():
    """
    TODO: Get 1 frame from MLX90640 camera
    Currently, it's using fake data
    """
    frame = np.random.rand(768) * 255
    frame = frame.reshape(24,32)
    frame = cv2.resize(frame, (72,96))
    return np.array(frame).astype('float') / 255

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
    MODEL_PATH = 'save_weights/custom.pt'
    ARCH_TYPE = 'custom'
    DEVICE = torch.device("cpu")
    NUM_FRAMES = 10
    CLASSES = {0: 'sit',
               1: 'stand',
               2: 'tilt'}
    
    # load model
    model = CNN_LSTM(ARCH_TYPE, DEVICE).to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH))
    
    model.eval()
    
    print("Starting livestream...")
    
    # get the first 10 frames
    frames = np.zeros((NUM_FRAMES, 96, 72))
    for i in range(NUM_FRAMES):
        frames[i] = get_frame()
    
    while True:
        try:
            # replace the last frame with the incoming frame and predict
            frames[:-1], frames[-1] = frames[1:], get_frame()
            arr = np.expand_dims(frames, axis=0)
            arr = torch.from_numpy(arr).float()
            print(predict(model, arr, CLASSES))

        except KeyboardInterrupt:
            break
