import os
import shutil


path = os.path.join(os.getcwd(),'1_AutoClass')
 


files = os.listdir(path)

for ii,ff in enumerate(files):
    print(ii,len(files))
    index = ff.split('_')[1].split('.')[0]
    if len(index) == 5:
        shutil.copy(os.path.join(path,ff),os.path.join(os.getcwd(),'train_set_5'))
    elif len(index) == 6: 
        shutil.copy(os.path.join(path,ff),os.path.join(os.getcwd(),'train_set_6'))
        