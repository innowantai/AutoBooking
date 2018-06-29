from selenium import webdriver
from PIL import Image
import time
import os
import numpy as np


driver = webdriver.Firefox()
driver.get('https://tixcraft.com/ticket/ticket/18NewEarth/4064/1/68')

 
folderName = 'Training'
path = os.path.join(os.getcwd(),folderName)
if not os.path.exists(path):
    os.mkdir(path)
for ii in range(0,1000) :     
    print('\r NowProcess : ' + str(ii + 1) + '/' + str(500), end = ' ')   
    try:
        time.sleep(0.2)
        
        driver.find_element_by_id('yw0').click()
        
        driver.save_screenshot('f1.jpg')
        ele = driver.find_element_by_id('yw0')
        
        
        ll = ele.location['x']
        rr = ele.location['x'] + ele.size['width']
        top = ele.location['y']
        bot = ele.location['y'] + ele.size['height']
        
        num = int(np.random.random()*100000)
        img = Image.open('f1.jpg')
        img = img.crop((ll,top,rr,bot))
        img = img.convert("RGB") 
        img.save(os.path.join(os.getcwd(),folderName, '%03d' % (ii) + '_' + str(num) + '.jpg') )
    except:
        pass



