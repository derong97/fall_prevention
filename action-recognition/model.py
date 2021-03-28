from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv3D, MaxPooling3D, ZeroPadding3D

def C3D_model(input_shape, num_classes, weights_path=None, summary=False, trainable=True, num_layers_remove=0):
    """
    Return a Conv3D model with an option to load pretrained weights
    """

    model = Sequential()

    # 1st layer group
    model.add(Conv3D(64, (3, 3, 3), activation="relu", name="conv1", 
                     input_shape=input_shape, strides=(1, 1, 1), padding="same"))  
    model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(1, 2, 2), name="pool1", padding="valid"))

    # 2nd layer group  
    model.add(Conv3D(128, (3, 3, 3), activation="relu",name="conv2", 
                     strides=(1, 1, 1), padding="same"))
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2), name="pool2", padding="valid"))

    # 3rd layer group   
    model.add(Conv3D(256, (3, 3, 3), activation="relu",name="conv3a", 
                     strides=(1, 1, 1), padding="same"))
    model.add(Conv3D(256, (3, 3, 3), activation="relu",name="conv3b", 
                     strides=(1, 1, 1), padding="same"))
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2), name="pool3", padding="valid"))

    # 4th layer group  
    model.add(Conv3D(512, (3, 3, 3), activation="relu",name="conv4a", 
                     strides=(1, 1, 1), padding="same"))   
    model.add(Conv3D(512, (3, 3, 3), activation="relu",name="conv4b", 
                     strides=(1, 1, 1), padding="same"))
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2), name="pool4", padding="valid"))

    # 5th layer group  
    model.add(Conv3D(512, (3, 3, 3), activation="relu",name="conv5a", 
                     strides=(1, 1, 1), padding="same"))   
    model.add(Conv3D(512, (3, 3, 3), activation="relu",name="conv5b",
                      strides=(1, 1, 1), padding="same"))
    model.add(ZeroPadding3D(padding=(0, 1, 1)))	
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2), name="pool5", padding="valid"))
    model.add(Flatten())
                     
    # FC layers group
    model.add(Dense(4096, activation='relu', name='fc6'))
    model.add(Dropout(.5))
    model.add(Dense(4096, activation='relu', name='fc7'))
    model.add(Dropout(.5))
    model.add(Dense(num_classes, activation='softmax', name='fc8'))

    # Print model summary, by default False
    if summary:
        print('Original model summary:' )
        print(model.summary())

    # Path to the model file with pretrained weights, by default None
    if weights_path:
        print('Loading Model Weights from %s' % weights_path)
        model.load_weights(weights_path)

    # Pop layers from the top of the network
    if num_layers_remove > 0:
        print('Popping last %s layers' % num_layers_remove)
        for idx in range(num_layers_remove):
            model.pop()

        if summary:
            print('Summary after popping:')
            print(model.summary())
    
    # Set all the layers as trainable, by default True
    for layer in model.layers:
        layer.trainable = trainable

    return model