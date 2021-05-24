import torch
import torch.nn as nn
import torch.nn.functional as F

class CNN_LSTM(nn.Module):
    """
    Model with Convolutional LSTM architecture
    """

    def __init__(self):
        super(CNN_LSTM, self).__init__()
        
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2,2)),

            nn.Conv2d(64, 128, 3),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2,2)),
            nn.Dropout2d(p=0.3),

            nn.Conv2d(128, 128, 3),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2,2)),
            nn.Dropout2d(p=0.3),
        )
        
        self.fc1 = nn.Sequential(nn.Linear(8960, 128), nn.Dropout())
        self.rnn = nn.LSTM(128, 256, num_layers = 1)
        self.fc2 = nn.Sequential(nn.Linear(256, 128), nn.ReLU(), nn.Dropout())
        self.classifier = nn.Linear(128, 4)

    def forward(self, inputs, hidden=None):
        seq_length = len(inputs[0])
        batch_size = len(inputs)
        lstm_in = torch.zeros(seq_length, batch_size, self.rnn.input_size)
            
        for j in range(seq_length):
            x = inputs[:,j,:,:]
            x = x.unsqueeze(1).repeat(1,3,1,1)
            x = self.features(x)
            x = x.view(x.size(0), -1)
            x = self.fc1(x)
            lstm_in[j] = x
                    
        outputs, hidden = self.rnn(lstm_in, hidden)
        # take the last output of sequence
        outputs = outputs[-1]
        outputs = self.fc2(outputs)
        outputs = self.classifier(outputs)
        output = F.log_softmax(outputs, dim=1)
        return output
