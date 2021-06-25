## Posture Action Recognition


## Instructions to run python files in the notebook
1. `train.py`: Trains the model.

    To train the default model, run the following command:
    `python train.py`  

    Optional parameters:  
    `--arch`: set architecture      
    `--epochs`: set number of training epochs  
    `--batch`: set batch size  
    `--lr`: set learning rate    
    `--beta1`: set first momentum term for Adam optimizer  
    `--beta2`: set second momentum term for Adam optimizer  
    `--weight_decay`: set weight decay for regularization on loss function  
    `--gamma`: set gamma for learning rate scheduler  
    `--step_size`: set step size for learning rate scheduler  
    `--cuda`: enable cuda training  
    `--checkpoint`: filepath to a checkpoint to load model  
    `--save_dir`: filepath to save the model  

2. `evaluate.py`: Evaluate the trained model on test set.  

     After training the model and saving it, we can evaluate the model on test set.  
     For example, the model is saved as `./custom.pt`.  
     
     Run the following command:  
     `python evaluate.py --arch custom --checkpoint ./custom.pt`  
     where the `arch` parameter has to match the architecture of the saved model.  

3. `predict.py`: Predicts the class of a video using the trained model.  

    After training the model and saving it, we can use the model to predict the class of a single video.

    Run the following command:  
    `python predict.py --arch custom --checkpoint custom.pt --video_path <video_file_path>`  
    where `video_file_path` is the file path to the video (in numpy format). 
