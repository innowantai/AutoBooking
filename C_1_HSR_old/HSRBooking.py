import os
import re
import PIL  
import time
import numpy as np  
from DISCOUNT import DISCOUNT
from PIL import Image
from bs4 import BeautifulSoup
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
    
    def booking(self,startSatation,destinationStation,year,month,day,timeIndex,IDNumber,CellPhone,bookingMethod,trainNumber,earlyBird):
        self.startSatation = startSatation
        self.destinationStation = destinationStation
        self.year = year
        self.month =  month
        self.day = day 
        self.timeIndex = timeIndex
        self.IDNumber = IDNumber
        self.CellPhone = CellPhone
        self.bookingMethod = bookingMethod
        self.trainNumber = trainNumber
        self.earlyBird = earlyBird
        self.model = load_model('my_model_CNN_5000_2.h5') 
        self.VGGmodel = VGG16(weights='imagenet', include_top=False) 
        self.Input_Date = str(year) + '/' + '%02d' % month + '/' + '%02d' % day
        
        self.driver = webdriver.Firefox()
        self.driver.get('https://irs.thsrc.com.tw/IMINT/')
        
        self.Part1_InputInformation()  
        
        self.Part2_selectTrainNumber()
        
        self.Part3_TickInformationAndConfirm(self.IDNumber,self.CellPhone)

    def Part1_InputInformation(self):
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
            if self.earlyBird == 1:
                self.driver.find_element_by_id('onlyQueryOffPeakCheckBox').click()
        elif self.bookingMethod == 2:
            method2.click()
            trainNumber.send_keys(self.trainNumber)
        
        while check != -1:            
            # 3.Save Screenshot and catch ID-Figure
            self.CatchingIDFigure(self.driver)
            Img = HRSImgProcess()
            Img.IMGProcess('IDFigure.jpg')
            
            # ID-figure Part
            # Find the name of input ID-figure result box and using send_keys function to send ID-words
            IDbox = self.driver.find_elements_by_name('homeCaptcha:securityCode')[0] 
            IDbox.clear()
            IDbox.send_keys(self.FigureID_sub())
            
            # Click confirm box 
            self.driver.find_element_by_id('SubmitButton').click()   
            check = self.CheckPage(self.driver,'查詢車次')
            if check != -1:        
                reset = self.driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink')
                reset.click()
        return check

    def Part2_selectTrainNumber(self):
        if self.earlyBird:                
            disc = DISCOUNT()
            disc.ID(self.VGGmodel,self.CatchingCountIMG()) 
            index = disc.Index
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
        self.driver.save_screenshot('f2.jpg')
        eles =  self.driver.find_elements_by_tag_name("img")
        kk = 0
        for ele in eles: 
            ll = ele.location['x']
            rr = ele.location['x'] + ele.size['width']
            top = ele.location['y']
            bot = ele.location['y'] + ele.size['height']    
            img = Image.open('f2.jpg')
            img = img.crop((ll,top,rr,bot))
            img = img.convert("RGB") 
            img.save(os.path.join(os.getcwd(),'CmpIMG',('%02d' % kk) + '_IDFigure.jpg') )
            kk = kk + 1
        return kk


    def CatchingIDFigure(self,driver):
        driver.save_screenshot('f1.jpg')
        ele = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')       
        ll = ele.location['x']
        rr = ele.location['x'] + ele.size['width']
        top = ele.location['y']
        bot = ele.location['y'] + ele.size['height']    
        img = Image.open('f1.jpg')
        img = img.crop((ll,top,rr,bot))
        img = img.convert("RGB") 
        img.save(os.path.join('IDFigure.jpg') )

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
        Path = os.path.join(os.getcwd(),'0_OnlineIndex')
        Files_ = os.listdir(Path)
        Files = []
        kk = 1
        for ff in Files_:
            if ff.find('.jpg') != -1 and kk <= 4: 
                Files.append(ff)  
                kk = kk + 1
        baseH = 50
        digits = []   
        for ii,jj in enumerate(Files): 
            pil_image = PIL.Image.open(os.path.join(Path,jj)).convert('1') 
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
 
    
    

startSatation = '左營'
destinationStation = '桃園'
year = 2018
month =  10
day = 16
IDNumber = 'P123863062123'
CellPhone = '0970393967123' 
trainNumber = 1234
bookingMethod = 1
earlyBird = 1
timeIndex = 13

BOOK = HSR()
BOOK.booking(startSatation,destinationStation,year,month,day,timeIndex,IDNumber,CellPhone,bookingMethod,trainNumber,earlyBird)
 


 



  

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
     







