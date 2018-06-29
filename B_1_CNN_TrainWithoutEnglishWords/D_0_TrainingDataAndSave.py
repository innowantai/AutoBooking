import numpy as np
import PIL
import os


oPath = os.getcwd()

## Get all FileNumber to calculate progress
AllFilesNum = 0
for ii in range(10):
    num = len(os.listdir(os.path.join(oPath,'ProcessData',str(ii))))
    AllFilesNum += num


 

baseH = 50
digits = []
labels = []
kk = 0
for ii in range(10):
    Path = os.path.join(oPath,'ProcessData',str(ii))
    Files = os.listdir(Path) 
    for nn,jj in enumerate(Files): 
        kk += 1
        print('\rProcess : ' + '%0.3f' % (kk/AllFilesNum*100) + '%, ' + str(kk) + '/' + str(AllFilesNum) ,end = '')
        #print('\rProcess : ' + str(ii) + ' - ' + str(nn) + '/' + str(len(Files)),end = '')
        pil_image = PIL.Image.open(os.path.join(Path,jj)).convert('1') 
        digits.append([vv for vv in pil_image.getdata()])
        labels.append(ii) 
digit_ary = np.array(digits) / 255
Lab = np.array(labels)


print('The Figures Loading compeleted')

f1 = open('X_Training.npy','bw')
f2 = open('Y_Training.npy','bw')
np.save(f1,digit_ary)
np.save(f2,Lab) 
f1.close()
f2.close()

print('The Figures save completed')
