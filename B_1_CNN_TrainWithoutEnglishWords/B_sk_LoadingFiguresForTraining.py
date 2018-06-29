import numpy as np
import PIL
import os



    


oPath = os.getcwd()


baseH = 50
digits = []
labels = []
for ii in range(10):
    Path = os.path.join(oPath,'ProcessData',str(ii))
    Files = os.listdir(Path)
    for jj in Files:
        pil_image = PIL.Image.open(os.path.join(Path,jj)).convert('1')
        baseW = int(pil_image.size[1]/pil_image.size[0]*baseH)
        img = pil_image.resize((baseH,baseW),PIL.Image.ANTIALIAS)
        digits.append([vv for vv in img.getdata()])
        labels.append(ii)
digit_ary = np.array(digits)



print('The Figures Loading compeleted')



##### Processing Neural Network Part #####


# =============================================================================
# from sklearn.preprocessing import StandardScaler
# from sklearn.neural_network import MLPClassifier
# 
# scaler = StandardScaler()
# scaler.fit(digit_ary)
# x_scaled = scaler.transform(digit_ary)
# 
# ### The results of 5-layer with 120 node and 30000 iter is good enough
# ### The results of 5-layer with 400 node and 50000 iter is good enough same
# #mlp = MLPClassifier(hidden_layer_sizes=(700,500,300,300,300,120,120), activation='relu',max_iter = 280000)
# mlp = MLPClassifier(hidden_layer_sizes=(500,200,70), activation='logistic',max_iter = 200000)
# #mlp = MLPClassifier(hidden_layer_sizes=(70,70), activation='logistic',max_iter = 30000)
# mlp.fit(x_scaled,labels)
# 
# 
# predict = mlp.predict(x_scaled) 
#  
# test = predict - labels 
# test2 = test[test != 0]
# 
# print(len(test2))
# =============================================================================


        
        
        
        
        
        