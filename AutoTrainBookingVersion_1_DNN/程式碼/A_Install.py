import pip

def AutoInstall():        
    pip.main(['install','selenium'])
    pip.main(['install','pillow'])
    pip.main(['install','numpy'])
    pip.main(['install','keras'])
    pip.main(['install','bs4'])
    pip.main(['install','matplotlib'])
    pip.main(['install','tensorflow'])