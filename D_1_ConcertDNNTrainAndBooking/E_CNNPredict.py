import PIL 
import matplotlib.pyplot as plt
import os 
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


def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,33,50))  
    for vv in range(Num):
        index = data[vv,:].reshape((33,50))
        #index = index[1:,3:-3]
        Result[vv,:,:] = index
    return Result


def GerPredictFolders(prePath):
    files = os.listdir(os.path.join(os.getcwd(),'0_Predict',))
    result = [vv for vv in files if vv.find('.jpg') == -1]
    
    return result
            


model = load_model('my_model_CNN2.h5')


paradict_numToEng = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
paradict_EngTonum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}





ans_ = [['woue'],['qufe'],['pumi'],['kugc'],
       ['toma'],['ciya'],['nika'],['oexu'],
       ['voae'],['guwe'],['xilf'],['waoa'],
       ['xsre'],['uaeo'],['sdyt'],]
 


ans = []
for ii in ans_: 
    res = []
    for jj in ii[0]:
        res.append(paradict_EngTonum[jj])
    ans.append(res)


prePath = os.path.join(os.getcwd(),'0_Predict')

folders = GerPredictFolders(prePath)
 
res = []
Pre_labels = []

for ii, Name in enumerate(folders):    
    path = [] 
    Pre_digits = []
    path = os.path.join(os.getcwd(),'0_Predict',Name)
    files = os.listdir(path) 
    for jj , vv in enumerate(files): 
        pil_image = PIL.Image.open(os.path.join(path,vv)).convert('1')        
        Pre_digits.append([vv for vv in pil_image.getdata()])
        Pre_labels.append(ii)    
    indexData = np.array(Pre_digits)/255
    Pre_digit_ary = TransDatafromToCNN(indexData) 
    Pre_digit_ary = Pre_digit_ary.reshape(-1, 1,33, 50)
    Res = TransResult(model.predict(Pre_digit_ary))
    res.append(Res) 



def TranlferNumToEng(data,paradict_numToEng):
    res = '[ '
    for ii in data: 
        res += paradict_numToEng[ii] + ' '
    res += ' ]'
    return res

kk = 0
print('')
print('    識別結果','     原始驗證碼')
for ii , _ in enumerate(ans):
    Ans = np.array(ans[ii])
    Try = np.array(res[ii])
    cmp = Ans - Try
    test = cmp[cmp != 0]
    if len(test) != 0 :
        print(ii,TranlferNumToEng(Try,paradict_numToEng),TranlferNumToEng(Ans,paradict_numToEng),' 總共有 ',str(len(test)),'字母錯誤 ==> ',TranlferNumToEng(Ans[cmp != 0],paradict_numToEng))
    else:
        kk += 1
        print(ii,TranlferNumToEng(Try,paradict_numToEng),TranlferNumToEng(Ans,paradict_numToEng),'        ok ')
print('Result : ',str(kk),'/',str(len(ans)),' ==> ','%.1f' % (kk/(len(ans))*100) ,'%')

