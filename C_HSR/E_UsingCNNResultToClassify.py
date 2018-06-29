import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
import PIL 
import os 
import numpy as np 
from keras.models import load_model
import shutil
import keras 



def TransResult(result): 
    Res = []
    for vv in result.tolist():
        Res.append(vv.index(max(vv))) 
    return Res

def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,33,50))  
    Result = np.zeros((Num,33-5,50-10)) 
    for vv in range(Num):
        index = data[vv,:].reshape((33,50))
        index = index[3:-2,5:-5]
        Result[vv,:,:] = index
    return Result




# Loading trained CNN model
model = load_model('my_model_CNN_5000_2.h5')







Path = os.path.join(os.getcwd(),'_nonClassify','0_Split')
Files_ = os.listdir(Path)
Files = []
for ff in Files_:
    if ff.find('.jpg') != -1:
        Files.append(ff)


paraDic1 = {0: '2', 1: '3', 2: '4', 3: '5', 4: '7', 5: '9', 6: 'A', 7: 'C', 8: 'F', 9: 'H', 10: 'K', 11: 'M', 12: 'N', 13: 'P', 14: 'Q', 15: 'R', 16: 'T', 17: 'Y', 18: 'Z'}
paraDic2 = {'2': 0, '3': 1, '4': 2, '5': 3, '7': 4, '9': 5, 'A': 6, 'C': 7, 'F': 8, 'H': 9, 'K': 10, 'M': 11, 'N': 12, 'P': 13, 'Q': 14, 'R': 15, 'T': 16, 'Y': 17, 'Z': 18}

# Create folder for saving corresponding figure
for ii in paraDic1:
    if not os.path.exists(os.path.join(Path,paraDic1[ii])) :
        os.mkdir(os.path.join(Path,paraDic1[ii])) 


 


# Loading All fiugre and saving to np.array format
baseH = 50
digits = []
labels = []     
for ii,jj in enumerate(Files):
    print(str(ii),'/',str(len(Files)))
    pil_image = PIL.Image.open(os.path.join(Path,jj)).convert('1') 
    baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
    img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS)
    digits.append([vv for vv in img.getdata()])
digit_ary = np.array(digits) / 255



# Translate the figure of np.array to CNN format

X_Test = TransDatafromToCNN(digit_ary)

X_Test = X_Test.reshape(-1, 1,28, 40)
 
Res = TransResult(model.predict(X_Test))





print('Moving Figure to correspond Folder')
for ii,ff in enumerate(Files):
    print('Process : ', str(ii),'/',str(len(Files)) )
    folder = paraDic1[Res[ii]]
    shutil.move(os.path.join(Path,ff),os.path.join(Path,folder))


print('Move Completed')









