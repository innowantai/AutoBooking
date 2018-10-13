from selenium import webdriver
from selenium.webdriver.support.ui import Select
import PIL  
import os
import numpy as np 
import os  
from keras.models import load_model 
from B_ImgProcessingOBJ import HRSImgProcess
from PIL import Image
import re
import time
from bs4 import BeautifulSoup
from keras.applications.vgg16 import VGG16

def CatchingIDFigure():
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

def FigureID_sub():
    Path = os.path.join(os.getcwd(),'0_OnlineIndex')
    Files_ = os.listdir(Path)
    Files = []
    for ff in Files_:
        if ff.find('.jpg') != -1 :
            Files.append(ff)  
    baseH = 50
    digits = []   
    for ii,jj in enumerate(Files): 
        pil_image = PIL.Image.open(os.path.join(Path,jj)).convert('1') 
        baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
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
    return res

def CheckPage(driver,checkName):
    time.sleep(1)
    page = driver.page_source
    rr = r'<title>[\D]*</title>'
    check_ = re.findall(rr,page)[0]
    check = check_.find(checkName) 
    return check


def Part1_InputInformation(driver):
    check = 0     
    # Setting the booked information 
    # 1.Start and destination station setting
    Start = Select(driver.find_element_by_name('selectStartStation'))
    Destination = Select(driver.find_element_by_name('selectDestinationStation'))
    Start.select_by_index(Station[startSatation])
    Destination.select_by_index(Station[destinationStation])
    
    # 2.Date and time Setting 
    # Date
    TimeSpan = driver.find_element_by_id('toDate')
    DateSetting = TimeSpan.find_element_by_name('toTimeInputField')
    DateSetting.clear()
    DateSetting.send_keys(Input_Date)
    # Time
    StartTime = Select(driver.find_element_by_name('toTimeTable'))
    StartTime.select_by_index('2')
    # Booking methods
    method1 = driver.find_element_by_id('bookingMethod_0')
    method2 = driver.find_element_by_id('bookingMethod_1')
    trainNumber = driver.find_element_by_name('toTrainIDInputField')
    if bookingMethod == 1:
        method1.click()
    elif bookingMethod == 2:
        method2.click()
        trainNumber.send_keys(trainNumber)
        
    
    
    while check != -1:            
        # 3.Save Screenshot and catch ID-Figure
        CatchingIDFigure()
        Img = HRSImgProcess()
        Img.IMGProcess('IDFigure.jpg')
        
        # ID-figure Part
        # Find the name of input ID-figure result box and using send_keys function to send ID-words
        IDbox = driver.find_elements_by_name('homeCaptcha:securityCode')[0] 
        IDbox.clear()
        IDbox.send_keys(FigureID_sub())
        
        # Click confirm box 
        driver.find_element_by_id('SubmitButton').click()   
        check = CheckPage(driver,'查詢車次')
        if check != -1:        
            reset = driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink')
            reset.click()
    return check


def Part3_TickInformationAndConfirm(driver,IDNumber,CellPhone):
    # Part 3 : The information of ticket
    # ID number 
    idInput = driver.find_element_by_id('idNumber')
    idInput.clear()
    idInput.send_keys(IDNumber)
    # Cellphone
    CellInput = driver.find_element_by_id('phoneNumber')
    CellInput.clear()
    CellInput.send_keys(CellPhone)
    # Agree
    agree = driver.find_element_by_name('agree')
    agree.click()
    
    # submit
    submit = driver.find_element_by_id('isSubmit')
    submit.click()
 
 
paraDic1 = {0: '2', 1: '3', 2: '4', 3: '5', 4: '7', 5: '9', 6: 'A', 7: 'C', 8: 'F', 9: 'H', 10: 'K', 11: 'M', 12: 'N', 13: 'P', 14: 'Q', 15: 'R', 16: 'T', 17: 'Y', 18: 'Z'}
paraDic2 = {'2': 0, '3': 1, '4': 2, '5': 3, '7': 4, '9': 5, 'A': 6, 'C': 7, 'F': 8, 'H': 9, 'K': 10, 'M': 11, 'N': 12, 'P': 13, 'Q': 14, 'R': 15, 'T': 16, 'Y': 17, 'Z': 18}
 


# Loading trained CNN model
model = load_model('my_model_CNN_5000_2.h5') 

# All Station select index show below
Station = {'南港':'1','台北' :'2','板橋':'3','桃園':'4','新竹':'5','苗栗':'6','台中':'7','彰化':'8','雲林':'9','嘉義':'10','台南':'11','左營':'12'}
startSatation = '左營'
destinationStation = '桃園'
year = 2018
month =  10
day = 18
IDNumber = 'P123863062123'
CellPhone = '0970393967123'
IDNumber = 'P123863062'
CellPhone = '056314222'

bookingMethod = 1
trainNumber = 123
 



Input_Date = str(year) + '/' + '%02d' % month + '/' + '%02d' % day
driver = webdriver.Firefox()
driver.get('https://irs.thsrc.com.tw/IMINT/') 
 
#Input = driver.find_element_by_id('action').send_keys('123')
 

check_1 = Part1_InputInformation(driver)  
asd
# Part 2 : Select Tarin Number
select = driver.find_element_by_name('TrainQueryDataViewPanel:TrainGroup')
radios = driver.find_elements_by_xpath("//*/input[@type='radio']")

html = driver.page_source
data = BeautifulSoup(html,'html.parser')
aa = data.find_all('td')
T_number = []
T_timeSt = []
T_timeEnd = []
for vv in aa:
    #print(vv.find('span',{'id':'QueryCode'}))
    #print(vv.find('span'))
    if vv.find('span',{'id':'QueryCode'}) != None:
        vv2 = vv.find('span',{'id':'QueryCode'})
        T_number.append(vv2.text) 
    elif vv.find('span',{'id':'QueryDeparture'}) != None:
        vv2 = vv.find('span',{'id':'QueryDeparture'})
        T_timeSt.append(vv2.text)  
    elif vv.find('span',{'id':'QueryArrival'}) != None:
        vv2 = vv.find('span',{'id':'QueryArrival'})
        T_timeEnd.append(vv2.text)       

Next2 = driver.find_element_by_name('SubmitButton').click() 
 
Part3_TickInformationAndConfirm(driver,IDNumber,CellPhone)
     







