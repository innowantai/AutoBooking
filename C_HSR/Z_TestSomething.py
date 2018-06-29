import os





path = os.path.join(os.getcwd(),'Predict','06')
files = os.listdir(path)


for ii in range(22):
    if not os.path.exists(os.path.join(os.getcwd(),'Predict','%02d' % ii)):
        os.mkdir(os.path.join(os.getcwd(),'Predict','%02d' % ii))