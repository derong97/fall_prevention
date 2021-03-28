import matplotlib.pyplot as plt

def load_dataset(filepath):
    return

def performance_curve(train_arr, test_arr, title)
    """
    Plot the evolution of metric score over epochs
    """
    plt.plot(train_arr, label="Train")
    plt.plot(test_arr, label="Test")
    plt.title(title)
    plt.legend()
    plt.show()