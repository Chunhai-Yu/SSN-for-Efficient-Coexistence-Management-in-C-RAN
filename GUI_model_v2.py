#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import keyboard #Using module keyboard
import time
import threading
from SSN_modul import myglobals
from SSN_modul.Init_sensors import init_sensors
from SSN_modul.LCEngine import LCEngine
from SSN_modul.init_Sources import init_sources
from SSN_modul.Create_clusters import create_clusters
from SSN_modul.GCEngine import GCEngine
from SSN_modul.Database import Database
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
#--------------------------------------



global CUaction
CUaction = Actions()

# button's functions
def clickMe1():
    print('imaging...')
    global CUaction
    CUaction.Hold = 0
    CUaction.Start = 1
    CUaction.Quit = 0

    # read input from gui
    myglobals.nSSU = num.get()
    myglobals.loc_source = [x.get(), y.get()]

    if myglobals.nSSU == 0:
        myglobals.nSSU = 5
        myglobals.loc_source = [5, 2.4]

    #-----
    CU = [0]
    CU[0] = LCEngine()
    clusterConfig = np.array([1, 1])
    ClusterGroup = create_clusters(clusterConfig)
    CU[0].Clust = ClusterGroup[0]
    globalEngine = GCEngine()
    globalEngine.ClusterGroup = ClusterGroup
    #
    globalEngine.initialize_database()
    #
    nSSU = myglobals.nSSU
    SensorGroup = init_sensors(nSSU)
    nSource = myglobals.nSource
    SourceGroup = init_sources(nSource)

    CU[0].SensorGroup = SensorGroup
    CU[0].source = SourceGroup[0]
    CU[0].update_pairwise_distance()

    globalEngine.assign_LCE(CU)
    globalEngine.SourceGroup = SourceGroup[0]
    #-----


    def receive_sen_power():
        rece=1
        while rece:
            rece=rece+1
            print('receive:',rece)
            if CUaction.Quit == 1:
                myglobals.senpow=[]
                break
            elif CUaction.Hold == 1:
                myglobals.senpow = []
                break
            elif CUaction.Start == 1:
                # ----------------------------------------------------------generate model
                globalEngine.LCEGroup[0].updata_source_loc()
                globalEngine.updata_sourceloc()
                prx=globalEngine.LCEGroup[0].receive_senpow()
                myglobals.senpow.append(prx)
                time.sleep(1)

    def kriging_image():
        ima=1
        while ima:
            ima=ima+1
            print('ima:',ima)

            if CUaction.Quit == 1:
                myglobals.senpow = []
                break
            elif CUaction.Hold == 1:
                myglobals.senpow = []
                break
            elif CUaction.Start == 1:

                # ----------------------------------------------------------generate model
                try:
                    # =================================get data for image
                    map = globalEngine.get_heat_map()
                    globalEngine.Data.add_new_frame(map)
                    Img0 = globalEngine.Data.get_background()


                    loc_sen = globalEngine.SensorLoc

                    # -------------------------------------------------
                    fig.clf()
                    axis1 = fig.add_subplot(131)
                    pic = axis1.imshow(Img0, origin='lower', interpolation='nearest')
                    fig.colorbar(pic)
                    axis1.set_title('Radio Environment Map')

                    axis1.set_xlabel('X[pixel]')
                    axis1.set_ylabel('Y[pixel]')
                    # print('---------------------------------')
                    # axis0.draw()
                    # -------------------------------------------------
                    axis2 = fig.add_subplot(133)
                    axis2.scatter(loc_sen[:, 1].T / myglobals.PixelResolution,
                                  loc_sen[:, 0].T / myglobals.PixelResolution,color='b')

                    axis2.scatter(globalEngine.SourceGroup.Loc[1] / myglobals.PixelResolution,
                                  globalEngine.SourceGroup.Loc[0] / myglobals.PixelResolution,color='r')

                    # loes = np.argwhere(Img0 == np.max(Img0))[0]
                    # print('estimate source location',loes)
                    # axis2.scatter(loes[1],loes[0],color='g')



                    axis2.set_title('Simulation Environment')

                    axis2.set_xlabel('X[pixel]')
                    axis2.set_ylabel('Y[pixel]')
                    axis2.set_xlim(0, 10)
                    axis2.set_ylim(0, 20)


                    axis0.draw()

                    #plt.pause(0.2)
                except:
                    pass
                # ----------------------------------------------------------

    t = threading.Thread(name='receive senpow', target=receive_sen_power)
    w = threading.Thread(name='worker', target=kriging_image)
    t.start()
    w.start()
    print('over')





def clickMe2():
    global CUaction
    CUaction.Hold=1
    CUaction.Start=0
    CUaction.Quit=0
def clickMe3():
    # global CUaction
    # CUaction.Hold = 0
    # CUaction.Start = 0
    # CUaction.Quit = 1
    root.destroy()


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
    fig=plt.figure(1,figsize=(8, 4))

    axis0 = FigureCanvasTkAgg(fig, master=root)
    axis0.get_tk_widget().grid(row=6, columnspan=3)

    # fig1 = plt.figure(2,figsize=(4, 2))
    # environ = FigureCanvasTkAgg(fig1, master=root)
    # environ.get_tk_widget().grid(row=7, columnspan=3)




    #----------------------------------

    #
    root.update()
    root.mainloop()