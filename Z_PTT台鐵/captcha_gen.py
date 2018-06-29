from PIL import Image, ImageDraw, ImageFont
from random import randint
import csv
import numpy as np
FONTPATH = ["./times-bold.ttf", "./courier-bold.ttf"]


class rect:
    def __init__(self):
        self.size = (randint(5, 21), randint(5, 21))
        self.location = (randint(1, 199), randint(1, 59))
        self.luoverlay = True if randint(1, 10) > 6 else False
        self.rdoverlay = False if self.luoverlay else True if randint(1, 10) > 8 else False
        self.lucolor = 0 if randint(0, 1) else 255
        self.rdcolor = 0 if self.lucolor == 255 else 255
        self.ludrawn = False
        self.rddrawn = False
        self.pattern = randint(0, 1)


    def draw(self, image, overlay):
        if((overlay or not self.luoverlay) and not self.ludrawn):
            self.ludrawn = True
            stp = self.location
            transparent = int(255 * 0.45 if self.lucolor == 0 else 255 * 0.8)
            color = (self.lucolor, self.lucolor, self.lucolor, transparent)
            uline = Image.new("RGBA", (self.size[0], 1), color)
            lline = Image.new("RGBA", (1, self.size[1]), color)
            image.paste(uline, stp, uline)
            image.paste(lline, stp, lline)
        if((overlay or not self.rdoverlay) and not self.rddrawn):
            self.rddrawn = True
            dstp = (self.location[0], self.location[1] + self.size[1])
            rstp = (self.location[0] + self.size[0], self.location[1])
            transparent = int(255 * 0.45 if self.rdcolor == 0 else 255 * 0.8)
            color = (self.rdcolor, self.rdcolor, self.rdcolor, transparent)
            dline = Image.new("RGBA", (self.size[0], 1), color)
            rline = Image.new("RGBA", (1, self.size[1]), color)
            image.paste(dline, dstp, dline)
            image.paste(rline, rstp, rline)


class captchatext:
    def __init__(self, priority, offset,engOpen):
        num = np.arange(10).tolist()
        eng = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']
        if engOpen == 1:
            numWithEng =  eng
        else:
            numWithEng = num 
        self.number = numWithEng[randint(0, len(numWithEng)-1)]
        self.color = [randint(10, 140) for _ in range(3)]
        self.angle = randint(-55, 55)
        self.priority = priority
        self.offset = offset
        self.next_offset = 0


    def draw(self, image):
        color = (self.color[0], self.color[1], self.color[2], 255)
        font = ImageFont.truetype(FONTPATH[randint(0, 1)], randint(25, 27) * 10)
        text = Image.new("RGBA", (150, 300), (0, 0, 0, 0))
        textdraw = ImageDraw.Draw(text)
        textdraw.text((0, 0), str(self.number), font=font, fill=color)
        text = text.rotate(self.angle, expand=True)
        text = text.resize((int(text.size[0] / 10), int(text.size[1] / 10)))
        base = int(self.priority * (200 / 6))
        rand_min = (offset - base - 2) if (offset - base - 2) >= -15 else -15
        rand_min = 0 if self.priority == 0 else rand_min
        rand_max = (33 - text.size[0]) if self.priority == 5 else (33 - text.size[0] + 10)
        try:
            displace = randint(rand_min, rand_max)
        except:
            displace = rand_max
        location = (base + displace, randint(3, 23))
        self.next_offset = location[0] + text.size[0]
        image.paste(text, location, text)


num = 5
outputcsv = open('./train_set/train_' +  str(num) + '.csv', 'w', encoding = 'utf8', newline = '')
numberlist = []
status = 1
for index in range(1, 20001, 1):
    print('\r' + str(index) + '/' + str(20001))
    numberstr = ""
    bgcolor = [randint(180, 250) for _ in range(3)]
    captcha = Image.new('RGBA', (200, 60), (bgcolor[0], bgcolor[1], bgcolor[2], 255))
    rectlist = [rect() for _ in range(32)]
    for obj in rectlist:
        obj.draw(image=captcha, overlay=False)

    offset = 0 
    randJudge = randint(0,num-1)
    for i in range(num):
        if i == randJudge:
            engOpen = 1
        else:
            engOpen = 0
        newtext = captchatext(i, offset,engOpen)
        newtext.draw(image=captcha)
        offset = newtext.next_offset
        numberstr += str(newtext.number) 
    numberlist.append([str(index), numberstr]) 

    for obj in rectlist:
        obj.draw(image=captcha, overlay=True)


    captcha.convert("RGB").save("./train_set/" + str(index) + '_' + str(num) + ".jpg", "JPEG")
     
    

writer = csv.writer(outputcsv)
writer.writerows(numberlist)
outputcsv.close()
