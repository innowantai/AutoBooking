from selenium import webdriver
from selenium.webdriver.support.ui import Select
import PIL  
import os
import numpy as np 
import os  
from keras.models import load_model  
from PIL import Image
import re
import time
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import shutil
from A_0_1_SplitFigureOBJ import *



def TransResult(result): 
    Res = []
    for vv in result.tolist():
        Res.append(vv.index(max(vv))) 
    return Res


def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,33,50))  
    for vv in range(Num):
        index = data[vv,:].reshape((33,50))
        #index = index[1:,3:-3]
        Result[vv,:,:] = index
    return Result

def IDNumberByCNN(AllTest):
    
    Pre_digits = []
    for test1 in AllTest:
        Pre_digits.append([vv for vv in test1.getdata()])
    
    indexData = np.array(Pre_digits)/255
    Pre_digit_ary = TransDatafromToCNN(indexData) 
    Pre_digit_ary = Pre_digit_ary.reshape(-1, 1,33, 50)
    Res = TransResult(model.predict(Pre_digit_ary))
    
    res = ''
    for ii in Res:
        res += str(ii)
    
    return res



# =============================================================================
# def IDNumberByCNN():
#     baseH = 50 
#     path = [] 
#     Pre_digits = []
#     path = os.path.join(os.getcwd(),'0_OnlineIndex')
#     files = os.listdir(path) 
#     for jj , vv in enumerate(files): 
#         pil_image = PIL.Image.open(os.path.join(path,vv)).convert('1')
#         baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
#         img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS) 
#         Pre_digits.append([vv for vv in img.getdata()]) 
#     indexData = np.array(Pre_digits)/255
#     Pre_digit_ary = TransDatafromToCNN(indexData) 
#     Pre_digit_ary = Pre_digit_ary.reshape(-1, 1,32, 44)
#     Res = TransResult(model.predict(Pre_digit_ary))
#     
#     res = ''
#     for ii in Res:
#         res += str(ii)
#     
#     return res
# =============================================================================


def StateCheck(driver,StateInformation,stage):
    sp = BeautifulSoup(driver.page_source,'html.parser')
    PageLabel = sp.find('title').text
    return PageLabel == StateInformation[stage]

def CatchingIDFigure(driver,fillName,IDFigureName):
    driver.save_screenshot(fillName)
    ele = driver.find_element_by_id('idRandomPic')       
    ll = ele.location['x']
    rr = ele.location['x'] + ele.size['width']
    top = ele.location['y']
    bot = ele.location['y'] + ele.size['height']    
    img = Image.open(fillName)
    img = img.crop((ll,top,rr,bot))
    img = img.convert("RGB") 
    img.save(os.path.join(IDFigureName) )
    
    

def FindBookedDateAndStationsInformation(driver):
    data = BeautifulSoup(driver.page_source,'html.parser')
    data2 = data.findAll('div',{'class':'col-xs-3'})
    T_Date = dict()
    Station = dict()
    for ff in data2: 
        if ff.find('label') != None:
            index = ff.find('label').text 
            if index.find('乘車日期') != -1:
                ff2 = ff.find('select')
                Times = ff2.find_all('option') 
                for ii,tt in enumerate(Times):
                    index = tt.text
                    index = index.split('【')[0]
                    index = index.replace('/','-')
                    T_Date[index] = str(ii) 
            elif index.find('起站代碼') != -1:
                ff2 = ff.find('select')
                Times = ff2.find_all('option') 
                for ii,tt in enumerate(Times):
                    index = tt.text
                    index = index.split('-')[1]
                    Station[index] = str(ii) 
                     
    return T_Date,Station
    

def Part1_InputBookedInformation(driver,Date,from_station,to_station,train_no):    
    # Get booked Date and Station information and saving into the variable of T_Date and Station respectively
    T_Date, Station =  FindBookedDateAndStationsInformation(driver)
    
    # Input train_no
    Box_train_no = driver.find_element_by_name('train_no')
    Box_train_no.clear()
    Box_train_no.send_keys(train_no) 
    

    # Input persion_id
    Box_person_id = driver.find_element_by_name('person_id')
    Box_person_id.clear()
    Box_person_id.send_keys(person_id)
    
    # Select Date, the station name of start and destination
    # The Part of Date
    Se_Date = Select(driver.find_element_by_name('getin_date'))
    Se_Date.select_by_index(int(T_Date[Date]))
    
    # The Part of Start station
    Se_Start = Select(driver.find_element_by_name('from_station'))
    Se_Start.select_by_index(int(Station[from_station]))
    
    # The Part of Destination
    Se_Destination = Select(driver.find_element_by_name('to_station'))
    Se_Destination.select_by_index(int(Station[to_station]))
    
    
    
    try:               
        time.sleep(2)
        N_order = Select(driver.find_element_by_name('n_order_qty_str'))
        N_order.select_by_index(BookNumber)    
        # If want to book the table seat, Open below code to do that
        # T_order = Select(driver.find_element_by_name('z_order_qty_str'))
        # T_order.select_by_index(BookNumber)    
    except:
        Ori_order = Select(driver.find_element_by_name('order_qty_str'))
        Ori_order.select_by_index(BookNumber - 1)
            
    Next = driver.find_element_by_class_name('col-xs-12') 
    Next.find_element_by_class_name('btn').click()



