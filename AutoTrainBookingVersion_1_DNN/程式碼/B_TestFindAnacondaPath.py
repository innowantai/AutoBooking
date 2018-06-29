import os



oriPath = 'C:\\'
#oriPath = os.getcwd()

folder = os.listdir(oriPath)

for ii,ff in enumerate(os.walk(oriPath)): 
    if ff[0].find('Anaconda') != -1:
        MovePath = ff[0]
        break