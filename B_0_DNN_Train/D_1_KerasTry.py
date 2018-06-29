import os
os.environ['KERAS_KACKEND'] = 'theano'
import keras

import numpy as np 
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
from keras.models import load_model
 

def TransResult(result): 
    Res = []
    for vv in result.tolist():
        Res.append(vv.index(max(vv))) 
    return Res

X_train =  np.load('X_Training.npy')
y_train =  np.load('Y_Training.npy')
X_test =   np.load('X_test.npy')
y_test =   np.load('Y_test.npy')


y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

 
### Another way to building your Neueal net
model = Sequential([
        Dense(1000, input_dim = 1650,),
        Activation('sigmoid'), 
        Dense(1000,), 
        Activation('sigmoid'),   
        Dense(400,), 
        Activation('relu'),   
        Dense(10),
        Activation('softmax'),
        ])
saveName = 'my_model3.h5'
    
# =========================== This Result is good enough =====================================
# ### Another way to building your Neueal net
# model = Sequential([
#         Dense(1000, input_dim = 1650,),
#         Activation('sigmoid'), 
#         Dense(400,), 
#         Activation('sigmoid'),   
#         Dense(400,), 
#         Activation('relu'),   
#         Dense(10),
#         Activation('softmax'),
#         ])
# saveName = 'my_model2.h5'
# =============================================================================
    
# =============================================================================
# ### Another way to building your Neueal net
# model = Sequential([
#         Dense(500, input_dim = 1650,),
#         Activation('relu'), 
#         Dense(400,), 
#         Activation('relu'), 
#         Dense(200,), 
#         Activation('relu'), 
#         Dense(200,), 
#         Activation('relu'),  
#         Dense(10),
#         Activation('softmax'),
#         ])
# =============================================================================
    

### Another way to define your optimizer
rmsprop = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

### 

model.compile(
        optimizer=rmsprop,
        loss='categorical_crossentropy',
        metrics=['accuracy'],
        )


print('Training ------ ')

### Another way to train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)

print('Testing ------ ')
 
loss, accuracy = model.evaluate(X_test, y_test)

print('test loss: ', loss)
print('test accuracy: ', accuracy)


xx = model.predict(X_train)
xx = np.array(TransResult(xx))
yy = np.array(TransResult(y_train))

cmp = xx - yy
print('error number:',len(cmp[cmp != 0]))


model.save(saveName)
