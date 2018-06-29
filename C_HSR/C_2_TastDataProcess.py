import PIL
import numpy as np
import matplotlib.pyplot as plt
import os 



oPath = os.getcwd()
Path = os.path.join(oPath,'Training','0_Split')
folders = []
kk = 0
dic = dict()
for ii in os.listdir(Path):
    if ii.find('_') == -1:
        dic[ii] = kk
        folders.append(ii)
        kk += 1

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
 

baseH = 50
result = []
Pre_digits = []
Pre_labels = []

for ii in range(0,len(ans)):    
    path = []
    usToTest = []
    path = os.path.join(os.getcwd(),'Predict',"%02d" % ii)
    files = os.listdir(path) 
    for vv in files:        
        pil_image = PIL.Image.open(os.path.join(path,vv)).convert('1')
        baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
        img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS)
        Pre_digits.append([vv for vv in img.getdata()])
        Pre_labels.append(ii)     

Pre_digit_ary = np.array(Pre_digits)/255 
      
Lab = []
for ii in ans:
    for jj in ii:
        Lab.append(jj)
Lab = np.array(Lab)
 


f1 = open('X_test.npy','wb')
f2 = open('Y_test.npy','wb') 
np.save(f1,Pre_digit_ary)
np.save(f2,Lab) 
f1.close()
f2.close()
