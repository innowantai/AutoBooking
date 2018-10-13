import os
import re
import cv2
import PIL  
import time
import numpy as np  
from HSRGUI import HSRGUI
from DISCOUNT import DISCOUNT
from PIL import Image 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from B_ImgProcessingOBJ import HRSImgProcess
from keras.models import load_model 
from keras.applications.vgg16 import VGG16


class HSR():
    def __init__(self):
        self.paraDic1 = {0: '2', 1: '3', 2: '4', 3: '5', 4: '7', 5: '9', 6: 'A', 7: 'C', 8: 'F', 9: 'H', 10: 'K', 11: 'M', 12: 'N', 13: 'P', 14: 'Q', 15: 'R', 16: 'T', 17: 'Y', 18: 'Z'}
        self.paraDic2 = {'2': 0, '3': 1, '4': 2, '5': 3, '7': 4, '9': 5, 'A': 6, 'C': 7, 'F': 8, 'H': 9, 'K': 10, 'M': 11, 'N': 12, 'P': 13, 'Q': 14, 'R': 15, 'T': 16, 'Y': 17, 'Z': 18}
        self.Station = {'南港':'1','台北' :'2','板橋':'3','桃園':'4','新竹':'5','苗栗':'6','台中':'7','彰化':'8','雲林':'9','嘉義':'10','台南':'11','左營':'12'}
    
    def booking(self,IDNumber,CellPhone):
        self.gui = HSRGUI()
        self.gui.GUI() 
        
        if not self.gui.flag:
            return False
        
        ########## Path Setting ########## 
        self.DataPath = os.path.join(os.getcwd(),"Data")
        
        self.Case = 'Case1'
        self.IDFIgureName = self.Case + '.jpg'
        self.IDFigurePath = os.path.join(os.path.join(self.DataPath , self.IDFIgureName))
        self.OnlineIndexPath = os.path.join(self.DataPath , self.Case)
        self.f1Path = os.path.join(self.DataPath, self.Case + '_1.jpg')
        self.f2Path = os.path.join(self.DataPath, self.Case + '_2.jpg')
        self.BaseIMGPath = os.path.join(self.DataPath,"BaseIMG")
        self.CmpIMGPath  = os.path.join(self.DataPath,self.Case + "_CmpIMG")
        if not os.path.exists(self.CmpIMGPath ):
            os.makedirs(self.CmpIMGPath )
        ##################################
        
        Data = self.gui.getStationData()
        self.startSatation = Data[0]
        self.destinationStation = Data[1]
        self.year = Data[2]
        self.month =  Data[3]
        self.day = Data[4] 
        self.timeIndex = Data[5]
        self.trainNumber = Data[6]
        self.earlyBird = Data[7]
        self.bookingMethod = Data[8]
        
        self.IDNumber = IDNumber
        self.CellPhone = CellPhone 
        self.model = load_model(os.path.join(self.DataPath,'my_model_CNN_5000_2.h5')) 
        self.VGGmodel = VGG16(weights='imagenet', include_top=False) 
        self.Input_Date = str(self.year) + '/' + '%02d' % self.month + '/' + '%02d' % self.day
        
        
        self.Loop();
        
    def Loop(self):
        try:            
            self.Start = True
            while self.Start:             
                self.t1 = time.time()   
                self.driver = webdriver.Firefox()
                self.driver.get('https://irs.thsrc.com.tw/IMINT/')            
                self.Start = self.Part1_InputInformation()  
            if self.bookingMethod == 1:
                self.Part2_selectTrainNumber() 
            self.Part3_TickInformationAndConfirm(self.IDNumber,self.CellPhone) 
        except:
            self.driver.quit()
            self.Loop()

    def Part1_InputInformation(self):
        self.driver.minimize_window()
        check = 0     
        # Setting the booked information 
        # 1.Start and destination station setting
        Start = Select(self.driver.find_element_by_name('selectStartStation'))
        Destination = Select(self.driver.find_element_by_name('selectDestinationStation'))
        Start.select_by_index(self.Station[self.startSatation])
        Destination.select_by_index(self.Station[self.destinationStation])
        
        # 2.Date and time Setting 
        # Date
        TimeSpan = self.driver.find_element_by_id('toDate')
        DateSetting = TimeSpan.find_element_by_name('toTimeInputField')
        DateSetting.clear()
        DateSetting.send_keys(self.Input_Date)
        # Time
        StartTime = Select(self.driver.find_element_by_name('toTimeTable'))
        StartTime.select_by_index(self.timeIndex)
        
        # Booking methods
        method1 = self.driver.find_element_by_id('bookingMethod_0')
        method2 = self.driver.find_element_by_id('bookingMethod_1')
        trainNumber = self.driver.find_element_by_name('toTrainIDInputField') 
        if self.bookingMethod == 1:
            method1.click()  
            
        elif self.bookingMethod == 2:
            method2.click()
            trainNumber.send_keys(self.trainNumber) 
        
        while check != -1:    
            
            if time.time() - self.t1 >= 1800: 
                self.driver.quit()
                return True
            
            if self.earlyBird == 1 and not self.driver.find_element_by_id('onlyQueryOffPeakCheckBox').is_selected():
                self.driver.find_element_by_id('onlyQueryOffPeakCheckBox').click()
                
            # 3.Save Screenshot and catch ID-Figure
            self.CatchingIDFigure(self.driver) 
            Img = HRSImgProcess()
            Img.IMGProcess(self.IDFigurePath, self.OnlineIndexPath) 
            
            # ID-figure Part
            # Find the name of input ID-figure result box and using send_keys function to send ID-words
            IDbox = self.driver.find_elements_by_name('homeCaptcha:securityCode')[0] 
            IDbox.clear()
            IDbox.send_keys(self.FigureID_sub())
            del IDbox
            
            # Click confirm box 
            self.driver.find_element_by_id('SubmitButton').click()   
            check = self.CheckPage(self.driver,'查詢車次')
            if check != -1:        
                reset = self.driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink')
                reset.click()
                del reset
        return False

    def Part2_selectTrainNumber(self):
        if self.earlyBird:                
            #disc = DISCOUNT()
            #disc.ID(self.VGGmodel,self.CatchingCountIMG()) 
            #index = disc.Index
            
            index = self.getCountRatios(self.CatchingCountIMG())
            trainIter = self.driver.find_elements_by_name('TrainQueryDataViewPanel:TrainGroup')
            trainIter[index].click()
        self.driver.find_element_by_name('SubmitButton').click() 
        
    def Part3_TickInformationAndConfirm(self,IDNumber,CellPhone):
        # Part 3 : The information of ticket
        # ID number 
        idInput = self.driver.find_element_by_id('idNumber')
        idInput.clear()
        idInput.send_keys(IDNumber)
        # Cellphone
        CellInput = self.driver.find_element_by_id('phoneNumber')
        CellInput.clear()
        CellInput.send_keys(CellPhone)
        # Agree
        agree = self.driver.find_element_by_name('agree')
        agree.click() 
        # submit
        submit = self.driver.find_element_by_id('isSubmit')
        submit.click()
        
    def CatchingCountIMG(self):
        self.driver.save_screenshot(self.f2Path)
        eles =  self.driver.find_elements_by_tag_name("img")
        kk = 0
        for ele in eles: 
            ll = ele.location['x']
            rr = ele.location['x'] + ele.size['width']
            top = ele.location['y']
            bot = ele.location['y'] + ele.size['height']    
            img = Image.open(self.f2Path)
            img = img.crop((ll,top,rr,bot))
            img = img.convert("RGB") 
            img.save(os.path.join(self.CmpIMGPath,('%02d' % kk) + '_' + self.IDFIgureName) )
            kk = kk + 1
        return kk

    def getCountRatios(self,num):  
        
        BaseImg = [ cv2.imread(os.path.join(self.BaseIMGPath,bb)) for bb in os.listdir(self.BaseIMGPath)]
        CmpImg = [ cv2.imread(os.path.join(self.CmpIMGPath,bb)) for bb in os.listdir(self.CmpIMGPath)] 
        IDres = []
        IDres = np.array([ num for cc in CmpImg     for num,bb in enumerate(BaseImg)         if np.mean(bb - cc) == 0][:num])
        Index = np.where(IDres == np.min(IDres))[0][0]
        return Index

    def CatchingIDFigure(self,driver):
        driver.save_screenshot(self.f1Path)
        ele = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')       
        ll = ele.location['x']
        rr = ele.location['x'] + ele.size['width']
        top = ele.location['y']
        bot = ele.location['y'] + ele.size['height']    
        img = Image.open(self.f1Path)
        img = img.crop((ll,top,rr,bot))
        img = img.convert("RGB") 
        img.save(self.IDFigurePath )

    def TransDatafromToCNN(self,data):
        Num = data.shape[0] 
        Result = np.zeros((Num,33,50))  
        Result = np.zeros((Num,33-5,50-10)) 
        for vv in range(Num):
            index = data[vv,:].reshape((33,50))
            index = index[3:-2,5:-5]
            Result[vv,:,:] = index
        return Result

    def TransResult(self,result): 
        Res = []
        for vv in result.tolist():
            Res.append(vv.index(max(vv))) 
        return Res

    def FigureID_sub(self): 
        Files_ = os.listdir(self.OnlineIndexPath)
        Files = []
        kk = 1
        for ff in Files_:
            if ff.find('.jpg') != -1 and kk <= 4: 
                Files.append(ff)  
                kk = kk + 1
        baseH = 50
        digits = []   
        for ii,jj in enumerate(Files): 
            pil_image = PIL.Image.open(os.path.join(self.OnlineIndexPath,jj)).convert('1') 
            baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
            img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS)
            digits.append([vv for vv in img.getdata()])
        digit_ary = np.array(digits) / 255 
        
        # Translate the figure of np.array to CNN format
        
        X_Test = self.TransDatafromToCNN(digit_ary)
        X_Test = X_Test.reshape(-1, 1,28, 40) 
        Res = self.TransResult(self.model.predict(X_Test))
        
        res = ''
        for ii in Res:
            folder = self.paraDic1[ii]
            res += folder
        return res

    def CheckPage(self,driver,checkName):
        time.sleep(1)
        page = driver.page_source
        rr = r'<title>[\D]*</title>'
        check_ = re.findall(rr,page)[0]
        check = check_.find(checkName) 
        return check
 
    
    


 



  

