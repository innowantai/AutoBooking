import os
import pandas as pd
import csv
import numpy as np
from PIL import Image
import cv2
import PIL

def toonehot(text,paradict_EngTonum):
    labellist = []
    for number in text:
        onehot = [0 for _ in range(len(paradict_EngTonum))] 
        num = paradict_EngTonum[number]
        onehot[num] = 1
        labellist.append(onehot)
    return labellist


def LoadCsvToProcessLabel(savePath,Number):
    DataCsv = open(savePath, 'r', encoding = 'utf8')
    Read_Label = [toonehot(row[2],paradict_EngTonum) for row in csv.reader(DataCsv)]
    Train_label = [[] for _ in range(Number)]
    for arr in Read_Label:
        for index in range(Number):
            Train_label[index].append(arr[index])
    Train_label = [arr for arr in np.asarray(Train_label)]
    return Train_label


def A_0_GetFigurePath(Path):
    files = os.listdir(Path)
    nPath = []
    for ff in files:
        if ff.find('.jpg') != -1:
            nPath.append(os.path.join(Path,ff))
    return nPath
    


num = 6
TrainSetFolderName = 'train_set_' + str(num)
RealSetFolderName = 'real_set_' + str(num)
CaseName = 0
Path = [os.path.join(os.getcwd(),TrainSetFolderName),os.path.join(os.getcwd(),RealSetFolderName)]
SaveName = ['train_' + str(num) + '.csv','vail'  + str(num) +  '.csv']
DataName = ['Train_data' + str(num) + '.npy','vali_data' + str(num) + '.npy']
LabelName = ['Train_Label' + str(num) + '.npy','vali_Label' + str(num) + '.npy']
path = Path[CaseName]
savePath = os.path.join(path,SaveName[CaseName])
files = os.listdir(path)
Name = []
ID = []
ind = []
for ii,ff in enumerate(files):
    if ff.find('.jpg') != -1:            
        Name.append(ff)
        ID.append(ff.split('_')[1].split('.')[0])
        ind.append(ii)
        
test1 = pd.DataFrame(Name)
test2 = pd.DataFrame(ID)
Data = pd.concat([test1,test2],axis=1)
Data.to_csv(savePath, header=False)


paradict_numToEng = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}
paradict_EngTonum = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}


 

print("Reading training data...")
tData = A_0_GetFigurePath(path)

 
#train_data = np.stack([np.array(Image.open(index))/255.0 for index in tData])

Res = []
for ii,index in enumerate(tData):
    print('\r' + str(ii) + '/' + str(len(tData)),end = '')
    ff = Image.open(index).convert('RGB')#.resize((80,50))
    open_cv_img = np.array(ff) 
    img_gray = cv2.cvtColor(open_cv_img,cv2.COLOR_BGR2GRAY)
    img_gray[img_gray > 110] = 0
    _, thresh = cv2.threshold(img_gray,0,255,1)  
    test1 = PIL.Image.fromarray(thresh).resize((100,50))  #  
    Res.append(np.array(test1)/255)
    
train_data = np.stack(Res)
train_Label = LoadCsvToProcessLabel(savePath,num)


test = np.zeros((len(train_data),50,100,1))
test[:,:,:,0] = train_data

print('\nThe Figures Loading compeleted')
  
f1 = open(DataName[CaseName],'wb')
np.save(f1,test)
f1.close() 


print('The Figures saving compeleted')

# =============================================================================
# f2 = open(LabelName[CaseName],'wb')
# np.save(f2,train_Label)
# =============================================================================



words = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ind = {}
for ii,w in enumerate(words):
    ind[ii] = w





