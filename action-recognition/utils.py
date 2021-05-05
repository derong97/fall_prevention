from dataset import *
import matplotlib.pyplot as plt
import torch.nn as nn
import datetime
import cv2

def plot_class_distribution():
    """
    Plots bar graphs of the class distributions of train, val and test set
    over the 3 classes: sit, stand and tilt.

    There is 1 bar graph plotted:
    - Number of images per class for each dataset (side by side)
    """

    # Plot number of images per class for each dataset
    train_ds = MLX90640_Dataset('train')
    val_ds = MLX90640_Dataset('val')
    test_ds = MLX90640_Dataset('test')

    labels = train_ds.dataset_numbers.keys()
    train_num = train_ds.dataset_numbers.values()
    val_num = val_ds.dataset_numbers.values()
    test_num = test_ds.dataset_numbers.values()
    
    x = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots()
    ax.bar(x - width, train_num, width, label='Train')
    ax.bar(x, val_num, width, label='Validation')
    ax.bar(x + width, test_num, width, label='Test')

    ax.set_title('No. of videos per class')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
        
    plt.show()

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

    train_loss, train_acc, _ = evaluate(model, device, train_loader)
    print('Train Epoch: {} @ {} \nTrain Loss: {:.4f} - Train Accuracy: {:.1f}%'.format(
        epoch, datetime.datetime.now().time(), train_loss, train_acc))

    val_loss, val_acc, _ = evaluate(model, device, val_loader)
    print("Val Loss: {:.4f} - Val Accuracy: {:.1f}%".format(val_loss, val_acc))

    return train_loss, train_acc, val_loss, val_acc

def evaluate(model, device, data_loader):
    """
    Evaluates the model and returns loss, accuracy and confusion matrix
    """
    model.eval()
    loss = 0
    correct = 0
    confusion_matrix = torch.zeros(3, 3) # 3 classes
    with torch.no_grad():
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)
            target = torch.argmax(target, dim=1).long()
            output = model(data)
            criterion = nn.CrossEntropyLoss()
            loss += criterion(output, target)
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()
            
            for t, p in zip(target.view(-1), pred.view(-1)):
                confusion_matrix[t.long(), p.long()] += 1

    loss /= len(data_loader)
    acc = 100. * correct / len(data_loader.dataset)
    return loss, acc, confusion_matrix

def predict(model, video_path):
    """
    Predicts the label of the video given its filepath
    """
    
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
    classes = {0: 'sit',
               1: 'stand',
               2: 'tilt'}
    prediction = classes[pred]
    return prediction    

def load_model(model, model_path):
    """
    Load model from file path
    """
    model.load_state_dict(torch.load(model_path))
    return model

def display_frames(arr):
    
    fig, ax = plt.subplots(nrows=2, ncols=5, figsize=(10,5))
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
    