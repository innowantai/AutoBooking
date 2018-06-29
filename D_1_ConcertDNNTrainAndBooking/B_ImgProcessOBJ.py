from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import PIL 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import math
import time
 

def A_1_SearchBounded(InputImg,StartX):        
    flag = 0
    #Slop = [0,1,2,3,4,5,6,7,8,9,10,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
    for slop in range(-10,10):    
        newImg = np.copy(InputImg)
        if slop != 0 :
            y = np.arange(0,newImg.shape[0])
            x = y / slop         
            x2 = []
            for ii in x:
                if math.modf(ii)[0] == 0    :
                    x2.append(int(ii))
            x2 = np.array(x2) 
            y2 = newImg.shape[0] - x2*slop - 1
            x2 = x2 + StartX
        else:        
            y2 = newImg.shape[0] - np.arange(0,newImg.shape[0]) - 1
            x2 = np.ones(len(y2), dtype = np. int) * StartX         
        
        test = np.column_stack([x2,y2])
        index0 = []
        for ele in test:
            if ele[0] < newImg.shape[1] and ele[0] > 0:                
                index0.append(newImg[ele[1],ele[0]])
                
        xx2 = []
        yy2 = []
        for ii in range(len(test)-1):
            indexX = test[ii][0]
            indexY = test[ii][1]
            indexY2 = test[ii+1][1]
            for jj in range(indexY,indexY2,-1):
                xx2.append(indexX)
                yy2.append(jj)
        if indexY2 != 0:
            for jj in range(indexY2,0,-1):
                xx2.append(indexX)
                yy2.append(jj)                
        NewTest = np.column_stack([xx2,yy2])
        index = []
        for ele in NewTest: 
            #print(ele,newImg.shape[1])
            if abs(ele[0]) < newImg.shape[1] : # and ele[0] > 0:                 
                index.append(newImg[ele[1],ele[0]])
                newImg[ele[1],ele[0]] = 0
        
        index = np.array(index)
        if len(index[index == 0]) <  1 and min(index0) == 255: #int(newImg.shape[0]/10)  :
            flag = 1  
            break  
    return flag, test, slop
        
def A_1_SplitFigureAfterSearchBounded(InputImg,test):
    xx2 = []
    yy2 = []
    for ii in range(len(test)-1):
        indexX = test[ii][0]
        indexY = test[ii][1]
        indexY2 = test[ii+1][1]
        for jj in range(indexY,indexY2,-1):
            xx2.append(indexX)
            yy2.append(jj)
    if indexY2 != 0:
        for jj in range(indexY2,0,-1):
            xx2.append(indexX)
            yy2.append(jj)
            
    takeOff = np.column_stack([xx2,yy2])
    CatchFig = np.copy(InputImg)
    for ele in takeOff:
        if ele[0] < CatchFig.shape[1]:             
            CatchFig[ele[1],ele[0]:] = 255
            
    ResiFig = np.copy(InputImg)
    for ele in takeOff:
        if ele[0] < ResiFig.shape[1]:             
            ResiFig[ele[1],0:ele[0]+1] = 255 
             
            
    return CatchFig,ResiFig
    
    
   
    
def A_0_TakeOffBounded(thresh,ll,rr,uu,dd):
    for ii in range(0,thresh.shape[0]):
        if min(thresh[ii,:]) == 0:
            po1 = ii - ll
            if po1 < 0:
                po1 = ii
            break    
    for ii in range(thresh.shape[0]-1,0,-1): 
        if min(thresh[ii,:]) == 0:
            po2 = ii + rr
            if po2 < 0:
                po2 = ii
            break   
    for ii in range(0,thresh.shape[1]):
        if min(thresh[:,ii]) == 0:
            po3 = ii - uu
            if po3 < 0:
                po3 = ii
            break    
    for ii in range(thresh.shape[1]-1,0,-1): 
        if min(thresh[:,ii]) == 0:
            po4 = ii + dd
            if po4 < 0:
                po4 = ii
            break    
    newImg = np.copy(thresh[po1:po2,po3:po4]) 
    return newImg 






