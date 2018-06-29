import os



path = os.path.join(os.getcwd(),'Training')
savePath = os.path.join(path,'0_Split')


Name = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for ii in Name:
    pathFolder = os.path.join(savePath,ii)
    if not os.path.exists(pathFolder):
        os.mkdir(pathFolder) 