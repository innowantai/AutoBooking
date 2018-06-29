from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
from PIL import Image
import numpy as np 
import os
from keras.models import load_model
import cv2
import PIL




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


 
    
paradict_numToEng = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
paradict_EngTonum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}


model = load_model('cnn_modelAll.h5')


CaseName = 1
Path = [os.path.join(os.getcwd(),'train_set'),os.path.join(os.getcwd(),'real_set')]
SaveName = ['train.csv','vail.csv']
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
#tData = np.stack([np.array(Image.open(index))/255.0 for index in vData])





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
    
data_ = np.stack(Res)
data = np.zeros((len(data_),50,80,1))
data[:,:,:,0] = data_


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
