def A_0_ImgProcess(filePath):
    # Load figure and translat to gray pixels
    img = PIL.Image.open(filePath).convert('RGB')
    # transfer to np.array format
    open_cv_img = np.array(img) 
    img_gray = cv2.cvtColor(open_cv_img,cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray,230,255,1)     
    thresh[0:5,:] = 255
    newImg = A_0_TakeOffBounded(thresh,4,4,4,4)
    return newImg

def A_1_SpliteFigure(InputImg):
    newImg = np.copy(InputImg)
    # Because Using Slop to scan and Splite of the figue that may have a problem at bounded, so let rightest bounded equl 0 before scan
    newImg[:,-1] = 0
    newImg[:,0] = 0
    InputImg = np.copy(newImg)  
    AllCatch = []
    AllX2 = []
    for StartX in range(1,InputImg.shape[1]):
        flag , test ,slop= A_1_SearchBounded(InputImg,StartX)  
            
        if flag != 0:          
            CatchFig, InputImg =  A_1_SplitFigureAfterSearchBounded(InputImg,test) 
            CatchFig[:,0] = 255
            CatchFig[:,-1] = 255
            if len(CatchFig[CatchFig == 0]) > 2 : 
                AllCatch.append(A_0_TakeOffBounded(CatchFig,0,0,0,2))
                AllX2.append(slop)      
    # It may have error-judge when scan closed to right bounded at decrease-slop 
    InputImg[:,-1] = 255
    InputImg[:,0] = 255
    if len(InputImg[InputImg == 0]) > 10 :
        AllX2.append(StartX)
        AllCatch.append(A_0_TakeOffBounded(InputImg,0,0,0,2))
    
    return AllCatch,AllX2


def A_2_SplitSubFigurePath(InputImg,stX):
    index = np.copy(InputImg)
    stY = index.shape[0] - 1
    openFlag = 1  
    CatchFlag = 0 
    pathY = []
    pathX = [] 
    tick = 0
    while openFlag == 1:   
        if stX + 1 != index.shape[1]:
            dirction = [index[stY,stX-1],index[stY-1,stX],index[stY,stX+1]]
        else:
            dirction = [index[stY,stX-1],index[stY-1,stX],0]            
        #print(dirction,stY,stX)
        pathY.append(stY)
        pathX.append(stX)
        #print(stY,stX,dirction)    
        if  stY == 0 :
            openFlag = 0 
            CatchFlag = 1        
            
        if dirction[1] != 0:
            stY = stY - 1            
        elif dirction[0] != 0 and dirction[2] == 0:
            stX = stX - 1
        elif dirction[2] != 0 and dirction[1] == 0:
            stX = stX + 1
        tick += 1
        if tick >= index.shape[0]*3 or stX < 0 :
            openFlag = 0
            CatchFlag = 0
            
        takeOff = np.column_stack([pathX,pathY])
    return CatchFlag,takeOff    

def A_2_SplitSubFigureByPath(InputImg,takeOff): 
    CatchFig = np.copy(InputImg)
    for ele in takeOff:             
        if ele[0] < CatchFig.shape[1]: 
            CatchFig[ele[1],ele[0]:] = 255
    
    ResiFig = np.copy(InputImg)
    for ele in takeOff:
        if ele[0] < ResiFig.shape[1]:             
            ResiFig[ele[1],0:ele[0]+1] = 255
    return CatchFig, ResiFig

def A_2_SplitSubFigure(InputImg,CatNum):
    ResiFig = np.copy(InputImg)
    SubFigure = []
    for stX in range(ResiFig.shape[1]-1):
        index = ResiFig[:,stX]
        if min(index) == 0:          
            CatchFlag, takeOff = A_2_SplitSubFigurePath(ResiFig,stX)
            if CatchFlag == 1:
               # print(stX)  
                CatchFig, ResiFig = A_2_SplitSubFigureByPath(ResiFig,takeOff)
                if len(CatchFig[CatchFig == 0]) != 0:
                    SubFigure.append(CatchFig)            
        if len(SubFigure) == CatNum:
            break
    return SubFigure

