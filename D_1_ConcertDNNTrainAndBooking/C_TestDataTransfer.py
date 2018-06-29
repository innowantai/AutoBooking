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
 
 
 

 
result = []
Pre_digits = []
Pre_labels = []

for ii in range(0,len(ans)):    
    path = []
    usToTest = []
    path = os.path.join(os.getcwd(),'0_Predict',"%02d" % ii)
    files = os.listdir(path) 
    for vv in files:        
        pil_image = PIL.Image.open(os.path.join(path,vv)).convert('1')        
        Pre_digits.append([vv for vv in pil_image.getdata()])
        Pre_labels.append(ii)     
        

Pre_digit_ary = np.array(Pre_digits)/255 
      
Lab = []
for ii in ans:
    for jj in ii:
        Lab.append(jj)
Lab = np.array(Lab)
   
 

print('The Figures Loading compeleted')
 
X_test = TransDatafromToCNN(Pre_digit_ary)
f1 = open('X_test_CNN.npy','wb')
np.save(f1,X_test)
f1.close()
 

f2 = open('Y_test.npy','bw')
np.save(f2,Lab) 
f2.close()

print('The Figures save completed')









