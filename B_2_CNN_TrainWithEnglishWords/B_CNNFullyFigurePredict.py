from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
from PIL import Image
import numpy as np 
import os
import cv2
import PIL
from keras.models import load_model




def TransferCNNResult(predict,paradict_numToEng):
    Res = []
    for ii in range(len(data)): 
        res = []
        for nn,ff in enumerate(predict):
            index = predict[nn]
            res_ = index[ii]
            po = np.where(res_ == max(res_))[0][0]
            res.append(po) 
        Res.append(res)
    return Res
 
def A_0_GetFigurePath(Path):
    files = os.listdir(Path)
    nPath = []
    for ff in files:
        if ff.find('.jpg') != -1:
            nPath.append(os.path.join(Path,ff))
    return nPath


 
paradict_numToEng = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}
paradict_EngTonum = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}




Number = 6

model = load_model('cnn_model' + str(Number) + '.h5')


CaseName = 1
Path = [os.path.join(os.getcwd(),'train_set_' + str(Number)),os.path.join(os.getcwd(),'real_set_' + str(Number) )]
SaveName = ['train' + str(Number) + '.csv','vali' + str(Number) + '.csv']
path = Path[CaseName]
files = os.listdir(path)
Name = []
ID = [] 
for ii,ff in enumerate(files):
    if ff.find('.jpg') != -1:            
        Name.append(ff)
        ID.append(ff.split('_')[1].split('.')[0]) 
        
AnsAll = []
for ww in ID:
    index = []
    for w in ww:
        index.append(paradict_EngTonum[w])
    AnsAll.append(index)
        
tData = A_0_GetFigurePath(path)     

   
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
    
data_ = np.stack(Res)
data = np.zeros((len(data_),50,100,1))
data[:,:,:,0] = data_

print('\nData Loading Completed')


def TransNumToEng(data,paradict_numToEng):
    res = []
    for ff in data:
        res.append(paradict_numToEng[ff])
    return res
    


predict = model.predict(data)
Res = TransferCNNResult(predict,paradict_numToEng)
 
kk = 0
for ii in range(len(Res)):
    Ans = np.array(AnsAll[ii])
    Val = np.array(Res[ii])
    diff = np.where((Ans - Val) != 0)[0]
    if len(diff) != 0:
        diffEng = [paradict_numToEng[Val[re]] for re in diff]
        #print(ii,TransNumToEng(Ans,paradict_numToEng),TransNumToEng(Val,paradict_numToEng),'Diff = ',diffEng)
        print(ii,TransNumToEng(Ans,paradict_numToEng),TransNumToEng(Val,paradict_numToEng),'總共有',len(diffEng),'字母錯誤 ==>',diffEng)
         
    else:
        kk += 1
        print(ii,TransNumToEng(Ans,paradict_numToEng),TransNumToEng(Val,paradict_numToEng),'Ok')
         
    
    
print('Result : ',str(kk),'/',str(len(Res)),' ==> ','%.1f' % (kk/(len(Res))*100) ,'%')
