def A_3_SplitProcessing2(AllCatch):
    TotalNum = 4
    CatNum = TotalNum - len(AllCatch) + 1
    AllSize = [ii.shape[1] for ii in AllCatch]     
    IndexFig = [0,1,2,3]  
    AllFig = [] 
    CaseName = 0
    if len(AllSize) == 3:
        CaseName = 1
        CatIndex = AllSize.index(max(AllSize))
        IndexFig.remove(CatIndex)
        IndexFig.remove(CatIndex+1)
        for ii in range(len(AllSize)):
            if ii != CatIndex:
                AllFig.append(AllCatch[ii])   
    elif len(AllSize) == 2:
        if np.abs(AllSize[1] - AllSize[0]) > 15 : 
            CaseName = 2
            CatIndex = AllSize.index(max(AllSize))        
            IndexFig.remove(CatIndex)
            IndexFig.remove(CatIndex+1)
            IndexFig.remove(CatIndex+2)
            if CatIndex == 0:
                AllFig.append(AllCatch[1])
            else:
                AllFig.append(AllCatch[0])
        else: 
            CaseName = 3 
            CatIndex = [0,1] 
             
             
    if CaseName == 1 or CaseName == 2:
        index = AllCatch[CatIndex]
        SubFigure = A_2_SplitSubFigure(index,CatNum) 
        
        if len(SubFigure) != CatNum:
            span = int(index.shape[1] / CatNum)
            SubFigure = []
            for kk in range(CatNum):
                index2 = np.copy(index[:,0+span*(kk) :span+span*(kk)])
                SubFigure.append(index2)
                
        for ii,ff in enumerate(SubFigure):
            IndexFig.append(CatIndex + ii)
            AllFig.append(ff)
        
        IndexFig = np.array(IndexFig)
        AllFig2 = []
        for ii in range(4):
            po = np.where(IndexFig == ii)[0][0] 
            AllFig2.append(AllFig[po]) 
            
        AllFig = AllFig2   
        
    elif CaseName == 3:
        AllFig = []
        CatNum = 2
        for ii in CatIndex:
            index = AllCatch[ii]
            SubFigure = A_2_SplitSubFigure(index,CatNum) 
            
            if len(SubFigure) != CatNum:
                span = int(index.shape[1] / CatNum)
                SubFigure = []
                for kk in range(CatNum):
                    index2 = np.copy(index[:,0+span*(kk) :span+span*(kk)])
                    AllFig.append(index2)
            else:
                for ff in SubFigure:
                    AllFig.append(ff)
        
    elif CaseName == 0:
        AllFig = AllCatch
        
        
        
        
    AllResult = []
    for ff in AllFig:
        index = A_0_TakeOffBounded(ff,0,0,4,7)
        AllResult.append(index)
    # =============================================================================
    #     plt.figure()
    #     plt.imshow(index)
    # =============================================================================
    
    return AllResult





def A_IMGProcess(filePath,SavePath):
    
    files = os.listdir(SavePath)
    if len(files) != 0:
        for ff in files:
            os.remove(os.path.join(SavePath,ff))
    
    
    newImg = A_0_ImgProcess(filePath)
    # Step 2 : Splie To sub Figure
    AllCatch,Allx2 = A_1_SpliteFigure(newImg)  
    # Step 3 : Statstics Figure prepare to re-split
    Result =  A_3_SplitProcessing2(AllCatch)
    files = []
    for ii,ff in enumerate(Result):
        jj = int(np.random.random(1)*10000)
        jj2 = int(np.random.random(1)*10000)
        saveName = str(ii) + '_' + str(jj) + '_' + str(jj2) + '.jpg'
        test1 = PIL.Image.fromarray(ff).resize((50,33))
        test1.save(os.path.join(SavePath,saveName))
        files.append(saveName)
    return files


 














