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
from SSN_modul.Create_clusters import create_clusters
from SSN_modul.GCEngine import GCEngine
from SSN_modul.Database import Database
from SSN_modul.self_psd import selfpsd
#
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
from tkinter import *
from tkinter import ttk
import time as ti
from PIL import Image, ImageTk

#
from SSN_modul.gui_test import guitest
from SSN_modul.Actions import Actions
from SSN_modul.parallel_get_senPow import parallel_sensor_power
#
from rtlsdr import RtlSdr


# ----------------------------------------------------------------------
#--------------------------------------
myglobals
#----------threading to receive power from sensors-----------------
parallel_sensor_power()

CUaction = Actions()
globalEngine = GCEngine()
CU = [0]
CU[0] = LCEngine()

# button's functions
def clickMe1():
    print('imaging...')
    global CUaction
    CUaction.Hold = 0
    CUaction.Start = 1
    CUaction.Quit = 0

    #------------------------------------------------------ read input from gui
    myglobals.area_size = np.array([x.get(), y.get()])
    myglobals.PixelResolution=r.get()
    myglobals.nSSU = num.get()
    myglobals.center_freq = fc.get()
    myglobals.sample_rate = fb.get()

    if myglobals.nSSU == 0:
        myglobals.nSSU = 12
        myglobals.area_size = np.array([5,10])
        myglobals.PixelResolution = 0.5
        myglobals.center_freq = 434 * 1e6
        myglobals.sample_rate = 1e6


    #-----

    clusterConfig = np.array([1, 1])
    ClusterGroup = create_clusters(clusterConfig)

    CU[0].Clust = ClusterGroup[0]


    globalEngine.ClusterGroup = ClusterGroup
    #
    globalEngine.initialize_database()
    #
    nSSU = myglobals.nSSU
    SensorGroup = init_sensors(nSSU)

    CU[0].SensorGroup = SensorGroup
    CU[0].update_pairwise_distance()

    globalEngine.assign_LCE(CU)
    #-----

    def kriging_image():
        ima=1

        start=time.time()
        NN=1000
        ima=NN
        flag=0
        while ima:
            ima = ima - 1
            #ima=ima+1
            
            globalEngine.update_sensorloc()
            #globalEngine.LCEGroup[0].update_pairwise_distance()

            if CUaction.Quit == 1:
                #myglobals.senpow = []
                break
            elif CUaction.Hold == 1:
                #myglobals.senpow = []
                break
            elif CUaction.Start == 1:

                # ----------------------------------------------------------generate model
                #try:

                    # =================================get data for image


                    map = globalEngine.get_heat_map()
                    


                    ##globalEngine.Data.add_new_frame(map)
                    ##Img0 = globalEngine.Data.get_background()
                    Img0=map # for krige
                    #Img0=Img0.T # for self kriging and nearest
                    # -----------------------------------------------------
                    # to compare difference
                    # for transmitter location error
                    '''test=200
                    loc_err=[]
                    x0 = 3
                    y0 = 4
                    
                    while (np.max(Img0)-np.min(Img0)>4) and (test):
                        test=test-1
                        lo1=np.argwhere(Img0==np.max(Img0))
                        d=np.sqrt((0.5*lo1[0][0]+0.5-y0)**2+(0.5*lo1[0][1]+0.5-x0)**2)
                        loc_err.append(d)
                    if len(loc_err)==200:
                        print(len(loc_err))
                        print('loc_err',sum(loc_err)/len(loc_err))'''

                  # for sensor power error
                    test = 200
                    pow_err1 = []
                    #pow_err2 = []
                    while (np.max(Img0) - np.min(Img0) > 4) and (test):
                        test = test - 1
                        #print('SU22',Img0[8,3],Img0[8,4],Img0[8,5])
                        e1=abs(Img0[8,5] - myglobals.power_threads[12][-1])
                        #e2=abs(Img0[1,1] - myglobals.power_threads[13][-1])
                        pow_err1.append(e1)
                        #pow_err2.append(e2)
                    
                    if test==0:
                        #hist1, bin_edges1 = np.histogram(pow_err1, bins='auto', density=False)
                        #hist2, bin_edges2 = np.histogram(pow_err2, bins='auto', density=False)
                        #err22 = sum(np.array(hist1[0:len(bin_edges1) - 1]) * np.array(bin_edges1[0:len(bin_edges1) - 1])) / (
                                #sum(np.array(hist1)))
                        #err23 = sum(np.array(hist2[0:len(bin_edges2) - 1]) * np.array(bin_edges2[0:len(bin_edges2) - 1])) / (
                                #sum(np.array(hist2)))
                        err22=sum(np.array(pow_err1))/len(pow_err1)
                        #err23=sum(np.array(pow_err2))/len(pow_err2)
                        print('sen22', err22)
                        #print('sen23', err23)
                        

                    # -------------------------------------------------
                    loc_sen = globalEngine.SensorLoc
                    fig.clf()
                    axis1 = fig.add_subplot(111)
                    pic = axis1.imshow(Img0, origin='lower', interpolation='nearest',vmin=-50, vmax=-10)
                    fig.colorbar(pic)
                    #--------------------------------------------------
                    axis1.scatter(loc_sen[:, 0].T / myglobals.PixelResolution,
                                  loc_sen[:, 1].T / myglobals.PixelResolution, color='b')
                    #axis1.scatter(globalEngine.SourceGroup.Loc[1] / myglobals.PixelResolution, globalEngine.SourceGroup.Loc[0] / myglobals.PixelResolution, color='r')
                    axis1.set_title('Radio Environment Map')
                    axis1.set_xlabel('X[pixel]')
                    axis1.set_ylabel('Y[pixel]')
                    axis1.set_xlim(0, 2*myglobals.area_size[0])
                    axis1.set_ylim(0, 2*myglobals.area_size[1])

                    axis0.draw()
                    ## to measure tran-rem time
                    #max_value = np.max(np.max(map))
                    #if max_value > -38.5:
                     #   print('end time', time.gmtime())
                     #
                    flag=flag+1
                    #------------------
                    #print(Img0[2*y0-1,2*x0-1])
                    #print(myglobals.power_threads[myglobals.nSSU][-1])
                    #------------------
                #except:
                    #pass

        sensingtime0 = (time.time() - start)
        print('average time0', sensingtime0 / flag)#start = time.time()
        print('flag',flag)

                # ----------------------------------------------------------
    w = threading.Thread(name='worker', target=kriging_image)
    w.start()



