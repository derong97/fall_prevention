import matplotlib.pyplot as plt
import torch.nn as nn
import torch
import datetime
import cv2
import numpy as np

def train(model, device, train_loader, val_loader, optimizer, epoch):
    """
    Trains the model on training data
    """
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        # convert one-hot to numerical categories
        target = torch.argmax(target, dim=1).long()
        optimizer.zero_grad()
        output = model(data)
        criterion = nn.CrossEntropyLoss()
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    train_loss, train_cm = evaluate(model, device, train_loader)
    train_acc = get_accuracy(train_cm)
    print('Train Epoch: {} @ {} \nTrain Loss: {:.4f} - Train Accuracy: {:.1f}%'.format(
        epoch, datetime.datetime.now().time(), train_loss, train_acc * 100))

    val_loss, val_cm = evaluate(model, device, val_loader)
    val_acc = get_accuracy(val_cm)
    print("Val Loss: {:.4f} - Val Accuracy: {:.1f}%".format(val_loss, val_acc * 100))

    return train_loss, train_acc, val_loss, val_acc

def evaluate(model, device, data_loader):
    """
    Evaluates the model and returns loss, accuracy and confusion matrix
    """
    model.eval()
    loss = 0
    confusion_matrix = torch.zeros(4, 4) # 4 classes
    with torch.no_grad():
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)
            target = torch.argmax(target, dim=1).long()
            output = model(data)
            criterion = nn.CrossEntropyLoss()
            loss += criterion(output, target)
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            
            for t, p in zip(target.view(-1), pred.view(-1)):
                confusion_matrix[t.long(), p.long()] += 1

    loss /= len(data_loader)
        
    return loss, confusion_matrix

def predict(model, video_path):
    """
    Predicts the label of the video given its filepath
    """
    model.eval()
    
    frames = np.load(video_path)

    # transform
    arr = []
    for frame in frames:
        frame = np.float32(frame)
        im = frame.reshape((24, 32))
        im = cv2.resize(im, (72, 96))
        arr.append(im)

    arr = np.array(arr) / 255
    
    # display
    display_frames(arr)

    arr = np.expand_dims(arr, axis=0)
    arr = torch.from_numpy(arr).float()

    output = model(arr)
    pred = output.argmax(dim=1, keepdim=True).item()
    classes = {0: 'sit', 1: 'stand', 2: 'bend', 3: 'tampered'}
    
    prediction = classes[pred]
    return prediction    

def load_model(model, model_path):
    """
    Load model from file path
    """
    model.load_state_dict(torch.load(model_path))
    return model

def get_accuracy(cm):
    """
    Calculates the accuracy score from confusion matrix
    """
    return torch.diag(cm).sum() / cm.sum()

def display_frames(arr):
    """
    Prints 10 frames in 1x5 grid
    """
    fig, ax = plt.subplots(nrows=1, ncols=5, figsize=(10,5))
    for i in range(arr.shape[0]):
        frame = arr[i]
        ax.ravel()[i].imshow(frame)
        ax.ravel()[i].set_title('Frame {}'.format(i))
        ax.ravel()[i].set_axis_off()
    plt.show()

def plot_curves(train_arr, test_arr, plot_name):
    """
    Plots training and validation learning curves over successive epochs
    """
    plt.plot(train_arr, label="Train")
    plt.plot(test_arr, label="Validation")
    plt.title(plot_name)
    plt.legend()
    plt.show()
    