from dataset import *
import matplotlib.pyplot as plt

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
    
def plot_curves(train_arr, test_arr, plot_name):
    """
    Plots training and validation learning curves over successive epochs
    """
    plt.plot(train_arr, label="Train")
    plt.plot(test_arr, label="Validation")
    plt.title(plot_name)
    plt.legend()
    plt.show()