def psdfigure(*args):

    while 1:
        #print('psd...')
        fig1.clf()
        axis1 = fig1.add_subplot(131)
        #axis1.set_title('power spectral density')
        axis1.set_xlabel('frequency[Hz]')
        axis1.set_ylabel('Relative power (dB)')
        # axis1.set_xlim(0, 10)
        axis1.set_ylim(-120, -50)
        axis2 = fig1.add_subplot(133)
        #axis1.set_title('power spectral density')
        axis2.set_xlabel('frequency[Hz]')
        axis2.set_ylabel('Relative power (dB)')
        axis2.set_ylim(-120, -50)

        # ------------------first psd figure-------------------

        if senID.get() == '0':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[0].get_new_psd(0)
            axis1.plot(fre, p_density)
        elif senID.get() == '1':
            
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[1].get_new_psd(1)
            axis1.plot(fre, p_density)
        elif senID.get() == '2':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[2].get_new_psd(2)
            axis1.plot(fre, p_density)
        elif senID.get() == '3':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[3].get_new_psd(3)
            axis1.plot(fre, p_density)
        elif senID.get() == '4':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[4].get_new_psd(4)
            axis1.plot(fre, p_density)
        elif senID.get() == '5':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[5].get_new_psd(5)
            axis1.plot(fre, p_density)
        elif senID.get() == '6':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[6].get_new_psd(6)
            axis1.plot(fre, p_density)
        elif senID.get() == '7':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[7].get_new_psd(7)
            axis1.plot(fre, p_density)
        elif senID.get() == '8':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[8].get_new_psd(8)
            axis1.plot(fre, p_density)
        elif senID.get() == '9':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[9].get_new_psd(9)
            axis1.plot(fre, p_density)
        elif senID.get() == '10':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[10].get_new_psd(10)
            axis1.plot(fre, p_density)
        elif senID.get() == '11':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[11].get_new_psd(11)
            axis1.plot(fre, p_density)
        elif senID.get() == '12':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[12].get_new_psd(12)
            axis1.plot(fre, p_density)
        elif senID.get() == '13':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[13].get_new_psd(13)
            axis1.plot(fre, p_density)

        if senID1.get() == '0':
            p_density,fre = globalEngine.LCEGroup[0].SensorGroup[0].get_new_psd(0)
            axis2.plot(fre, p_density)
        elif senID1.get() == '1':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[1].get_new_psd(1)
            axis2.plot(fre, p_density)
        elif senID1.get() == '2':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[2].get_new_psd(2)
            axis2.plot(fre, p_density)
        elif senID1.get() == '3':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[3].get_new_psd(3)
            axis2.plot(fre, p_density)
        elif senID1.get() == '4':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[4].get_new_psd(4)
            axis2.plot(fre, p_density)
        elif senID1.get() == '5':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[5].get_new_psd(5)
            axis2.plot(fre, p_density)
        elif senID1.get() == '6':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[6].get_new_psd(6)
            axis2.plot(fre, p_density)
        elif senID1.get() == '7':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[7].get_new_psd(7)
            axis2.plot(fre, p_density)
        elif senID1.get() == '8':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[8].get_new_psd(8)
            axis2.plot(fre, p_density)
        elif senID1.get() == '9':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[9].get_new_psd(9)
            axis2.plot(fre, p_density)
        elif senID1.get() == '10':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[10].get_new_psd(10)
            axis2.plot(fre, p_density)
        elif senID1.get() == '11':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[11].get_new_psd(11)
            axis2.plot(fre, p_density)
        elif senID1.get() == '12':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[12].get_new_psd(12)
            axis2.plot(fre, p_density)
        elif senID1.get() == '13':
            p_density, fre = globalEngine.LCEGroup[0].SensorGroup[13].get_new_psd(13)
            axis2.plot(fre, p_density)

        psdFig.draw()
        plt.pause(0.0000000000001)

