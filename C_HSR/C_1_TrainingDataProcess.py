import numpy as np
import PIL
import os


oPath = os.getcwd()
Path = os.path.join(oPath,'Training','0_Split')
folders = []
for ii in os.listdir(Path):
    if ii.find('_') == -1:
        folders.append(ii)


baseH = 50
digits = []
labels = []
for ii ,ff in enumerate(folders): 
    print(str(ii),'/',str(len(folders)))
    Files = os.listdir(os.path.join(Path,ff)) 
    for jj in Files:
        pil_image = PIL.Image.open(os.path.join(Path,ff,jj)).convert('1')
        baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
        img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS)
        digits.append([vv for vv in img.getdata()])
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
