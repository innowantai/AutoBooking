import cv2
import PIL
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import shutil


###### This code is to Predict the figure's number by training model and classify to correspon folder to building data base




path = os.path.join(os.getcwd(),'Classify','0_SplitedFigures')
files = os.listdir(path)
 

for ii in range(10):
    try:
        os.mkdir(os.path.join(path,str(ii)))
    except:
        pass
    

    
kk = 0

Pre_digits = []
Pre_labels = []   
for ii,vv in enumerate(files):  
    if ii % 100 == 0:
        print(ii,len(files))        
    if vv.find('jpg') != -1:          
        kk += 1
        
        pil_image = PIL.Image.open(os.path.join(path,vv)).convert('1')         
        baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
        img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS)
        Pre_digits.append([vv for vv in img.getdata()])
        Pre_labels.append(vv)
        
        
        
Pre_digit_ary = np.array(Pre_digits)
scaler = StandardScaler()
scaler.fit(Pre_digit_ary)
x_scaled = scaler.transform(Pre_digit_ary)
pre = mlp.predict(x_scaled)

        
          
        
        
pre = pre.tolist()
for ii, v in enumerate(Pre_labels):    
    shutil.copy(os.path.join(path,v),os.path.join(path,str(pre[ii])))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    