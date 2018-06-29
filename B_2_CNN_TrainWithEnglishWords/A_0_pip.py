import pip

def AutoInstall():         
    pip.main(['install','PIL'])
    pip.main(['install','numpy'])
    pip.main(['install','keras'])
    pip.main(['install','bs4'])
    pip.main(['install','matplotlib']) 
    
 
AutoInstall()   