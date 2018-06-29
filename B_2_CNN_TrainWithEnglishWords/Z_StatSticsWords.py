import os




Number = 6
folder = './train_set_' + str(Number)
files = os.listdir(folder)

Words = [ff.split('_')[1].split('.')[0] for ff in files if ff.find('.jpg') != -1]

kk = 0
for ww in Words:
    if ww.isdigit():
        kk += 1
print('Total Number = ', kk , 'Vocabulary Number = ' ,len(Words) - kk)