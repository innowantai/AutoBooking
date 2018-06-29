from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
import numpy as np
import csv
import os

def toonehot(text,paradict_EngTonum):
    labellist = []
    for number in text:
        onehot = [0 for _ in range(len(paradict_EngTonum))] 
        num = paradict_EngTonum[number]
        onehot[num] = 1
        labellist.append(onehot)
    return labellist

def LoadCsvToProcessLabel(savePath,Number):
    DataCsv = open(savePath, 'r', encoding = 'utf8')
    Read_Label = [toonehot(row[2],paradict_EngTonum) for row in csv.reader(DataCsv)]
    Train_label = [[] for _ in range(Number)]
    for arr in Read_Label:
        for index in range(Number):
            Train_label[index].append(arr[index])
    Train_label = [arr for arr in np.asarray(Train_label)]
    return Train_label


paradict_numToEng = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
paradict_EngTonum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}




# Create CNN Model
print("Creating CNN model...")
tensor_in = Input((50, 80, 1))
tensor_out = tensor_in
tensor_out = Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = Conv2D(filters=32, kernel_size=(3, 3), activation='relu')(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = Conv2D(filters=64, kernel_size=(3, 3), activation='relu')(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = Conv2D(filters=128, kernel_size=(3, 3), activation='relu')(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Conv2D(filters=256, kernel_size=(3, 3), activation='relu')(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Flatten()(tensor_out)
tensor_out = Dropout(0.5)(tensor_out)
tensor_out = [Dense(26, name='digit1', activation='softmax')(tensor_out),\
    Dense(26, name='digit2', activation='softmax')(tensor_out),\
    Dense(26, name='digit3', activation='softmax')(tensor_out),\
    Dense(26, name='digit4', activation='softmax')(tensor_out)]
model = Model(inputs=tensor_in, outputs=tensor_out)
model.compile(loss='categorical_crossentropy', optimizer='Adamax', metrics=['accuracy'])
model.summary()

 

def A_0_GetFigurePath(Path):
    files = os.listdir(Path)
    nPath = []
    for ff in files:
        if ff.find('.jpg') != -1:
            nPath.append(os.path.join(Path,ff))
    return nPath
    

Number = 4
TrainPath = os.path.join(os.getcwd(),'train_set')
VailPath = os.path.join(os.getcwd(),'real_set')
trainCSVPath = os.path.join(TrainPath,'train.csv')
VailCSVPath = os.path.join(VailPath,'vail.csv')



tData = A_0_GetFigurePath(TrainPath)
vData = A_0_GetFigurePath(VailPath)
 



print("Reading training data...")
train_data = np.load('Train_data.npy') 
train_label = LoadCsvToProcessLabel(trainCSVPath,4)
print("Shape of train data:", train_data.shape)

 


print("Reading validation data...")
vali_data = np.load('vali_data.npy')  
vali_label = LoadCsvToProcessLabel(VailCSVPath,4) 
print("Shape of train data:", vali_data.shape)



filepath="./cnn_modelAll.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_digit4_acc', verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor='val_loss', patience=2, verbose=1, mode='auto')
#tensorBoard = TensorBoard(log_dir = "./logs", histogram_freq = 1)
callbacks_list = [ earlystop, checkpoint]
model.fit(train_data, train_label, batch_size=400, epochs=50, verbose=2, validation_data=(vali_data, vali_label), callbacks=callbacks_list)
























#train_label = LoadCsvToProcessLabel(trainCSVPath,Number)
#vali_label = LoadCsvToProcessLabel(VailCSVPath,Number) 

