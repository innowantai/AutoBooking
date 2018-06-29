import cv2
import PIL
import numpy as np
import matplotlib.pyplot as plt
import os

def DeNoise(img):    
    for i in range(10):
        img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)         
    return img

def DeNoise_gray(thresh,control):
    test = PIL.Image.fromarray(thresh.astype('uint8'), 'L')
    de = cv2.fastNlMeansDenoising(np.array(test),None,control,7,21)   
    de[de > 0] = 255
    return de


def DeNoise_UseDefine(thresh,nn): 
    for ii in range(nn,thresh.shape[0]):
        for jj in range(nn,thresh.shape[1]):
            index = thresh[ii-nn:ii+nn+1,jj-nn:jj+nn+1]
            if index[nn,nn] == 0:
                index2 = np.copy(index)
                index2[:,nn] = 255
                index2[nn,:] = 255
                if len(index2[index2==0]) == 0:
                    index[nn,:] = 255
                    index[:,nn] = 255
    return thresh


def DeNoise_UseDefineSignal(thresh,nn): 
    for ii in range(nn,thresh.shape[0]):
        for jj in range(nn,thresh.shape[1]):
            index = thresh[ii-nn:ii+nn+1,jj-nn:jj+nn+1]
            if index[nn,nn] == 0:
                index2 = np.copy(index)   
                if len(index2[index2==0]) == 1:
                    index[nn,nn] = 255  
    return thresh

def ConnectTwoSideNumber(thresh):    
                                                                                #### Connecting splited number         
                                                                                #### Contain Vertical and Horizontal Part    
    nn = 1
    for ii in range(nn,thresh.shape[0]-nn):
        for jj in range(nn,thresh.shape[1]-nn):
            index = thresh[ii - nn : ii + nn + 1,jj - nn : jj + nn + 1]   
            if np.mean(index[:,1]) == 255 :                                     #### Vertial
                test1 = index[:,0]
                test2 = index[:,2]
                if len(test1[test1 == 0]) >=2 and len(test2[test2==0]) >= 2:
                    index[nn,nn] = 0    
                     
            if np.mean(index[1,:]) == 255 :                                     #### Horizon
                test3 = index[0,:]
                test4 = index[2,:]
                if len(test3[test3 == 0]) >=2 and len(test4[test4==0]) >= 2:
                    index[nn,nn] = 0 
    return thresh
    

def TransferColorAndTakeOffBoundNoise(thresh):    
    thresh[thresh == 0] = 254                                                   #### Transfer Color
    thresh[thresh == 255]= 0
    thresh[thresh == 254] = 255      
    thresh[:,20] = 255                                                          #### Take Off Boundaried Noise
    thresh[-10:,:] = 255
    thresh[:10:,:] = 255
    return thresh


######## 此函數為尋找 x方向所有數字區間                         
def findBoundary(m):    
    po = []
    for i in range(len(m)-1):
        if m[i+1] - m[i] < 0:
            po.append(i+1)
        elif m[i+1] - m[i] > 0:
            po.append(i)
            
    for ii in range(1,len(po)-1,2):
        if po[ii+1] - po[ii] <= 2:
            po[ii] = 0
            po[ii+1] = 0
        
    po2 = []
    for ii in po:
        if ii != 0:
            po2.append(ii)
            
    if len(po2) % 2 == 1:
        if m[0] == 0:
            po2 = [0] + po2
        elif m[-1] == 0:
            po2.append(len(m)-1) 
    return po2 


######## This function is to find most continued of figure for y-axis  
######## 此函數為尋找 y方向之最長連續段數字                              
def diffAndCatching(data):
    dif = []
    for ii in range(1,len(data),2):
        dif.append(data[ii]-data[ii-1]) 
    po = []
    position = dif.index(max(dif)) 
    po.append(data[2*position])
    po.append(data[2*position+1])
    return po
