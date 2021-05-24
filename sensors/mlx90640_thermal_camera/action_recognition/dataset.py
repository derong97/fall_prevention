from utils import display_frames
import torch
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

class MLX90640_Dataset(Dataset):
    """
    MLX90640 Dataset Class
    """

    def __init__(self, group, data_dir='data', num_frames=10):
        """
        Constructor for MLX90640 Dataset class

        Parameters:
            - group should be set to test, train or val

        """

        # Number of frames per video
        self.num_frames = num_frames

        # Size of frame: mlx90640 is a 32x24 IR array
        self.frame_size = (24, 32)

        # 5 classes
        self.classes = {0: 'sit',
                        1: 'stand',
                        2: 'bend',
                        3: 'tampered'}

        # Dataset should belong to only one group: train, test or val
        self.group = group
        
        # root directory for the data
        root_dir = data_dir + '/{}'.format(self.group)
        self.dataset_paths = {'sit': root_dir + '/sit',
                              'stand': root_dir + '/stand',
                              'bend': root_dir + '/bend',
                              'tampered': root_dir + '/tampered'}
        
        # Number of videos for each class in the dataset
        self.dataset_numbers = {}
        
        # List of filenames of videos for each class in the dataset
        self.dataset_filenames = {}
        for key in self.dataset_paths:
            path = self.dataset_paths[key]
            _, _, files = next(os.walk(path))
            self.dataset_numbers[key] = len(files)
            self.dataset_filenames[key] = files
    
    def describe(self):
        """
        Descriptor function.
        Will print details about the dataset when called.
        """

        msg = "This is the {} dataset from our self-collected MLX90640 dataset used for Capstone.\n".format(self.group)
        msg += "It contains a total of {} videos. \n".format(sum(self.dataset_numbers.values()))
        msg += "The videos are stored in the following locations and each one contains the following number of videos:\n"
        
        for key, val in self.dataset_paths.items():
            msg += " - {}, in folder {}: {} videos.\n".format(key, val, self.dataset_numbers[key])
        print(msg)

    def open_video(self, class_val, index_val):
        """
        Opens video with specified parameters.

        Parameters:
            - class_val should be set to one of the classes i.e.: 'sit', 'stand', 'tile
            - index_val should be an integer with values between 0 and the maximal number of videos in dataset.

        Returns processed video as numpy array.
        """

        # Asserts checking for consistency in passed parameters
        err_msg = "Error - class_val variable is incorrect."
        assert class_val in self.classes.values(), err_msg
        max_val = self.dataset_numbers['{}'.format(class_val)]
        err_msg = "Error - index_val variable should be an integer between 0 and the maximal number of videos."
        err_msg += "\n(In {}, you have {} videos.)".format(class_val, max_val)
        assert isinstance(index_val, int), err_msg
        assert index_val >= 0 and index_val <= max_val, err_msg

        # open video as numpy array
        filenames = self.dataset_filenames['{}'.format(class_val)]
        filename = '{}/{}'.format(self.dataset_paths['{}'.format(class_val)], filenames[index_val])
        
        # sample the right number of frames from the npy arrays
        arr = np.load(filename)
        arr = self.transform(arr)

        return arr

    def show_video(self, class_val, index_val):
        """
        Opens, then displays video frames with specified parameters

        Parameters:
            - class_val should be set to one of the classes i.e.: 'sit', 'stand', 'tilt'
            - index_val should be an integer with values between 0 and the maximal number of videos in dataset.
        """

        # open video
        arr = self.open_video(class_val, index_val)
        display_frames(arr)

    def transform(self, frames):
        """
        Transforms the frames
        """
        arr = []
        
        # take 5 frames only
        for frame in frames[:5]:
            frame = np.float32(frame)
            im = frame.reshape(self.frame_size)
            im = cv2.resize(im, tuple(i*3 for i in self.frame_size))
            
            # only apply data augmentation to training samples
            if self.group == 'train':
                # TODO: translation?
                pass
            
            arr.append(im)
        
        arr = np.array(arr) / 255
        
        return arr

    def __len__(self):
        """
        Length special method, returns the number of videos in dataset.
        """

        # Length function
        return sum(self.dataset_numbers.values())

    def __getitem__(self, index):
        """
        Getitem special method.

        Expects an integer value index, between 0 and len(self) - 1.

        Returns the video and its label as a one hot vector, both
        in torch tensor format in dataset.
        """

        # Get item special method
        one_hot = np.zeros(len(self.classes))

        first_val = int(list(self.dataset_numbers.values())[0])
        second_val = int(list(self.dataset_numbers.values())[1]) + first_val
        third_val = int(list(self.dataset_numbers.values())[2]) + second_val

        if index < first_val:
            class_num = 0
        elif index < second_val:
            class_num = 1
            index -= first_val
        elif index < third_val:
            class_num = 2
            index -= second_val
        else:
            class_num = 3
            index -= third_val

        class_val = self.classes[class_num]
        one_hot[class_num] = 1
        label = torch.Tensor(one_hot)

        vid = self.open_video(class_val, index)
        vid = torch.from_numpy(vid).float()
        return vid, label
