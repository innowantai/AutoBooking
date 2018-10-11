import cv2
import os
import numpy as np



ori = os.getcwd()


def getCountRatios(num): 
    path1 = os.path.join(ori,"BaseIMG")
    path2 = os.path.join(ori,"CmpIMG")
    BaseImg = [ cv2.imread(os.path.join(path1,bb)) for bb in os.listdir(os.path.join(path1))]
    CmpImg = [ cv2.imread(os.path.join(path2,bb)) for bb in os.listdir(os.path.join(path2))] 
    IDres = []
    IDres = np.array([ num for cc in CmpImg     for num,bb in enumerate(BaseImg)         if np.mean(bb - cc) == 0][:num])
    Index = np.where(IDres == np.min(IDres))[0][0]
    return Index

# =============================================================================
# 
# path2 = os.path.join(ori,'CmpIMG')
# 
# files1 = os.listdir(path1)
# files2 = os.listdir(path2)
# 
# 
# base = cv2.imread(os.path.join(path1,files1[1]))
# img1 = cv2.imread(os.path.join(path2,files2[0]))
# 
# 
# =============================================================================