####################################################################

 
def SpliterImgAndProcessDone(thresh):
    ######## This part is to splite figure that step show below
    ######## step 1 : Projecting number to x-axis, the result will show 255(None) or 0(have figure)    
    lis = [min(vv) for vv in thresh.T.tolist()]
    po = findBoundary(lis)                 
    fig1 = []
    for ii in range(0,len(po),2):
        if po[ii+1] - po[ii] >= 4:                   #### Catching width enough figure                               
            index = thresh[:,po[ii]:po[ii+1]]
            fig1.append(index)           
    
    fig2 = []
    for ff in fig1:
        lis = [min(vv) for vv in ff.tolist()]
        po = findBoundary(lis) 
        po2 = diffAndCatching(po)
        resultFF = ff[po2[0]:po2[1]+1,:]     
        if resultFF.shape[1] >= 10:                 #### Catching width enough figure
            fig2.append(resultFF)
    
    fig4 = []
    for kk,ff in enumerate(fig2):
        lis = [min(vv) for vv in ff.T.tolist()]
        po = findBoundary(lis)
        
        if po != [] and (min(ff[:,0]) != 0 or min(ff[:,ff.shape[1]-1]) != 0):
            if po[0] <= ff.shape[1]/2:
                ff = ff[:,po[0]:]
            else:
                ff = ff[:,:po[0]]  
            
        if ff.shape[1] >= 23:
            ss = int(np.floor(ff.shape[1]/2))
            ff1 = ff[:,:ss]
            ff2 = ff[:,ss:]
            fig4.append(ff1)
            fig4.append(ff2)
        else:
            fig4.append(ff)
    
    fig5 = [] 
    for ii,ff in enumerate(fig4):      
        lis = [min(vv) for vv in ff.tolist()]    
        po = findBoundary(lis) 
        if po != [] and (lis[0] != 0 or lis[-1] != 0):        
            po2 = diffAndCatching(po)
            resultFF = ff[po2[0]:po2[1],:]     
            if resultFF.shape[1] >= 10:                 #### Catching width enough figure
                fig5.append(resultFF)                
        else:      
            fig5.append(ff)  

    return fig5



 
def MainProcess(fileName,OriName):     
    FilePaeh = os.path.join(os.getcwd(),fileName) 
    SavePath = OriName
    
    if not os.path.exists(SavePath):
        os.mkdir(SavePath)
    
    files = os.listdir(SavePath)
    for ff in files:
        os.remove(os.path.join(SavePath,ff))    
    
    
    
    img = PIL.Image.open(FilePaeh).convert('RGB')
    open_cv_img = np.array(img) 
    img_gray = cv2.cvtColor(open_cv_img,cv2.COLOR_BGR2GRAY)
    
    
    img_gray[img_gray > 110] = 0
    _, thresh = cv2.threshold(img_gray,0,255,0)
    
    
    thresh = TransferColorAndTakeOffBoundNoise(thresh)
    thresh = DeNoise_UseDefine(thresh,2)
    thresh = DeNoise_UseDefineSignal(thresh,1)   
    thresh = ConnectTwoSideNumber(thresh)
    
    fig5 = []
    fig5 = SpliterImgAndProcessDone(thresh)
     
# =============================================================================
#     AllTest = [] 
#     for kk ,ff in enumerate(fig5): 
#         ii = str(int(np.random.random(1)*100000))
#         ii2 = str(int(np.random.random(1)*100000))
#         test1 = PIL.Image.fromarray(ff).resize((50,33))
#         AllTest.append(test1) 
#         test1.save(SavePath + '\\' +  str(kk) + '_' + ii + '_' + ii2 + '.jpg')
# =============================================================================
 
        
    return len(fig5)
    
    







# =============================================================================
# def MainProcess(fileName):     
#     FilePaeh = os.path.join(os.getcwd(),fileName)
#     SavePath = os.path.join(os.getcwd(),'0_OnlineIndex')
#     
#     
#     if not os.path.exists(SavePath):
#         os.mkdir(SavePath)
#     
#     files = os.listdir(SavePath)
#     for ff in files:
#         os.remove(os.path.join(SavePath,ff))    
#     
#     
#     
#     img = PIL.Image.open(FilePaeh).convert('RGB')
#     open_cv_img = np.array(img) 
#     img_gray = cv2.cvtColor(open_cv_img,cv2.COLOR_BGR2GRAY)
#     
#     
#     img_gray[img_gray > 110] = 0
#     _, thresh = cv2.threshold(img_gray,0,255,0)
#     
#     
#     thresh = TransferColorAndTakeOffBoundNoise(thresh)
#     thresh = DeNoise_UseDefine(thresh,2)
#     thresh = DeNoise_UseDefineSignal(thresh,1)   
#     thresh = ConnectTwoSideNumber(thresh)
#     
#     fig5 = []
#     fig5 = SpliterImgAndProcessDone(thresh)
#      
#     
#     for kk ,ff in enumerate(fig5): 
#         plt.figure(figsize=(6,4), dpi = 100)
#         plt.imshow(ff) 
#         plt.savefig(SavePath + '\\' +  str(kk) + '.jpg',dpi=100)
#     plt.close('all')
# =============================================================================








