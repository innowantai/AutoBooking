

from matplotlib.pyplot import plot,savefig 

import numpy as np  

import matplotlib
matplotlib.use('TkAgg')



 

 
x=np.linspace(-4,4,30)
y=np.sin(x); 
plot(x,y,'--*b') 
savefig('MyFig.jpg')

