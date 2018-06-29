import cv2
import PIL
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

ans = [[0,2,6,6,7,5],[0,6,1,8,9,2],[0,3,7,9,9,4],[0,5,2,8,8,0],
       [7,5,9,3,4,3],[8,3,7,1,0,4],[2,9,4,8,4,4],[4,2,5,7,2,8],
       [1,6,8,3,7,8],[1,3,8,7,2,2],[1,8,7,7,1,6],[3,6,4,0,5,5],
       [6,1,3,6,8,8],[3,0,2,8,2  ],[6,5,3,0,2,8],[0,1,7,7,8],
       [5,8,5,9,4,8],[1,4,0,4,1],[2,1,5,2,2,2],[8,1,7,3,1,4],
       [4,8,0,7,8,2]]
 
result = []
for ii in range(0,len(ans)):    
    Pre_digits = []
    Pre_labels = []
    path = []
    path = os.path.join(os.getcwd(),'Predict',str(ii))
    files = os.listdir(path)
    for vv in files:        
        pil_image = PIL.Image.open(os.path.join(path,vv)).convert('1')
        baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
        img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS)
        Pre_digits.append([vv for vv in img.getdata()])
        Pre_labels.append(ii)     
        Pre_digit_ary = np.array(Pre_digits)
        scaler = StandardScaler()
        scaler.fit(Pre_digit_ary)
        x_scaled = scaler.transform(Pre_digit_ary)
        pre = mlp.predict(x_scaled)
    result.append(pre)
    
     
print('     識別結果','     原始驗證碼')
kk = 0
for ii, rr in enumerate(result):
    ori = np.array(ans[ii])
    cmp = rr-ori
    cm = len(cmp) - len(cmp[cmp == 0])
    if cm == 0:
        print(ii,rr,np.array(ans[ii]),'ok' ) 
        kk += 1
    else:
        err = ori[cmp != 0]
        print(ii,rr,np.array(ans[ii]),cm,'個數字錯誤 = ', err.tolist() )
        
print('Reults : ', str(kk),'/',str(len(result)))