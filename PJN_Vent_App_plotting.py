#import libraries
import serial
import time
from tkinter import *
from PIL import Image, ImageTk
from math import *
from threading import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class MyApp(Tk):
    global tk
    tk = Tk()
    #PJN edit size of application
    tk.geometry("1600x1200")
    tk.configure(background='white')


    def __init__(self): 
        self.threaded_dataread()
        self.threaded_plot()
        self.my_widgets()

# All GUI entry and building
    def my_widgets(self):
        # Logo entry
        #image=Image.open("/home/pi/Desktop/noulsmatic_v2/logo2.jpg")
        #photo=ImageTk.PhotoImage(image)
        #label=Label(image=photo)
        #label.image=photo
        #label.grid(row=1, column=1)
        #label.grid(columnspan = 2)
#PJN try a different method of placing this that might be better
        #label.place(relx=0.25,rely=0.05)
        # Setting breath rate
        #Label(tk,text="Breath Rate (Br/min)",fg="blue",bg="white",font=('Arial',12,'bold')).grid(
        #    row=45, column =1,pady=10)
        #PJN Change method of setting location to make this prettier
        #Label(tk,text="Breath Rate (Br/min)",fg="blue",bg="white",font=('Arial',10,'bold')).place(
        #    relx=0.1, rely = 0.25)
        #PJN change default breath rate from 100 to 80
        tk.BrRate_var=StringVar(tk,value='80')
        tk.BrRate_var.trace("w",self.callback)
        tk.BrRate=Entry(tk,textvariable=tk.BrRate_var,state='normal',disabledforeground="red")
        tk.BrRate.grid(row=46, column =1)
        tk.BrRate.bind('<Return>',self.variableupdt)
        tk.submit_button=Button(tk,text="Get Single Breath Duration",fg="black",bg="white",font=('Arial',12,'bold'),
                            command=self.calc_breathduration).grid(
                                row=47, column =1,pady=10)
    
        # Setting inhalation duration
        Label(tk,text="Inhalation Duration (msec)",fg="blue",bg="white",font=('Arial',12,'bold')).grid(
            row=49, column =1,pady=10)
        #PJN try a different method of placing this that might be better
        #Label(tk,text="Inhalation Duration (msec)",fg="blue",bg="white",font=('Arial',10,'bold')).place(
        #    relx=0.1, rely = 0.32)
        #PJN change default value from 150 to 200
        tk.InDuration_var=StringVar(tk,value='200')
        tk.InDuration_var.trace("w",self.callback)
        tk.InDuration=Entry(tk,textvariable=tk.InDuration_var,state='normal',disabledforeground="red")
        tk.InDuration.bind('<Return>',self.variableupdt)
        tk.InDuration.grid(row=50, column =1)
        #PJN Change method of placing this to make this prettier
        #tk.InDuration.place(relx=0.1, rely =0.35)

        # Setting breath hold duration
        Label(tk,text="Breath Hold Duration (msec)",fg="blue",bg="white",font=('Arial',12,'bold')).grid(
            row=51, column =1,pady=10)
        #PJN Change Default Breathhold from 150 to 200
        tk.BrHold_var=StringVar(tk,value='200')
        tk.BrHold_var.trace("w",self.callback)
        tk.BrHold=Entry(tk,textvariable=tk.BrHold_var,state='normal',disabledforeground="red")
        tk.BrHold.bind('<Return>',self.variableupdt)
        tk.BrHold.grid(row=52, column =1)

