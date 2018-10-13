from selenium import webdriver
from PIL import Image
import time
import os
import numpy as np


driver = webdriver.Firefox()
driver.get('https://irs.thsrc.com.tw/IMINT/')

 
folderName = 'Training'
path = os.path.join(os.getcwd(),folderName)
for ii in range(525,5000) :        
    try:
        driver.get('https://irs.thsrc.com.tw/IMINT/')
        time.sleep(0.2)
        
        driver.save_screenshot('f1.jpg')
        ele = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')
        
        
        ll = ele.location['x']
        rr = ele.location['x'] + ele.size['width']
        top = ele.location['y']
        bot = ele.location['y'] + ele.size['height']
        
        num = int(np.random.random()*100000)
        img = Image.open('f1.jpg')
        img = img.crop((ll,top,rr,bot))
        img = img.convert("RGB") 
        img.save(os.path.join(os.getcwd(),folderName,str(ii) + '_' + str(num) + '.jpg') )
    except:
        pass



