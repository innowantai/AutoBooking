from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import os
import time
import shutil








class HRSImgProcess():
    
    def __int__(self):
        pass
        
    def IMGProcess(self,fileName):
        try:    
            Name = fileName.split('.')[0]
            oriimg = cv2.imread(os.path.join(os.getcwd(),fileName))  
            img = self.ImageCurveProcess(oriimg) 
            img2 = self.takeOffBoundary(img)
                          
            data = self.takeOffPoints_2(img2)
            data = self.takeOffPoints(data)
            data = self.takeOffPoints_2(data)
            data = self.takeOffPoints(data)
            
            fig = self.splitFigure(data)
            result = self.CatchingsplitFigure(fig) 
            SaveCreat = os.path.join(os.getcwd(),'0_OnlineIndex') 
            if not os.path.exists(SaveCreat):
                os.mkdir(SaveCreat)
            oldFiles = os.listdir(SaveCreat)
            
            for ff in oldFiles:
                os.remove(os.path.join(SaveCreat,ff))
             
            for kk,ff in enumerate(result):
                saveName = os.path.join(os.getcwd(),'0_OnlineIndex', Name + '_'+ str(kk) + '.jpg')             
                if not os.path.exists(saveName):
                    plt.figure(figsize=(6,4), dpi = 100)
                    plt.imshow(ff) 
                    plt.savefig(saveName,dpi=100)  
            plt.close('all') 
        
        except:
            print('Have Error !')
        
        
        
        
    
    def ImageCurveProcess(self,img):
        dimg = cv2.fastNlMeansDenoisingColored(img,None,35,35,7,21)
        # Loading figure and translate GRAY
        _,thresh = cv2.threshold(dimg,127,255,cv2.THRESH_BINARY_INV)
        imgarr = cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
        
        ##### Fitting poly 
        # Catching the curve of left and right side saving variable : imgarr
        imgarr[:,10:-5] = 0 
        ww = imgarr.shape[1]
        hh = imgarr.shape[0]
         
        # finding curve position by function of np.where 
        imgData = np.where(imgarr == 255)
        
        # The results include two element first is Y-dir second is X-dir 
        X = np.array([imgData[1]])
        Y = hh - imgData[0]
        
        # Setting parameter for fitting 
        poly_reg = PolynomialFeatures(degree = 2)   
        X_ = poly_reg.fit_transform(X.T)
        reg = LinearRegression()
        reg.fit(X_,Y)
        X2 = np.array([[i for i in range(0,ww)]])
        X2_ = poly_reg.fit_transform(X2.T)
        
        # =============================================================================
        # plt.figure()
        # plt.scatter(X,Y, color="black")
        # plt.ylim(ymin=0)
        # plt.ylim(ymax=47)
        # plt.plot(X2.T, reg.predict(X2_), color= "blue", linewidth = 28)
        # =============================================================================
        
        # Creating new image by thresh 
        newimg =  cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY) 
        
        # Stack the result Y and X into (Y,X) by function of np.colimn.stack
        # The result of fitting have tiny shift
        # To modify shift step show below : 
        # 1 : Calculation curve center of ori-Image
        # 2 : Calculation curve top and bottom boundary of ori-Image
        # 3 : Calculation pixels between top and center saving variable difTop
        # 4 : Calculation pixels center top and bottom saving variable difBot
        combine = np.column_stack([reg.predict(X2_).round(0),X2[0],] )
        shiht = np.where(imgarr[:,0] != 0)
        aver = np.mean(shiht).round(0)
        top = np.min(shiht)
        bot = np.max(shiht)
        diff = int(aver - hh + combine[0][0])
        difTop = int(aver-top)  -1
        difBot = int(bot - aver) +1
         
        # Translation the color of curve and modify width by difTop and difBot
        for ele in combine:
            pos = hh-int(ele[0]) + diff
            newimg[pos-difTop:pos+difBot,int(ele[1])] =   255 - newimg[pos-difTop:pos+difBot,int(ele[1])]
        #plt.figure()
        #plt.imshow(newimg)
        return newimg

    def takeOffBoundary(self,img):
        rr = [] 
        for ii in range(img.shape[1]):
            index = img[:,ii]
            rr.append(len(index[index == 0]))
        rr2 = np.array(rr)
        po = np.where(rr2 > (img.shape[0] - 5))[0]
        
        dif = []
        for ii in range(len(po)-1):
            index = po[ii+1]-po[ii]
            if index != 1:
                dif.append(ii)
                
        st = po[dif[0]]
        en = po[dif[-1]+1]
        img2 = img[:,st:en]
        #plt.imshow(img2)
        return img2
    
    def takeOffPoints(self,img2):
        num = 2  
        data = np.copy(img2)
        for ii in range(num,data.shape[0]):    
            for jj in range(num,data.shape[1]):
                index = data[ii-num:ii+num-1,jj-num:jj+num-1]
                # 1: take off singal point 
                if index[1,1] == 255 and len(index[index == 255]) == 1:
                    index[1,1] = 0       
                # 2: Adding singal point
                if index[1,1] == 0 and len(index[index == 0]) <= 2:
                    index[1,1] = 255
                # 3: Take off cornet point
                if index[1,1] == 255 and len(np.where(index[1,:] == 255)[0]) == 1 and len(np.where(index[:,1] == 255)[0]) == 1 and len(np.where(index == 255)[0]) == 2 :
                    index[1,1] = 0
                # 4: Adding hole point 
                if index[1,1] == 0 and len(np.where(index[1,:] == 255)[0])+len(np.where(index[:,1] == 255)[0]) >=3  : #and len(np.where(index == 255)[0]) >= 6 :
                    index[1,1] = 255
                # 5: Take off H-dir points
                if index[1,1] == 255 and len(np.where(index[1,:] == 255)[0]) == 3 and len(np.where(index == 255)[0]) == 3:  
                   index[1,:] = 0    
                # 6: Take off V-dir points
                if index[1,1] == 255 and len(np.where(index[:,1] == 255)[0]) == 3 and len(np.where(index == 255)[0]) == 3:  
                   index[:,1] = 0  
                # 7: Add off H-dir points
                if index[1,1] == 0 and len(np.where(index[1,:] == 0)[0]) == 3 and len(np.where(index == 255)[0]) >=5:   
                   index[:,1] = 255  
                # 8: take off H-dir discrete points   
                if index[1,1] == 255 and len(np.where(index[1,:] == 255)[0]) == 2 and len(np.where(index == 255)[0]) <= 3:  
                   index[1,:] = 0
                # 8: take off V-dir discrete points
                if index[1,1] == 255 and len(np.where(index[:,1] == 255)[0]) == 2 and len(np.where(index == 255)[0]) <= 3:  
                   index[:,1] = 0               
        return data
    
    def takeOffPoints_2(self,img2):
        num = 2
        data = np.copy(img2)
        for ii in range(num,data.shape[0]):    
            for jj in range(num,data.shape[1]):
                index = data[ii-num:ii+num-1,jj-num:jj+num-1]
                if index[1,1] == 255 and len(np.where(index[1,:] == 255)[0]) == 2 and len(np.where(index == 255)[0]) <= 3:  
                   index[1,:] = 0
                if index[1,1] == 255 and len(np.where(index[:,1] == 255)[0]) == 2 and len(np.where(index == 255)[0]) <= 3:  
                   index[:,1] = 0
        return data
        
    
    def CmpVertical(self,data):   
        rr = []
        for ii in range(data.shape[1]):
            index = data[:,ii]
            rr.append(len(np.where(index == 255)[0]))
        return np.array(rr)
    
    # This function is to split sub-figure, it may have some problem will be process
    def splitFigure(self,data):      
        rr = []
        for ii in range(data.shape[1]):
            index = data[:,ii]
            rr.append(len(np.where(index == 255)[0]))
        rr = np.array(rr)
        #### This number is to decide take off number
        po = np.where(rr <= 3)[0].tolist()
        if po[0] != 0:
            po = [0] + po
        if po[-1] != data.shape[1]:
            po = po + [data.shape[1]]    
        
        thre = data.shape[1] / 3 
        fig = []
        for ii in range(len(po)-1):
            index = po[ii+1] - po[ii]
            if index >= 10:
                newImg = data[:,po[ii]:po[ii+1]]
                if newImg.shape[1] >= thre:
                    ss = round((newImg.shape[1] / 2))
                    fig.append(newImg[:,:ss])
                    fig.append(newImg[:,ss:])             
                else:            
                    fig.append(newImg)    
        return fig
    
    
    def CatchingsplitFigure(self,fig):
        cat = [] 
        for ff in fig:        
            rr = []
            ff[0,:] = 0
            ff[-1,:] = 0
            # Catching 255 position for H-dir
            for ii in range(ff.shape[0]):
                index = len( np.where(ff[ii,:] == 255)[0])  
                if index != 0 :
                    rr.append(255)
                else:
                    rr.append(0)
                    
            # Catching cross position
            res = []
            for ii in range(len(rr) - 1):
                index = rr[ii+1] - rr[ii]
                if index == 255 or index == -255:
                    res.append(ii)
                    
            # If the interval more then 2, catching the figure of most length interval 
            if len(res) > 2:
                las = 0 
                po = 0
                for ii in range(len(res)-1):
                    if res[ii+1] - res[ii] > las:
                        las = res[ii+1] - res[ii] 
                        po = ii
                res = [res[po], res[po+1]]
            cat.append(res) 
              
        result = []
        for ii,ff in enumerate(fig):
            po = cat[ii]
            index = ff[po[0]:po[1],:]
            result.append(index)
        return result
    





Img = HRSImgProcess()
Img.IMGProcess('IDFigure.jpg')





 


