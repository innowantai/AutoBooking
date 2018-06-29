import os






folderName = '0_Classify'
path = os.path.join(os.getcwd(),folderName)

folders = os.listdir(path)

nn = 0
for ff in folders:
    files = os.listdir(os.path.join(path,ff))
    print(ff,' : ',len(files))
    nn += len(files)


