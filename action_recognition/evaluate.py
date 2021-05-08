import argparse
from model import *
from dataset import *
from utils import *
import torch
from torch.utils.data import DataLoader

# arguments to command line
parser = argparse.ArgumentParser(description="Evaluate model")
parser.add_argument("--checkpoint", type=str, default=None, help="file path to save the model")
parser.add_argument("--arch", type=str, default="custom", help="set architecture")

# Parse arguments
args = parser.parse_args()
checkpoint = args.checkpoint
arch  = args.arch

# set cpu
device = torch.device("cpu")

model = CNN_LSTM(arch, device) 
model.to(device)

if checkpoint:
    model = load_model(model, checkpoint)

# Dataloader
test_ds = MLX90640_Dataset('test')
test_loader = DataLoader(test_ds, 1, shuffle=False)

# Evaluate model based on overall accuracy and per-class accuracy
_, cm = evaluate(model, device, test_loader)
acc = get_accuracy(cm)
per_class_acc = cm.diag()/cm.sum(1)

print('Overall Accuracy: {:.1f}%\n'.format(acc * 100))
print('Per-class Accuracy')
for idx, val in enumerate(per_class_acc):
    print('   {}: {:.1f}%'.format(test_ds.classes[idx], val.item()*100))
    
print('\nConfusion Matrix:\n{}'.format(cm.numpy()))