# =============================================================================
#  
# sad
# # Part 2 : Select Tarin Number
# select = driver.find_element_by_name('TrainQueryDataViewPanel:TrainGroup')
# radios = driver.find_elements_by_xpath("//*/input[@type='radio']")
# 
# html = driver.page_source
# data = BeautifulSoup(html,'html.parser')
# aa = data.find_all('td')
# T_number = []
# T_timeSt = []
# T_timeEnd = []
# for vv in aa: 
#     if vv.find('span',{'id':'QueryCode'}) != None:
#         vv2 = vv.find('span',{'id':'QueryCode'})
#         T_number.append(vv2.text) 
#     elif vv.find('span',{'id':'QueryDeparture'}) != None:
#         vv2 = vv.find('span',{'id':'QueryDeparture'})
#         T_timeSt.append(vv2.text)  
#     elif vv.find('span',{'id':'QueryArrival'}) != None:
#         vv2 = vv.find('span',{'id':'QueryArrival'})
#         T_timeEnd.append(vv2.text)       
#         
#         
#         
#         
# ############# Add select car number code in the furture
# 
# 
# #############
# Next2 = driver.find_element_by_name('SubmitButton').click() 
#  
# Part3_TickInformationAndConfirm(driver,IDNumber,CellPhone)
# =============================================================================
     







