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
    files = os.listdir(os.path.join(os.getcwd(),'Predict',))
    result = [vv for vv in files if vv.find('.jpg') == -1]
    
    return result
            


model = load_model('my_model_CNN2.h5')



ans = [[0,2,6,6,7,5],[0,6,1,8,9,2],[0,3,7,9,9,4],[0,5,2,8,8,0],
       [7,5,9,3,4,3],[8,3,7,1,0,4],[2,9,4,8,4,4],[4,2,5,7,2,8],
       [1,6,8,3,7,8],[1,3,8,7,2,2],[1,8,7,7,1,6],[3,6,4,0,5,5],
       [6,1,3,6,8,8],[3,0,2,8,2  ],[6,5,3,0,2,8],[0,1,7,7,8  ],
       [5,8,5,9,4,8],[1,4,0,4,1  ],[2,1,5,2,2,2],[8,1,7,3,1,4],
       [4,8,0,7,8,2]]


# =============================================================================
# ,[4,0,9,1,8,7],[2,5,8,6,4,7],[4,3,9,3,2,9],
#        [3,4,5,7,8,1],[5,6,3,5,5  ],[7,1,6,2,4  ],[0,7,4,8,0,5],
#        [7,2,8,4,5,3],[4,7,5,8,5,9],[0,4,6,7,4,9],[3,5,0,2,2,3],
#        [0,2,4,8,0,1],[7,0,5,5,2,8],[5,4,9,1,6,7],[4,1,2,1,6,0],
#        [7,4,4,3,6,5],[1,0,2,2,7,5],[0,2,8,7,2,3],[2,4,5,4,7,6],
#        [8,3,9,1,6  ],[6,2,8,8,7,8],[9,6,0,7,5,3],[9,2,7,9,2  ],
#        [0,6,5,5,0,8],[5,1,9,6,7  ],[7,7,6,4,3,2],[7,7,8,5,8,0],
#        [4,6,1,5,3,5],[1,8,7,7,2,1],[9,5,2,2,4  ],[6,4,6,3,5,0],
#        [2,2,5,4,6,5],[6,1,3,6,8,6],[5,4,0,9,7,1],[0,6,5,5,1,2],
#        [3,9,0,7,5,2],[3,7,5,0,6  ],[6,9,2,2,7,1],[6,9,1,3,6,2],]
# =============================================================================
       






prePath = os.path.join(os.getcwd(),'Predict')

folders = GerPredictFolders(prePath)
 
res = []
Pre_labels = []

for ii, Name in enumerate(folders):    
    path = [] 
    Pre_digits = []
    path = os.path.join(os.getcwd(),'Predict',Name)
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


kk = 0
print('')
print('    識別結果','     原始驗證碼')
for ii , _ in enumerate(ans):
    Ans = np.array(ans[ii])
    Try = np.array(res[ii])
    cmp = Ans - Try
    test = cmp[cmp != 0]
    if len(test) != 0 :
        print(ii,Try,Ans,' 總共有 ',str(len(test)),'數字錯誤 ==> ',Ans[cmp != 0])
    else:
        kk += 1
        print(ii,Try,Ans,'        ok ')
print('Result : ',str(kk),'/',str(len(ans)),' ==> ','%.1f' % (kk/(len(ans))*100) ,'%')