def Part2_RandomNumberID(IDFigureName,fillName,OriName):
    CatchingIDFigure(driver,fillName,IDFigureName)
    Pre_digits = MainProcess(IDFigureName,OriName)
    IDNumber = IDNumberByCNN(Pre_digits)
    
    randInput = driver.find_element_by_name('randInput')
    randInput.clear()
    randInput.send_keys(IDNumber)
    driver.find_element_by_id('sbutton').click()
    return IDNumber


def FeedBackBookedState(driver):
    sp = BeautifulSoup(driver.page_source,'html.parser')
    data = sp.find('div', {'class':'alert alert-danger'})
    if data == None:
        ErrorCase = 4
        print('---- 訂票完成 ! ')
        rr = int(np.random.random(1)*1000)
        sav = '0_BookingDone_' + str(rr) + '.jpg'
        driver.save_screenshot(sav)
        driver.get('http://railway.hinet.net/Foreign/TW/etno1.html') 
        return ErrorCase
    
    index = data.text
    ErrorCase = 0
    if index.find('身分證字號錯誤') != -1:
        ErrorCase = 3
        #print('System Response : The persion-ID Error please modify it')
        print('---- 輸入身分證有誤請更正')
    elif index.find('亂數驗證碼失敗') != -1 or index.find('亂數號碼錯誤') != -1 :
        ErrorCase = 1
        #print('System Response : Random Number Check Error, Re-try again !')
        #print('---- 驗證碼識別錯誤,將自動重新驗證')
        driver.find_element_by_class_name('btn').click()
    elif index.find('該車次可訂票時間') != -1 :
        ErrorCase = 3
        #print('System Response : The ticket in this time can not be booked')
        #print('System Response : Program will be stop')
        print('---- 此時段車票已無法訂票,程式將自動結束')
    elif index.find('該區間無剩餘座位') != -1:
        ErrorCase = 4
        #print('---- 此區間無剩餘座位,程式將持續訂購') 
        driver.back() 
        #print('System Response : The ticket in this time is no seat now, Keep booking againg') 
    elif index.find('起到站錯誤') != -1:
        print('---- 起到站錯誤,請更正,程式將自動結束')
        ErrorCase = 3
    elif index.find('車次號碼錯誤') != -1:
        print('---- 車次號碼錯誤,請確認,程式將自動結束') 
    elif index.find('超過每日允許訂票張數') != -1:
        ErrorCase = 4  
        driver.back()  
    else:
        ErrorCase = 4
        driver.get('http://railway.hinet.net/Foreign/TW/etno1.html') 
        
    return ErrorCase





model = load_model('my_model_CNN2.h5')
driver = webdriver.Firefox()
driver.get('http://railway.hinet.net/Foreign/TW/etno1.html') 
driver.minimize_window()

Case = 5
SaveName     = '1_AutoClass'
OriName      = '0_OnlineIndex' + str(Case) 
fillName = 'f1' + str(Case) + '.jpg'
IDFigureName = 'IDFigure' + str(Case) + '.jpg'


person_id = 'P123863062'
Date = '2018-07-01'
from_station = '台北'
to_station = '花蓮'
train_no = 412
BookNumber = 1

StateInformation = ['Order Train Tickets','Random Numbers Check','Order Train Tickets Result']


jumpLoop = [0,3]
ErrorNumber = 123456 
kk = 0  
kk2 = 0
SavePath = os.path.join(os.getcwd(),SaveName)
oriPath = os.path.join(os.getcwd(),OriName)

if not os.path.exists(SavePath):
    os.mkdir(SavePath)
if not os.path.exists(oriPath):
    os.mkdir(oriPath)


IDTotalNumber = 0
IDOkNumber = 0
kk2 = 0
while not ErrorNumber in jumpLoop:      
    try:
        if StateCheck(driver,StateInformation,0):
            Part1_InputBookedInformation(driver,Date,from_station,to_station,train_no)         
        elif StateCheck(driver,StateInformation,1):                 
            IDNumber = Part2_RandomNumberID(IDFigureName,fillName,OriName)  
            IDTotalNumber += 1
            kk += 1 
        elif StateCheck(driver,StateInformation,2):
            ErrorNumber = FeedBackBookedState(driver)
            kk = 0
            
            if ErrorNumber == 4:
                kk2 += 1
                IDOkNumber += 1
                files = os.listdir(oriPath)
                print('\rID-Rate : ' + str(IDOkNumber) + '/' + str(IDTotalNumber) + ', ' + '%0.2f' % (IDOkNumber/IDTotalNumber*100) + '%' )
                #for ii,ff in enumerate(files):            
                #    shutil.copy(os.path.join(oriPath,ff),os.path.join(SavePath,IDNumber[ii]))  
                os.rename(os.path.join(os.getcwd(),IDFigureName),os.path.join(os.getcwd(),str(kk2) + '_' + IDNumber + '.jpg'))
                shutil.move(os.path.join(os.getcwd(),str(kk2) + '_' + IDNumber + '.jpg'),SavePath)
                
        else  :
            driver.get('http://railway.hinet.net/Foreign/TW/etno1.html')
            kk = 0
            
        if kk >= 20:
            driver.get('http://railway.hinet.net/Foreign/TW/etno1.html')
            kk = 0 
            
        if kk2 >= 700:
            driver.close()
            driver = webdriver.Firefox()
            driver.get('http://railway.hinet.net/Foreign/TW/etno1.html') 
            driver.minimize_window()
            kk2 = 0         
                
            
        kk2 += 1
        
    except:
        driver.get('http://railway.hinet.net/Foreign/TW/etno1.html') 
        
    
 





    


















