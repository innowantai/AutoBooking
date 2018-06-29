from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image
import time
import os
import numpy as np
from B_ImgProcessOBJ import A_IMGProcess
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
from keras.models import load_model
import PIL 
import shutil


def TransDatafromToCNN(data):
    Num = data.shape[0] 
    Result = np.zeros((Num,33,50))  
    for vv in range(Num):
        index = data[vv,:].reshape((33,50)) 
        Result[vv,:,:] = index
    return Result


def TransResult(result): 
    Res = []
    for vv in result.tolist():
        Res.append(vv.index(max(vv))) 
    return Res

def TransResultToEng(result,paradict_numToEng):
    Res = []
    for vv in result:
        Res.append(paradict_numToEng[vv])
    return Res
        
    
def A_1_SaveScreenAndIDFigure(driver,ScFigSaveName,IDFigSaveName,Url):
    #driver.find_element_by_id('yw0').click()       
    driver.save_screenshot(ScFigSaveName)
    OpenFlag = 1
    Jump = 0
    while OpenFlag == 1:   
        
        try:         
            
            if driver.title != Url:
                Jump = 1
                OpenFlag = 0 
                return Jump
            else:
                ele = driver.find_element_by_id('yw0')    
                ll = ele.location['x']
                rr = ele.location['x'] + ele.size['width']
                top = ele.location['y']
                bot = ele.location['y'] + ele.size['height']  
                img = Image.open(ScFigSaveName)
                img = img.crop((ll,top,rr,bot))
                img = img.convert("RGB") 
                img.save(IDFigSaveName) 
                OpenFlag = 0
                    
        except:
            pass
        
        
    return Jump
    
    
def A_2_IDFigureProcessing(IDFigSaveName,SaveFolder):    
    # Split Figure and save to the folder that  named in the variable of "SaveFolder"
    files = A_IMGProcess(IDFigSaveName,SaveFolder)
     
    Pre_digits = []
    for vv in files:        
        pil_image = PIL.Image.open(os.path.join(SaveFolder,vv)).convert('1')        
        Pre_digits.append([vv for vv in pil_image.getdata()]) 
    Pre_digit_ary = np.array(Pre_digits)/255 
    Pre_digit_ary = TransDatafromToCNN(Pre_digit_ary)
    X_test = Pre_digit_ary.reshape(-1, 1,33, 50) 
    Resule_Num = TransResult(model.predict(X_test))
    Resule_Eng = TransResultToEng(Resule_Num,paradict_numToEng)
    
    Res = ''
    for ff in Resule_Eng:
        Res += ff
    
    
    return Res


def A_3_DriverOperation(driver,IDResult):
    # Driver operation
    IDEng = driver.find_element_by_id('TicketForm_verifyCode')
    IDEng.send_keys(IDResult)
    
    Agree = driver.find_element_by_id('TicketForm_agree')
    Agree.click()
    
    TickNumber = Select(driver.find_element_by_class_name('mobile-select'))
    TickNumber.select_by_index(1)
    
    submit = driver.find_element_by_id('ticketPriceSubmit').click()
    
     
    Now_window_handle  = driver.current_window_handle
    return Now_window_handle








Case = 1
ScFigSaveName = 'f1_' + str(Case) + '.jpg'
IDFigSaveName = 'IDFig' + str(Case) + '.jpg'
ProcessFolder = '1_BookingProcess' + str(Case)
FullyFigureFolder = '0_FullyFigure'

paradict_numToEng = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
paradict_EngTonum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

model = load_model('my_model_CNN2.h5')

SaveFolder = os.path.join(os.getcwd(),ProcessFolder)
if not os.path.exists(SaveFolder):
    os.mkdir(SaveFolder)
    
FullyPath = os.path.join(os.getcwd(),FullyFigureFolder)
if not os.path.exists(FullyPath):
    os.mkdir(FullyPath)



url = 'https://tixcraft.com/ticket/ticket/18NewEarth/4064/1/68'

driver = webdriver.Firefox()
driver.get('https://tixcraft.com/ticket/ticket/18NewEarth/4064/1/68')
driver.minimize_window()
 

Page1Title  = 'tixCraft拓元售票系統 - New＆Earth 1st Fan Meeting in Taipei - 票種' 
Page2Title  = 'tixCraft拓元售票系統 - 登入'
   
 
OkCase = 0
kk = 0
while 1:  
    try:        
        kk += 1         
        Jump = A_1_SaveScreenAndIDFigure(driver,ScFigSaveName,IDFigSaveName,Page1Title)
        IDResult = A_2_IDFigureProcessing(IDFigSaveName,SaveFolder)
        
        if Jump == 1:
            driver.get('https://tixcraft.com/ticket/ticket/18NewEarth/4064/1/68')
            OkCase += 1
            print('OkCase',str(OkCase),'/',str(kk),'%0.1f' % (OkCase/kk*100),'% ID-words = ',IDResult)
            
            files = os.listdir(ProcessFolder)
            for num,ff in enumerate(files):
                shutil.copy(os.path.join(SaveFolder,ff),os.path.join(os.getcwd(),'0_Classify',IDResult[num]))
            
            reName = str(kk) + '_' + IDResult + '.jpg'
            os.renames(IDFigSaveName,reName)
            shutil.move(os.path.join(os.getcwd(),reName),FullyPath) 
                
        else:
            NHandle = A_3_DriverOperation(driver,IDResult)
            time.sleep(0.2) 
            
        if kk % 300 == 0:
            driver.quit()
            driver = webdriver.Firefox()
            driver.get('https://tixcraft.com/ticket/ticket/18NewEarth/4064/1/68')
            driver.minimize_window()
                
    
    except:
            driver.get('https://tixcraft.com/ticket/ticket/18NewEarth/4064/1/68')
            driver.minimize_window()
        
        
driver.quit()

 
    
