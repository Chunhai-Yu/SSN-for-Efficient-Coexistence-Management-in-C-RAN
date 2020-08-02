#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
from tkinter import *
from tkinter import ttk
import time as ti

#
from SSN_modul.gui_test import guitest
from SSN_modul.Actions import Actions
# ----------------------------------------------------------------------
global CUaction
CUaction = Actions()
# button's functions
def clickMe1():
    global CUaction
    CUaction.Hold = 0
    CUaction.Start = 1
    CUaction.Quit = 0
    command=1
    while command:
        if CUaction.Quit==1:
            break
        elif CUaction.Hold==1:
            break
        elif CUaction.Start==1:
            try:
                global MM, xcor, ycor, img
                MM = num.get()
                xcor = x.get()
                ycor = y.get()
                if MM == 0:
                    MM = 30
                    xcor = 5
                    ycor = 2.4
                print('imaging...')
                img = guitest(MM, xcor, ycor)
                fig.clf()
                axis1 = fig.add_subplot(111)
                pic = axis1.imshow(img, interpolation='nearest')
                fig.colorbar(pic)
                axis1.set_title('Radio Environment Map')
                axis1.set_xlabel('X[m]')
                axis1.set_ylabel('Y[m]')
                # plt.colorbar()
                axis0.draw()

                plt.pause(0.5)
            except:
                pass

def clickMe2():
    global CUaction
    CUaction.Hold=1
    CUaction.Start=0
    CUaction.Quit=0
def clickMe3():
    global CUaction
    CUaction.Hold = 0
    CUaction.Start = 0
    CUaction.Quit = 1


if __name__ == '__main__':
    root = Tk()
    #----------------------------------
    root.title("SSN Model")

    # Add Labels
    SenNum=Label(root, text="Number of Sensors:").grid(row=2, column=0)
    SouLoc=Label(root, text="Source Location:").grid(row=3, column=0)
    coX=Label(root, text="X").grid(row=3, column=1)
    coY=Label(root, text="Y").grid(row=3, column=2)

    # Add textbox
    # 1
    num = IntVar()
    sen_num = Entry(root, textvariable=num).grid(row=2, column=1)
    # 2
    x=DoubleVar()
    co_x = Entry(root, textvariable=x).grid(row=4, column=1)
    y=DoubleVar()
    co_y = Entry(root, textvariable=y).grid(row=4, column=2)

    # Adding Buttons
    action1 = Button(root, text="start imaging", command=clickMe1)
    action1.grid(row=5, column=0)
    action2 = Button(root, text="hold on", command=clickMe2)
    action2.grid(row=5, column=1)
    action3 = Button(root, text="quit simulation", command=clickMe3)
    action3.grid(row=5, column=2)
    #
    #fig = Figure(figsize=(4, 2))
    fig=plt.figure(1)

    axis0 = FigureCanvasTkAgg(fig, master=root)
    axis0.get_tk_widget().grid(row=6, columnspan=3)




    #----------------------------------

    # 启动事件循环
    root.update()
    root.mainloop()