#PJN Change column from 2 to 1 for the "Freeze Breath Parameters Button
        tk.vari=IntVar()
        Checkbutton(tk, text="Freeze Breath Parameters",variable=tk.vari,fg="black",bg="white",font=('Arial',12,'bold'),
                    command=self.nancheck).grid(
                        row=55, column =1,padx=20,pady=20)

        tk.HPgas=IntVar()
        Checkbutton(tk, text="Use HP Gas",variable=tk.HPgas,fg="black",bg="white",font=('Arial',12,'bold'),
                    command=self.nancheck).grid(
                        row=55, column =1,padx=20,pady=20)

       # submit_button=Button(tk,text="Get Exhalation Duration",fg="black",bg="white",font=('Arial',12,'bold'),
       #                  command=self.calc_exhalation).grid(
       #                      row=53, column =1,pady=10)
        

        Label(tk,text="Trigger delay (msec)",fg="Red",bg="white",font=('Arial',12,'bold')).grid(
            row=45, column =3,padx=20,pady=10)
        tk.Trig_var=StringVar(tk,value='250')
        tk.Trig_var.trace("w",self.callback)
        tk.Trig=Entry(tk,textvariable=tk.Trig_var)
        tk.Trig.bind('<Return>',self.variableupdt)
        tk.Trig.grid(row=46, column =3,padx=20)
        

        Label(tk,text="Trigger length(msec)",fg="Red",bg="white",font=('Arial',12,'bold')).grid(
            row=47, column =3,padx=20,pady=10)
        tk.TrigL_var=StringVar(tk,value='10')
        tk.TrigL_var.trace("w",self.callback)
        tk.TrigL=Entry(tk,textvariable=tk.TrigL_var)
        tk.TrigL.bind('<Return>',self.variableupdt)
        tk.TrigL.grid(row=48, column =3,padx=20)


        tk.var=IntVar()
        Checkbutton(tk, text="Trigger1",variable=tk.var,fg="Red",bg="white",font=('Arial',12,'bold'),onvalue=1,
                    command=self.cb,offvalue=0).grid(
                        row=49, column =3,padx=20,pady=10)
        

        Start=Button(tk,text="Execute",fg="Black",bg="green",font=('Arial',20,'bold'),
                       command=self.execute).grid(row=55, column =2,padx=10,pady=10)
        
        Stop=Button(tk,text="Stop",fg="Black",bg="Red",font=('Arial',20,'bold'),
                      command=self.stop).grid(row=56, column =2,padx=20,pady=10)

        #ResetParameters=Button(tk,text="Reset Parameters",fg="black",bg="green",font=('Arial',12,'bold'),
                               #command=self.resetParameters).grid(row=55,column=2,padx=10,pady=10)

       # ResetTrigger=Button(tk,text="Reset Trigger",fg="Green",bg="white",font=('Arial',12,'bold'),command=self.resetTrigger).grid(row=50,column=12,padx=10,pady=10)
       #PJN 5/19/2020 - add stuff for washin/washout
        #tk.wiocb=IntVar()
        #Checkbutton(tk, text="Wash in/Wash Out",variable=tk.wiocb,fg="Red",bg="white",font=('Arial',12,'bold'),onvalue=1,
        #            command=self.wiocheck,offvalue=0).grid(
        #                row=57, column =1,padx=20,pady=20)

        # Xnuc=Button(tk,text="X-Nuclei",bg="yellow",font=('Arial',20,'bold'),
        #            command=self.startHP).grid(row=55, column =3,padx=20,pady=20)

        # n2=Button(tk,text="Nitrogen",fg="white",bg="black",font=('Arial',20,'bold'),
        #          command=self.runn2).grid(row=56, column =3,padx=20,pady=20)
    
        Exit=Button(tk,text="Exit",bg="red",font=('Arial',12,'bold'),command=self.terminate).grid(row=100, column =3,padx=10,pady=10)

        fig = Figure(figsize=(8,6))
        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Pressure Reading")
        self.graph = FigureCanvasTkAgg(fig, master = tk)
        self.graph.get_tk_widget().grid(row = 46, column = 5, rowspan = 30)
        global end_plot
        end_plot = 1


    def callback(self, *args):
        print("Variable Change!")

    def variableupdt(self,*args):
        #global gas, Inhalation, Hold, breaths, rateperiod, singleduration, Exhalation, triggerdelay, triglen
        Inhalation=int(tk.InDuration_var.get())
        Hold=int(tk.BrHold_var.get())
        breaths=int(tk.BrRate_var.get())
        HPyes = tk.HPgas.get()
        triggerdelay=int(tk.Trig_var.get())
        triglen=int(tk.TrigL_var.get())
        return Inhalation, Hold, breaths, HPyes, triggerdelay, triglen

    def nancheck(self):
          print("check")
          if tk.vari.get() == 1:
              tk.BrRate.configure(state='disabled')
              tk.BrHold.configure(state='disabled')
              tk.InDuration.configure(state='disabled')
          else:
              tk.BrRate.configure(state='normal')
              tk.BrHold.configure(state='normal')
              tk.InDuration.configure(state='normal')

    def cb(self):
        print("trigger is", tk.var.get())   

    def calc_breathduration(self):
        breaths=float(tk.BrRate_var.get())
        rateperiod=float(60) #1 min in sec
        singleduration=float(rateperiod/breaths)
        labelresult=Label(tk,text="Breath Duration =  %g  sec" %singleduration,bg="white",font=('Arial',12,'bold')).grid(row=48, column =1)
        return singleduration


