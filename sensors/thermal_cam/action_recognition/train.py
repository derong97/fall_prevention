import argparse
from model import * 
from dataset import *
from utils import *
import torch
from torch.optim import Adam, SGD
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR
import matplotlib.pyplot as plt
import time

# arguments to command line
parser = argparse.ArgumentParser(description="Train model")
parser.add_argument("--arch", type=str, default="custom", help="set architecture")
parser.add_argument("--epochs", type=int, default=50, help="set epochs")
parser.add_argument("--batch", type=int, default=16, help="set batch size")
parser.add_argument("--lr", type=float, default=0.001, help="set learning rate")
parser.add_argument("--beta1", type=float, default=0.9, help="set the first momentum term")
parser.add_argument("--beta2", type=float, default=0.9, help="set the second momentum term")
parser.add_argument("--weight_decay", type=float, default=1e-5, help="set weight decay")
parser.add_argument("--gamma", type=float, default=0.9, help="set learning rate gamma")
parser.add_argument("--step_size", type=int, default=1, help="set scheduler step size")
parser.add_argument("--cuda", type=bool, default=True, help="enable cuda training")
parser.add_argument("--checkpoint", type=str, default=None, help="checkpoint to load model")
parser.add_argument("--save_dir", type=str, default=None, help="file path to save the model")

# get arguments
args = parser.parse_args()
arch = args.arch
batch_size = args.batch
epochs = args.epochs
learning_rate = args.lr
beta1 = args.beta1
beta2 = args.beta2
weight_decay = args.weight_decay
gamma = args.gamma
step_size = args.step_size
cuda = args.cuda
save_dir = args.save_dir
checkpoint = args.checkpoint

# set cpu / gpu
use_cuda = cuda and torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

model = CNN_LSTM(arch, device)
model.to(device)

# Dataset
train_ds = MLX90640_Dataset('train')
val_ds = MLX90640_Dataset('val')

# Dataloader
train_loader = DataLoader(train_ds, batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size, shuffle=True)

# Initialize model and optimizer
if checkpoint:
    model = load_model(model, checkpoint)

num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print("Number of trainable params: {}".format(num_params))
      
optimizer = Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=learning_rate, betas=(beta1, beta2), weight_decay=weight_decay)
scheduler = StepLR(optimizer, step_size=step_size, gamma=gamma)

train_losses = []
train_accs = []
val_losses = []
val_accs = []

print("Training...")
start = time.time()
for epoch in range(1, epochs + 1):
    train_loss, train_acc, val_loss, val_acc = train(model, device, train_loader, val_loader, optimizer, epoch)
    train_losses.append(train_loss)
    train_accs.append(train_acc)
    val_losses.append(val_loss)
    val_accs.append(val_acc)

    scheduler.step()

    # save best checkpoint based on validation acc score
    if epoch == 1:
        best_val_score = val_acc

    if save_dir:
        if val_acc >= best_val_score:
            torch.save(model.state_dict(), save_dir)
            best_val_score = val_acc

time_taken = time.time() - start            
print("Avg time taken per epoch: {}s".format(time_taken / epochs))            
            
# plot learning curves
plot_curves(train_losses, val_losses, "Loss curves")
plot_curves(train_accs, val_accs, "Accuracy curves")