def senloc_config(*args):
    if senID2.get()=='0':
        #print('ooooooooooooooooooooooo')
        loc=np.array([lx.get(),ly.get()])
        globalEngine.LCEGroup[0].SensorGroup[0].set_location(loc)
    if senID2.get()=='1':
        loc=np.array([lx.get(),ly.get()])
        globalEngine.LCEGroup[0].SensorGroup[1].set_location(loc)
    if senID2.get()=='2':
        loc=np.array([lx.get(),ly.get()])
        globalEngine.LCEGroup[0].SensorGroup[2].set_location(loc)
    if senID2.get()=='3':
        loc=np.array([lx.get(),ly.get()])
        globalEngine.LCEGroup[0].SensorGroup[3].set_location(loc)
    if senID2.get()=='4':
        loc=np.array([lx.get(),ly.get()])
        globalEngine.LCEGroup[0].SensorGroup[4].set_location(loc)



def clickMe2():
    global CUaction
    CUaction.Hold=1
    CUaction.Start=0
    CUaction.Quit=0

def clickMe3():
    root.destroy()





if __name__ == '__main__':
    root = Tk()
    #----------------------------------
    root.title("SSN Model")

    # environment settings
    areaSize=Label(root, text="area size(m):").grid(row=1, column=0, sticky=W)
    coX = Label(root, text="X").grid(row=1, column=1, sticky=W)
    coY = Label(root, text="Y").grid(row=1, column=2, sticky=W)
    x = DoubleVar()
    co_x = Entry(root, textvariable=x).grid(row=2, column=1, sticky=W)
    y = DoubleVar()
    co_y = Entry(root, textvariable=y).grid(row=2, column=2, sticky=W)
    resolution=Label(root, text="Resolution (pixels/m):").grid(row=1, column=3, sticky=W)
    r = DoubleVar()
    co_r = Entry(root, textvariable=r).grid(row=2, column=3, sticky=W)
    SenNum = Label(root, text="Number of Sensors:").grid(row=1, column=4, sticky=W)
    num = IntVar()
    sen_num = Entry(root, textvariable=num).grid(row=2, column=4, sticky=W)
    Fc=Label(root, text="Center frequency (Hz):").grid(row=1, column=5, sticky=W)
    fc = IntVar()
    fcvalue = Entry(root, textvariable=fc).grid(row=2, column=5, sticky=W)
    Fb = Label(root, text="Bandwidth (Hz):").grid(row=1, column=6, sticky=W)
    fb = IntVar()
    fbvalue = Entry(root, textvariable=fb).grid(row=2, column=6, sticky=W)

    # psd imaging
    psd1=Label(root, text="Power spectral density:").grid(row=3, column=3, sticky=W)
    psd2=Label(root, text="sensor ID").grid(row=4, column=3)
    psd3=Label(root, text="sensor ID").grid(row=4, column=5)

    # REM imaging
    ima = Label(root, text="Radio environment map:").grid(row=3, column=0)
    action1 = Button(root, text="Start imaging", command=clickMe1)
    action1.grid(row=4, column=0)
    action2 = Button(root, text="Hold on", command=clickMe2)
    action2.grid(row=4, column=1)
    action3 = Button(root, text="Quit REM", command=clickMe3)
    action3.grid(row=4, column=2)

    # sensor configure
    senloc1 = Label(root, text="sensor ID:").grid(row=9, column=0, sticky=W)
    senloc2 = Label(root, text="Sensor location:").grid(row=10, column=0, sticky=W)
    loX = Label(root, text="X").grid(row=10, column=1, sticky=W)
    loY = Label(root, text="Y").grid(row=10, column=2, sticky=W)
    lx = DoubleVar()
    lo_x = Entry(root, textvariable=lx).grid(row=11, column=1, sticky=W)
    ly = DoubleVar()
    lo_y = Entry(root, textvariable=ly).grid(row=11, column=2, sticky=W)
    img_gif = ImageTk.PhotoImage(Image.open("vfchair.gif"))
    label_img = Label(root, image=img_gif).grid(row=12, column=3)

    # add Combobox
    se_ID= StringVar()
    senID= ttk.Combobox(root, textvariable=se_ID)
    senID['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    senID.grid(row=4, column=4)
    senID.current(0)
    senID.bind("<<ComboboxSelected>>", psdfigure)

    se_ID1 = StringVar()
    senID1 = ttk.Combobox(root, textvariable=se_ID1)
    senID1['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    senID1.grid(row=4, column=6)
    senID1.current(0)
    senID1.bind("<<ComboboxSelected>>", psdfigure)

    se_ID2 = StringVar()
    senID2 = ttk.Combobox(root, textvariable=se_ID2)
    senID2['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    senID2.grid(row=9, column=1)
    senID2.current(0)
    senID2.bind("<<ComboboxSelected>>", senloc_config)

    #
    #fig = Figure(figsize=(8, 4))
    fig=plt.figure(1) #,figsize=(8, 4)
    axis0 = FigureCanvasTkAgg(fig, master=root)
    axis0.get_tk_widget().grid(row=5, column=0, columnspan=4, sticky=E)

    fig1 = Figure(figsize=(7, 4))
    #fig1=plt.figure(1,figsize=(7, 4))
    psdFig = FigureCanvasTkAgg(fig1, master=root)
    psdFig.get_tk_widget().grid(row=5, column=4, columnspan=4, sticky=W)






    #----------------------------------

    #
    root.update()
    root.mainloop()
