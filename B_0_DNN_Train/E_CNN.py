import numpy as np
np.random.seed(1337)
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
from keras.models import load_model

def TransResult(result): 
    Res = []
    for vv in result.tolist():
        Res.append(vv.index(max(vv))) 
    return Res

X_train = np.load('X_Training_CNN.npy')
X_test  = np.load('X_Test_CNN.npy')
y_train = np.load('Y_Training.npy')
y_test = np.load('Y_test.npy')

 
# data pre-processing
X_train = X_train.reshape(-1, 1,32, 44)
X_test = X_test.reshape(-1, 1,32, 44)

y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# Another way to buliding CNN
model = Sequential()

# Conv layer 1 output shape (32,32,44)
model.add(Convolution2D(
        nb_filter = 32,
        nb_row = 5,
        nb_col = 5,
        border_mode = 'same',   # padding method
        input_shape = (1,
                       32,44),  # heigh and width        
        ))
model.add(Activation('relu'))        
        
# Pooling layer 1 (max pooling) output shape (32,16,22)
model.add(MaxPooling2D(
        pool_size = (2,2),
        strides = (2,2),
        border_mode = 'same',
        ))


# Conv layer 2 output shape (64,14,14)
model.add(Convolution2D(nb_filter = 64,nb_row = 5,nb_col = 5,border_mode = 'same'))
model.add(Activation('relu'))   
 


# Pooling layer 1 (max pooling) output shape (64,8,11)
model.add(MaxPooling2D(pool_size = (2,2), border_mode = 'same'))



# Fully connected layer 1 input shape (64*7*7) = (3136) , output shape (1024)
model.add(Flatten())
model.add(Dense(2000))
model.add(Activation('sigmoid')) 
model.add(Dense(500))
model.add(Activation('sigmoid')) 

# Fully connected layer 2 to shape (10) for 10 classes
model.add(Dense(10))
model.add(Activation('softmax'))


adam = Adam(lr=1e-4)

# We add metrics to get more results you want to see
model.compile(optimizer=adam,
              loss='categorical_crossentropy',
              metrics=['accuracy'])




print('Training ------------')
# Another way to train the model
model.fit(X_train, y_train, epochs=30, batch_size=8,)

print('\nTesting ------------')
# Evaluate the model with the metrics we defined earlier
loss, accuracy = model.evaluate(X_test, y_test)

print('\ntest loss: ', loss)
print('\ntest accuracy: ', accuracy)

model.save('my_model_CNN2.h5')


