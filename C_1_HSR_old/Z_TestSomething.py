






def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,33,50))  
    Result = np.zeros((Num,33-5,50-10)) 
    for vv in range(Num):
        index = data[vv,:].reshape((33,50))
        index = index[3:-2,5:-5]
        Result[vv,:,:] = index
    return Result


def TransResult(result): 
    Res = []
    for vv in result.tolist():
        Res.append(vv.index(max(vv))) 
    return Res


 
Path = os.path.join(os.getcwd(),'0_OnlineIndexo')
Files_ = os.listdir(Path)
Files = []
for ff in Files_:
    if ff.find('.jpg') != -1:
        Files.append(ff)  
        
digits = []   
for ii,jj in enumerate(Files): 
    pil_image = PIL.Image.open(os.path.join(Path,jj)).convert('1') 
    img = pil_image.resize((50,33),PIL.Image.ANTIALIAS)
    digits.append([vv for vv in img.getdata()])
digit_ary = np.array(digits) / 255 

# Translate the figure of np.array to CNN format

X_Test = TransDatafromToCNN(digit_ary)
X_Test = X_Test.reshape(-1, 1,28, 40) 
Res = TransResult(model.predict(X_Test))

res = ''
for ii in Res:
    folder = paraDic1[ii]
    res += folder