#PJN - Function to open a serial connection to arduino and pass ventilation parameters
    def send2arduino(self,InDur,bhDur,bpm,HPyes,TrigStart,TrigDur):
        #Prepare string to pass to arduino
        sendStr = str(InDur) + "," + str(bhDur) + "," + str(bpm) + "," + str(HPyes) + "," + str(TrigStart) + "," + str(TrigDur) + '\n'
        #Open serial connection (this will cause Arduino to restart)
        global ser
        self.end_thread()
        print(sendStr)
        try:
            ser.close()
        except:
            a = 1
        
        print("Sending Values to Arduino")
        ser = serial.Serial('COM3',9600)
        time.sleep(2)
        Stat = ser.write(sendStr.encode())
        print("Sent Values to Arduino")
       # print(Stat)
       # line = ser.readline()
       # print(line)

    def execute(self):
        #read variables from gui
        InDur, bhDur, bpm, HPyes, TrigStart, TrigDur = self.variableupdt()
        #call serial update function
        self.send2arduino(InDur, bhDur, bpm, HPyes, TrigStart, TrigDur)
        if HPyes == 1:
            labelresult=Label(tk,text="Ventilating with 129Xe/O2",fg="green",bg="white",font=('Arial',18,'bold')).grid(row=58, column =3)
        else:
            labelresult=Label(tk,text="Ventilating with N2/O2",fg="red",bg="white",font=('Arial',18,'bold')).grid(row=58, column =3)
        self.threaded_dataread()

    def stop(self):
        global ser
        self.end_thread()
        ser.close()
        ser = serial.Serial('COM3',9600)
        time.sleep(2)
        Stat = ser.write("0,0,0,0,0,0".encode())
        labelresult=Label(tk,text="   Ventilation Stopped   ",bg="white",font=('Arial',18,'bold')).grid(row=58, column =3)
        self.threaded_dataread()

    def read_data2(self):
        global ser, kill_thread
        test_var = False
        try:
            test_var = ser.isOpen()
        except:
            test_var = False
        if not test_var:
            ser = serial.Serial('COM3',9600)
            time.sleep(2)
            Stat = ser.write("0,0,0,0,0,0".encode())
        for x in range(9):
            try:
                line = ser.readline()
                print(line)
            except:
                a=1
        starttime = time.time();
        self.sensor_data = []
        self.time_data = []
        while kill_thread:
            line = ser.readline()
            str1 = line.decode()
            str1 = str1.strip()
            str1 = str1.replace('\r','')
            try:
                val = float(str1)
            except:
                val = 0
          #  print(val)
            self.sensor_data.append(val)
            self.time_data.append(time.time()-starttime)

    def threaded_dataread(self):
        global kill_thread
        kill_thread = 1
        self.t1 = Thread(target=self.read_data2)
        self.t1.start()
        
    def threaded_plot(self):
        global end_plot
        end_plot = 1
        self.t2 = Thread(target=self.plotter)
        self.t2.start()

    def end_thread(self):
        global kill_thread
        kill_thread = 0
        self.t1.join()
      #  self.t2.join()
      #  print("Joined T2(data plot)")

    def terminate(self):
        global ser, tk, end_plot
        self.stop()
        self.end_thread()
        end_plot = 0
        ser.close()
        time.sleep(5)
        self.t2.join()
        tk.destroy()

    def plotter(self):
        global end_plot
        #I think I want this running forever... That will simplify life
        max_pressure = 0.3
        while end_plot:
            try:
                self.ax.cla()
                y = self.sensor_data
                #I'll hold off for now, but I believe that we'll need to do:
                #med = 0.5*3.3
                #high = 0.9*3.3 - med
                # Find difference between voltage reading and middle voltage range
                #y = y-med; 
                # Convert to psi using conversion factor psi = reading * max_pressure/high
                #y = y*max_pressure/high
                # Convert to cmH2O
                #y = y * 70.307
                x = self.time_data
                xs = x[-1000:]
                ys = y[-1000:]
                self.ax.plot(xs,ys)
                self.graph.draw()
            except:
                a = 1 #print("Tried to plot but failed")
            
        

def main():
   
    app = MyApp()
    tk.mainloop()
    #io.cleanup()

if __name__ == "__main__":
    main()
