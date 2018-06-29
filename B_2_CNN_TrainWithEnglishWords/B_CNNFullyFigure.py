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


paradict_numToEng = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}
paradict_EngTonum = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}




# Create CNN Model
print("Creating CNN model...")
tensor_in = Input((50, 100, 1))
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
tensor_out = [Dense(36, name='digit1', activation='softmax')(tensor_out),\
    Dense(36, name='digit2', activation='softmax')(tensor_out),\
    Dense(36, name='digit3', activation='softmax')(tensor_out),\
    Dense(36, name='digit4', activation='softmax')(tensor_out),\
    Dense(36, name='digit5', activation='softmax')(tensor_out),\
    Dense(36, name='digit6', activation='softmax')(tensor_out),]
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
    

Number = 6
TrainPath = os.path.join(os.getcwd(),'train_set_' + str(Number))
VailPath = os.path.join(os.getcwd(),'real_set_' + str(Number))
trainCSVPath = os.path.join(TrainPath,'train_' + str(Number) + '.csv' )
VailCSVPath = os.path.join(VailPath,'vail' + str(Number) + '.csv')



tData = A_0_GetFigurePath(TrainPath)
vData = A_0_GetFigurePath(VailPath)
 



print("Reading training data...")
train_data = np.load('Train_data' + str(Number) + '.npy') 
train_label = LoadCsvToProcessLabel(trainCSVPath,Number)
print("Shape of train data:", train_data.shape)

 


print("Reading validation data...")
vali_data = np.load('vali_data' + str(Number) + '.npy')  
vali_label = LoadCsvToProcessLabel(VailCSVPath,Number) 
print("Shape of train data:", vali_data.shape)



filepath="./cnn_model" + str(Number) + ".h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_digit' + str(Number) + '_acc', verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor='val_loss', patience=2, verbose=1, mode='auto')
#tensorBoard = TensorBoard(log_dir = "./logs", histogram_freq = 1)
callbacks_list = [ earlystop, checkpoint]
model.fit(train_data, train_label, batch_size=400, epochs=50, verbose=2, validation_data=(vali_data, vali_label), callbacks=callbacks_list)
























#train_label = LoadCsvToProcessLabel(trainCSVPath,Number)
#vali_label = LoadCsvToProcessLabel(VailCSVPath,Number) 

