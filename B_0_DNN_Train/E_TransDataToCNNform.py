import numpy as np 
np.random.seed(1337)
from keras.datasets import mnist 
import matplotlib.pyplot as plt
import PIL
import os

def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,32,44))  
    for vv in range(Num):
        index = data[vv,:].reshape((33,50))
        index = index[1:,3:-3]
        Result[vv,:,:] = index
    return Result
    

(X_train, y_train),(X_test,y_test) = mnist.load_data()
train = np.load('X_training.npy')
test = np.load('X_test.npy')

X_Train = TransDatafromToCNN(train)
X_Test = TransDatafromToCNN(test)


     

f1 = open('X_Training_CNN.npy','wb')
f2 = open('X_Test_CNN.npy','wb')

np.save(f1,X_Train)
np.save(f2,X_Test)
f1.close()
f2.close()














# =============================================================================
# kk1 = 0
# kk2 = 0
# kk3 = 0
# for ii in range(X_Train.shape[0]):
#     index = X_Train[ii,:,:]
#     test1 = index[:,4]
#     test2 = index[:,-4]
#     test3 = index[2,:]
#     if test1[test1 != 1] != []:
#         kk1 += 1        
#     if test2[test2 != 1] != []:
#         kk2 += 1
#     if test3[test3 != 1] != []:
#         kk3 += 1
# =============================================================================








