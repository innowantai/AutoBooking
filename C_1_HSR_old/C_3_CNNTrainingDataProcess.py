import numpy as np 
np.random.seed(1337)
from keras.datasets import mnist 
import matplotlib.pyplot as plt
import PIL
import os


# The left and right boundary reduce 12 pixels respectively
# The top and bottom boundary reduct 4 pixels respectively

rHH = 0
rWW = 0
def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,33,50))  
    Result = np.zeros((Num,33-5,50-10)) 
    for vv in range(Num):
        index = data[vv,:].reshape((33,50))
        index = index[3:-2,5:-5]
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
# # Take of boundary check
# kk1 = 0
# kk2 = 0
# kk5 = 0
# kk6 = 0
# hh1 = 3
# hh2 = 2
# po1 = 5
# po2 = 5
# for ii in range(len(X_Train)):
#     index = X_Train[ii,:,:]
#     if len(np.where(index[:,po1] == 0)[0]) != 0 :
#         kk1 += 1
#     if len(np.where(index[:,-po2] == 0)[0]) != 0 : 
#         kk2 += 1
#     if len(np.where(index[hh1,:] == 0)[0]) != 0 :
#         kk5 += 1
#     if len(np.where(index[-hh2,:] == 0)[0]) != 0 :
#         kk6 += 1
# 
# kk3 = 0
# kk4 = 0
# kk7 = 0
# kk8 = 0
# for ii in range(len(X_Test)):
#     index = X_Train[ii,:,:]
#     if len(np.where(index[:,po1] == 0)[0]) != 0 :
#         kk3 += 1
#     if len(np.where(index[:,-po2] == 0)[0]) != 0 :
#         kk4 += 1
#     if len(np.where(index[hh1,:] == 0)[0]) != 0 :
#         kk7 += 1
#     if len(np.where(index[-hh2,:] == 0)[0]) != 0 :
#         kk8 += 1
# print(kk1,kk2,kk3,kk4)
# print(kk5,kk6,kk7,kk8)
# 
# 
# =============================================================================



 