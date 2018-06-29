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


def GerPredictFolders(prePath):
    files = os.listdir(os.path.join(os.getcwd(),'Predict',))
    result = [vv for vv in files if vv.find('.jpg') == -1]
    
    return result
            
def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,28,40))  
    for vv in range(Num):
        index = data[vv,:].reshape((33,50))
        index = index[3:-2,5:-5]
        Result[vv,:,:] = index
    return Result

def TranNumberToWords(paraDic1,data):
    res = []
    for ii in data:
        res.append( paraDic1[ii])
    re = [res]
    return np.array(res)
    

model = load_model('my_model_CNN_5000_2.h5')



paraDic1 = {0: '2', 1: '3', 2: '4', 3: '5', 4: '7', 5: '9', 6: 'A', 7: 'C', 8: 'F', 9: 'H', 10: 'K', 11: 'M', 12: 'N', 13: 'P', 14: 'Q', 15: 'R', 16: 'T', 17: 'Y', 18: 'Z'}
paraDic2 = {'2': 0, '3': 1, '4': 2, '5': 3, '7': 4, '9': 5, 'A': 6, 'C': 7, 'F': 8, 'H': 9, 'K': 10, 'M': 11, 'N': 12, 'P': 13, 'Q': 14, 'R': 15, 'T': 16, 'Y': 17, 'Z': 18}


ans_ = [['4P4Z'],['PR2M'],['C9Q2'],['CZMQ'],
       ['7FTF'],['F7Q4'],['KY2A'],['N744'],
       ['7Z37'],['Z72F'],['MYRF'],['4ARC'],
       ['Y2FA'],['9F37'],['R4A9'],['24H3'],
       ['43FY'],['NK97'],['93K4']]
       

ans = []
for ii in ans_: 
    res = []
    for jj in ii[0]:
        res.append(paraDic2[jj])
    ans.append(res)
 


prePath = os.path.join(os.getcwd(),'Predict')

folders = GerPredictFolders(prePath)

baseH = 50
res = []
Pre_labels = []

for ii, Name in enumerate(folders):    
    path = [] 
    Pre_digits = []
    path = os.path.join(os.getcwd(),'Predict',Name)
    files = os.listdir(path) 
    for jj , vv in enumerate(files): 
        pil_image = PIL.Image.open(os.path.join(path,vv)).convert('1')
        baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
        img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS) 
        Pre_digits.append([vv for vv in img.getdata()])
        Pre_labels.append(ii)    
    indexData = np.array(Pre_digits)/255
    Pre_digit_ary = TransDatafromToCNN(indexData) 
    Pre_digit_ary = Pre_digit_ary.reshape(-1, 1,28, 40)
    Res = TransResult(model.predict(Pre_digit_ary))
    res.append(Res) 


kk = 0
print('')
print('        識別結果','       原始驗證碼')
for ii , _ in enumerate(ans):
    Ans = np.array(ans[ii])
    Try = np.array(res[ii])
    cmp = Ans - Try
    test = cmp[cmp != 0]
    AnsWords = TranNumberToWords(paraDic1,Ans)
    TryWords = TranNumberToWords(paraDic1,Try)
    if len(test) != 0 :
        #print(ii,Try,Ans,' 總共有 ',str(len(test)),'數字錯誤 ==> ',Ans[cmp != 0])
        print(ii,TryWords,AnsWords,' 總共有 ',str(len(test)),'個錯誤 ==> ',AnsWords[cmp != 0])
    else:
        kk += 1
        #print(ii,Try,Ans,'        ok ')
        print(ii,TryWords,AnsWords,'        ok ')
print('Result : ',str(kk),'/',str(len(ans)),' ==> ','%.1f' % (kk/(len(ans))*100) ,'%')

