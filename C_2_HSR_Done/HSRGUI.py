import tkinter as tk
from tkinter import ttk



class HSRGUI:
    def __init__(self):
        pass
    
    def GUI(self): 
        #### station information 
        self.timeDict = { '00:00':0, '00:30':1, '06:00':2,  '06:30':3,  '07:00':4,
             '07:30':5, '08:00':6, '08:30':7,  '09:00':8,  '09:30':9,
             '10:00':10,'10:30':11,'11:00':12, '11:30':13, '12:00':14,
             '12:30':15,'13:00':16,'13:30':17, '14:00':18, '14:30':19,
             '15:00':20,'15:30':21,'16:00':22, '16:30':23, '17:00':24,
             '17:30':25,'18:00':26,'18:30':27, '19:00':28, '19:30':29,
             '20:00':30,'20:30':31,'21:00':32, '21:30':33, '22:00':34,
             '22:30':35,'23:00':36,'23:30':37 }
        self.stations = {'南港' : 0,'台北' : 1,'板橋' : 2,'桃園' : 3,'新竹' : 4,'苗栗' : 5,'台中' : 6,'彰化' : 7,'雲林' : 8,'嘉義' : 9,'台南' : 10,'左營' : 11}
        self.years = {'2018' : 0,'2019' : 1,'2020' : 2,'2021' : 3,'2022' : 4,'2023' : 5} 
        self.earlyB = {"是":1 ,"否":0}
        self.flag = False
        ####
        
        
        
        
        self.win = tk.Tk()
        self.win.geometry('350x280+300+100')
        self.win.resizable(False, False)
        self.win.title("HSR Booking") 
        
        
        #### Variables 
        self.startName = tk.StringVar()
        self.destName = tk.StringVar()
        self.year = tk.StringVar()
        self.month = tk.StringVar()
        self.day = tk.StringVar() 
        self.startTimes = tk.StringVar() 
        self.trainNumber = tk.StringVar()
        self.earlyChecked = tk.StringVar() 
        self.var = tk.IntVar() 
        #####
        
        self.initData() 
        self.labStart = ttk.Label(self.win, text="起程站:" , font = ('新細明體',12)) 
        self.cboxStart = ttk.Combobox(self.win, width=6, textvariable = self.startName , font = ('新細明體',11))
        self.cboxStart['values'] =  ('南港','台北','板橋','桃園','新竹','苗栗','台中','彰化','雲林','嘉義','台南','左營')                              
        
        self.labDest = ttk.Label(self.win, text="到達站:" , font = ('新細明體',12)) 
        self.cboxDest = ttk.Combobox(self.win, width=6, textvariable = self.destName , font = ('新細明體',11))
        self.cboxDest['values'] =  ('南港','台北','板橋','桃園','新竹','苗栗','台中','彰化','雲林','嘉義','台南','左營')      
        
         
         
        
        self.labDate = ttk.Label(self.win, text="日期 :" , font = ('新細明體',12)) 
        self.cboxYear = ttk.Combobox(self.win, width = 4, textvariable = self.year ,font = ('times new roman',11))
        self.cboxYear['values'] = list(self.years.keys())
        
        self.cboxMonth = ttk.Combobox(self.win, width=3, textvariable = self.month ,font = ('times new roman',11) )
        self.cboxMonth['values'] = (1,2,3,4,5,6,7,8,9,10,11,12)          
        
        self.cboxDay = ttk.Combobox(self.win, width=3, textvariable = self.day ,font = ('times new roman',11)) 
        
        self.cboxDay['values'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31) 
           
        self.labDate = ttk.Label(self.win, text="日期 :" , font = ('新細明體',12))  
       
           
        self.var.set(1) 
        self.labMethod = ttk.Label(self.win, text="訂位方式 : ", font = ('新細明體',12))
        self.radio1 = tk.Radiobutton(self.win, text="起始時間搜尋 " , font = ('新細明體',12), variable = self.var, value = 1,  command = self.timeSearch)
        self.radio2 = tk.Radiobutton(self.win, text="直接輸入車號 " , font = ('新細明體',12), variable = self.var, value = 2,  command = self.directlyInput)
         
        
        self.InputTrainNumber = tk.Entry(self.win,width = 6, textvariable = self.trainNumber ,font = ('times new roman',12)) 
        self.cboxStartTime = ttk.Combobox(self.win, width=6, textvariable = self.startTimes,font = ('times new roman',12))
        self.cboxStartTime['values'] = (  '00:00', '00:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00',
                                     '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
                                     '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30')                         
        
        
        self.earlyCheck = ttk.Label(self.win, font = ('新細明體',12), text="是否只針對早鳥票 :") 
        self.cboxEarly = ttk.Combobox(self.win, font = ('新細明體',12) , width = 4, textvariable = self.earlyChecked)
        self.cboxEarly['values'] = ("否","是")  
        
        self.btnEnter = tk.Button(self.win,text = '確認',height = 1,width = 8, command = self.saveData, font = ('新細明體',12))
        self.btnEnter.grid(column=2, row=8, pady = 5) 
         
        self.initGUIData() 
        
        self.cboxMonth.state= "readonly"
        self.labStart.grid  (column=0, row=1)                       
        self.cboxStart.grid (column=1, row=1 , pady = 5, sticky = "W")        
        self.labDest.grid   (column=0, row=2, pady = 5)                        
        self.cboxDest.grid  (column=1, row=2, pady = 5, sticky = "W")  
        
        self.labDate.grid   (column=0, row=3, pady = 5)                            
        self.cboxYear.grid  (column=1, row=3, pady = 5,  sticky = "W")                         
        self.cboxMonth.grid (column=1, row=3 , pady = 5 )                  
        self.cboxDay.grid   (column=1, row=3, pady = 5 ,sticky = "E")      
        
        self.labMethod.grid (column=0, row=5, pady = 5) 
        self.radio1.grid    (column=1, row=5, pady = 5) 
        self.radio2.grid    (column=1, row=6, pady = 5)  
        
        self.InputTrainNumber.grid (column=2, row=6, pady = 5)                   
        self.cboxStartTime.grid    (column=2, row=5, pady = 5)        
        self.earlyCheck.grid       (column=1, row=7, pady = 5) 
        self.cboxEarly.grid        (column=2, row=7, pady = 5)     
                
        self.InputTrainNumber.configure(state='disabled')      
        
        self.allelements = [ self.cboxStart.state ,       self.cboxDest,        self.cboxYear ,
                             self.cboxMonth ,             self.cboxDay  ,       self.cboxStartTime,          self.cboxEarly, ]
        
        self.win.mainloop()      # 当调用mainloop()时,窗口才会显示出来 


    def directlyInput(self): 
       self.InputTrainNumber.configure(state='normal') 
       self.cboxEarly.configure(state='disabled')
       self.cboxStartTime.configure(state='disabled') 
       
    def timeSearch(self): 
       self.cboxStartTime.configure(state='normal')   
       self.InputTrainNumber.configure(state='disabled')
       self.cboxEarly.configure(state='normal')  

    def saveData(self):
        with open('preData.txt','w',encoding='big5') as f:   
            f.writelines(self.startName.get() + ",")
            f.writelines(self.destName.get() + ",")
            f.writelines(self.year.get() + ",")
            f.writelines(self.month.get() + ",")
            f.writelines(self.day.get() + ",")
            f.writelines(self.startTimes.get() + ",")
            f.writelines(self.trainNumber.get() + ",")
            f.writelines(self.earlyChecked.get() + ",")
            
        self.flag = True
        self.win.destroy()
            
    def loadPreData(self):
        with open('preData.txt','r') as f:
            data = f.readlines()
        return data        

    def initData(self):
        try:
            data = self.loadPreData()[0].split(',') 
            self.startName.set( data[0])
            self.destName.set(data[1])
            self.year.set(data[2])
            self.month.set(data[3])
            self.day.set(data[4])
            self.startTimes.set(data[5])
            self.trainNumber.set(data[6])
            self.earlyChecked.set(data[7])
        except:
            pass
        
    def initGUIData(self):
        try: 
            self.cboxStart.current(self.stations[self.startName.get()])                                       
            self.cboxDest.current(self.stations[self.destName.get()])                                
            self.cboxYear.current(self.years[self.year.get()])                     
            self.cboxMonth.current(int(self.month.get()) - 1) 
            self.cboxDay.current(int(self.day.get()) - 1)
            self.cboxStartTime.current(self.timeDict[self.startTimes.get()])                             
            self.cboxEarly.current(self.earlyB[self.earlyChecked.get()])  
        except:
            self.cboxStart.current(0)                                       
            self.cboxDest.current(0)                                
            self.cboxYear.current(0)                     
            self.cboxMonth.current(0) 
            self.cboxDay.current(0)
            self.cboxStartTime.current(0)                             
            self.cboxEarly.current(0)
            
    def getStationData(self):
        data = [self.startName.get(),
                self.destName.get(),
                int(self.year.get()),
                int(self.month.get()),
                int(self.day.get()),
                int(self.timeDict[self.startTimes.get()]),
                int(self.trainNumber.get()),
                int(self.earlyB[self.earlyChecked.get()]),
                int(self.var.get())]
        return data
    
    


# =============================================================================
# gg = HSRGUI()
# gg.GUI()
# 
# 
# print(gg.getStationData())
# 
# =============================================================================

