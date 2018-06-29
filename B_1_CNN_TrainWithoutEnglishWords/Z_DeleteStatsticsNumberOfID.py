import os


path = './1_AutoClass'
files = os.listdir(path)

 
for ff in files:
    ff = ff.split('_')[1].split('.')[0]
    if len(ff) == 5:
        kk1 += 1
    else:
        kk2 += 1