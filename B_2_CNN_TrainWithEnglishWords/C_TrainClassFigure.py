import os
import shutil
import csv


# =============================================================================
#  
# num = 6
# csvName = 'train_' + str(num) + '.csv'
# path = os.path.join(os.getcwd(),'train_set','Num' + str(num))
# csvPath = os.path.join(path,csvName)
# 
# DataCsv = open(csvPath, 'r', encoding = 'utf8')
# data = csv.reader(DataCsv)
# Lab = [ ii for ii in data]
# 
# files = os.listdir(path) 
# 
# for ii in Lab:
#     print(ii)
#     if os.path.exists(os.path.join(path,ii[0] + '_' + str(num) + '.jpg')):
#         os.rename(os.path.join(path,ii[0] + '_' + str(num) + '.jpg'),os.path.join(path,ii[0] + '_' + ii[1] + '.jpg')) 
# 
# =============================================================================

    
path1 = os.path.join(os.getcwd(),'train_set_ALL','Num6')

files = os.listdir(path1)

for kk, ff in enumerate(files):
    print(kk,'/',len(files))
    shutil.copy(os.path.join(path1,ff),os.path.join(os.getcwd(),'train_set_6'))

