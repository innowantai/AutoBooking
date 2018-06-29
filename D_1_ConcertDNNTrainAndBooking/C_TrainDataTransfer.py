import numpy as np
import PIL
import os






def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,33,50))  
    for vv in range(Num):
        index = data[vv,:].reshape((33,50)) 
        Result[vv,:,:] = index
    return Result





fileFolder = '0_Classify'



paradict_numToEng = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
paradict_EngTonum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}


oPath = os.getcwd()
filePath = os.path.join(oPath,fileFolder)

Folders = os.listdir(filePath)
 

## Get all FileNumber to calculate progress
AllFilesNum = 0
for ii in Folders:
    num = len(os.listdir(os.path.join(oPath,fileFolder,ii)))
    AllFilesNum += num
 
 
    
    
     
digits = []
labels = []
kk = 0
for ii in Folders:
    Path = os.path.join(filePath,str(ii))
    Files = os.listdir(Path) 
    for nn,jj in enumerate(Files): 
        kk += 1
        print('\rProcess : ' + '%0.1f' % (kk/AllFilesNum*100) + '%, ' + str(kk) + '/' + str(AllFilesNum) ,end = '') 
        #print('Process : ' + '%0.1f' % (kk/AllFilesNum*100) + '%, ' + str(kk) + '/' + str(AllFilesNum) ) 
        pil_image = PIL.Image.open(os.path.join(Path,jj)).convert('1') 
        digits.append([vv for vv in pil_image.getdata()])
        labels.append(paradict_EngTonum[ii])  
digit_ary = np.array(digits) / 255
Lab = np.array(labels)


print('\nThe Figures Loading compeleted')
 
X_Train = TransDatafromToCNN(digit_ary)
f1 = open('X_Training_CNN.npy','wb')
np.save(f1,X_Train)
f1.close()
 

f2 = open('Y_Training.npy','bw')
np.save(f2,Lab) 
f2.close()

print('The Figures save completed')










