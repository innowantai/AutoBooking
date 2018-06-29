import os





folder = '1_AutoClass'



files = os.listdir(folder)


Name = [ff for ff in files if ff.split('_')[1].split('.')[0].isdigit()]


kk = 1
for ff in Name:
    print('\r ' + str(kk),end = '')
    os.remove(os.path.join(os.getcwd(),folder,ff)) 
    kk += 1
