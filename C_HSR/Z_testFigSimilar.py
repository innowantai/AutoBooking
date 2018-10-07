from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import os 

def CatchingCountIMG():
    driver.save_screenshot('f2.jpg')
    eles =  driver.find_elements_by_tag_name("img")
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

def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)


def loadCountIMG(x_test,y_test): 
    for target in ["BaseIMG","CmpIMG"]:            
        for img_path in os.listdir(target):
            if img_path.endswith(".jpg"):
                img = image.load_img(target + "/"+img_path, target_size=(64, 32))
                y_test.append(img_path[0:4])
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                if len(x_test) > 0:
                    x_test = np.concatenate((x_test,x))
                else:
                    x_test=x  
    return x_test,y_test
 
    

x_test, y_test = loadCountIMG([],[]) 
x_test = preprocess_input(x_test)
model = VGG16(weights='imagenet', include_top=False) 


num = CatchingCountIMG()
# 萃取特徵
features = model.predict(x_test)
# 計算相似矩陣
features_compress = features.reshape(len(y_test),2*2*256)
sim = cosine_similarity(features_compress)[3:3+num,0:3]


 