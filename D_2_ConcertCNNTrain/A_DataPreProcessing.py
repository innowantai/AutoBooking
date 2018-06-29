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
    


CaseName = 0   ### 0 or 1 for select train or vail data respectively
Path = [os.path.join(os.getcwd(),'train_set'),os.path.join(os.getcwd(),'real_set')]
SaveName = ['train.csv','vail.csv']
DataName = ['Train_data.npy','vali_data.npy']
LabelName = ['Train_Label.npy','vali_Label.npy']
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


paradict_numToEng = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
paradict_EngTonum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}




Number = 4

print("Reading training data...")
tData = A_0_GetFigurePath(path)

 
#train_data = np.stack([np.array(Image.open(index))/255.0 for index in tData])

Res = []
for ii,index in enumerate(tData):
    print('\r' + str(ii) + '/' + str(len(tData)),end = '')
    ff = Image.open(index).convert('RGB').resize((80,50))
    open_cv_img = np.array(ff) 
    img_gray = cv2.cvtColor(open_cv_img,cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray,230,255,1) 
    thresh[0,:] = 255    
    test1 = PIL.Image.fromarray(thresh).resize((80,50))  #
    Res.append(np.array(test1)/255)
    
train_data = np.stack(Res)
train_Label = LoadCsvToProcessLabel(savePath,4)
 

test = np.zeros((len(train_data),50,80,1))
test[:,:,:,0] = train_data

print('The Figures Loading compeleted')
  
f1 = open(DataName[CaseName],'wb')
np.save(f1,test)
f1.close() 


print('The Figures saving compeleted')

# =============================================================================
# f2 = open(LabelName[CaseName],'wb')
# np.save(f2,train_Label)
# =============================================================================



