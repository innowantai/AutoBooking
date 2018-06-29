import os
import datetime
import time




def LoadAllFiles(path):
    files = os.listdir(path)
    Name = [ff.split('_')[1].split('.')[0] for ff in files]
    
    kk1 = 0
    kk2 = 0
    Allkk1 = 0
    Allkk2 = 0
    for ff in Name:
        if len(ff) == 5:
            Allkk1 += 1
            if not ff.isdigit():
                kk1 += 1 
                
        else:
            Allkk2 += 1
            if not ff.isdigit():
                kk2 += 1
    return kk1,kk2,Allkk1,Allkk2,files



path = './1_AutoClass'

            
Time = []
det_5 = []
det_6 = []
oldNum = 0
while True:       
    kk1,kk2,Allkk1,Allkk2,files = LoadAllFiles(path)
    NowTime = datetime.datetime.now()
    nTime = '%02d' % (NowTime.hour) + ':' + '%02d' % (NowTime.minute) + ':' + '%02d' % (NowTime.second)        
    print('----- NowTime : ',nTime)
    print('      Total  =  ' , len(files))
    print('      Len_5  =  ',kk1,Allkk1,'%0.2f' % (kk1/Allkk1*100),'%')
    print('      Len_6  =  ',kk2,Allkk2,'%0.2f' % (kk2/Allkk2*100),'%')
    print('      Increase : ',len(files) - oldNum)
    print('       ')
    Time.append(nTime)
    det_5.append(str(kk1) + ',' + str(Allkk1))
    det_6.append(str(kk2) + ',' + str(Allkk2))
    oldNum = len(files)
    time.sleep(60)

