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
from SSN_modul.self_psd import selfpsd
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

#
from rtlsdr import RtlSdr
# Get a list of detected device serial numbers (str)
serial_numbers = RtlSdr.get_device_serial_addresses()
print('serial_numbers:', serial_numbers)
# ---------------------------------------------------------first sensor
# Find the device index for a given serial number
device_index0 = RtlSdr.get_device_index_by_serial(serial_numbers[0])  # here is the first sensor
# print('choosed device index:',device_index0)
sdr1 = RtlSdr(device_index0)
sdr1.sample_rate = 1e6
sdr1.center_freq = 434 * 1e6
sdr1.gain = 1
# second sensor
device_index1 = RtlSdr.get_device_index_by_serial(serial_numbers[1])  # here is the first sensor
# print('choosed device index:',device_index1)
sdr2 = RtlSdr(device_index1)
sdr2.sample_rate = 1e6
sdr2.center_freq = 434 * 1e6
sdr2.gain = 1


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
        myglobals.nSSU = 30
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



# def psdfigure(*args):
#
#     while 1:
#
#         if senID.get()=='0':
#             print('nothing')
#         elif senID.get()=='1':
#             # -------------------------------------------------
#             samples1 = sdr1.read_samples(56 * 1024)  # 256
#             fig1.clf()
#             axis1 = fig1.add_subplot(111)
#             p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)
#             p_density1 = 10 * np.log10(p_density1)
#             axis1.plot(fre1,p_density1)
#             axis1.set_title('power spectral density')
#             axis1.set_xlabel('frequency[MHz]')
#             axis1.set_ylabel('Relative power (dB)')
#             #axis1.set_xlim(0, 10)
#             axis1.set_ylim(-120, -50)
#             print('sensor 1')
#
#
#         elif senID.get()=='2':
#             samples2 = sdr2.read_samples(56 * 1024)  # 256
#             fig1.clf()
#             axis1 = fig1.add_subplot(111)
#             p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)
#             p_density2 = 10 * np.log10(p_density2)
#             axis1.plot(fre2, p_density2)
#             axis1.set_title('power spectral density')
#             axis1.set_xlabel('frequency[MHz]')
#             axis1.set_ylabel('Relative power (dB)')
#             axis1.set_ylim(-120, -50)
#             print('sensor 2')
#
#         psdFig.draw()
#         plt.pause(0.2)
def psdfigure(*args):

    while 1:
        fig1.clf()
        axis1 = fig1.add_subplot(131)
        #axis1.set_title('power spectral density')
        axis1.set_xlabel('frequency[MHz]')
        axis1.set_ylabel('Relative power (dB)')
        # axis1.set_xlim(0, 10)
        axis1.set_ylim(-120, -50)
        axis2 = fig1.add_subplot(133)
        #axis1.set_title('power spectral density')
        axis2.set_xlabel('frequency[MHz]')
        axis2.set_ylabel('Relative power (dB)')
        axis2.set_ylim(-120, -50)

        if senID.get()!='0' and senID1.get()=='0':
            if senID.get()=='1':
                # -------------------------------------------------
                samples1 = sdr1.read_samples(56 * 1024)  # 256

                p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)
                p_density1 = 10 * np.log10(p_density1)
                axis1.plot(fre1, p_density1)

                print('sensor 1')
            elif senID.get()=='2':
                samples2 = sdr2.read_samples(56 * 1024)  # 256
                axis1 = fig1.add_subplot(131)
                p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)
                p_density2 = 10 * np.log10(p_density2)
                axis1.plot(fre2, p_density2)

                print('sensor 2')

        elif senID.get()=='0' and senID1.get()!='0':
            if senID1.get() == '1':
                # -------------------------------------------------
                samples1 = sdr1.read_samples(56 * 1024)  # 256

                p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)
                p_density1 = 10 * np.log10(p_density1)
                axis2.plot(fre1, p_density1)
                axis2.set_title('power spectral density')
                axis2.set_xlabel('frequency[MHz]')
                axis2.set_ylabel('Relative power (dB)')
                # axis1.set_xlim(0, 10)
                axis2.set_ylim(-120, -50)
                print('sensor 1')
            elif senID1.get() == '2':
                samples2 = sdr2.read_samples(56 * 1024)  # 256

                p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)
                p_density2 = 10 * np.log10(p_density2)
                axis2.plot(fre2, p_density2)
                axis2.set_title('power spectral density')
                axis2.set_xlabel('frequency[MHz]')
                axis2.set_ylabel('Relative power (dB)')
                axis2.set_ylim(-120, -50)
                print('sensor 2')

        elif senID.get()!='0' and senID1.get()!='0':
            if senID.get() == '1' and senID1.get() == '2':
                samples1 = sdr1.read_samples(56 * 1024)  # 256

                p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)
                p_density1 = 10 * np.log10(p_density1)
                axis1.plot(fre1, p_density1)
                axis1.set_title('power spectral density')
                axis1.set_xlabel('frequency[MHz]')
                axis1.set_ylabel('Relative power (dB)')
                # axis1.set_xlim(0, 10)
                axis1.set_ylim(-120, -50)
                print('sensor 1')
                samples2 = sdr2.read_samples(56 * 1024)  # 256

                p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)
                p_density2 = 10 * np.log10(p_density2)
                axis2.plot(fre2, p_density2)
                axis2.set_title('power spectral density')
                axis2.set_xlabel('frequency[MHz]')
                axis2.set_ylabel('Relative power (dB)')
                axis2.set_ylim(-120, -50)
                print('sensor 2')
            elif senID.get() == '2' and senID1.get() == '1':
                samples2 = sdr2.read_samples(56 * 1024)  # 256
                axis1 = fig1.add_subplot(131)
                p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)
                p_density2 = 10 * np.log10(p_density2)
                axis1.plot(fre2, p_density2)
                axis1.set_title('power spectral density')
                axis1.set_xlabel('frequency[MHz]')
                axis1.set_ylabel('Relative power (dB)')
                axis1.set_ylim(-120, -50)
                print('sensor 2')
                samples1 = sdr1.read_samples(56 * 1024)  # 256

                p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)
                p_density1 = 10 * np.log10(p_density1)
                axis2.plot(fre1, p_density1)
                axis2.set_title('power spectral density')
                axis2.set_xlabel('frequency[MHz]')
                axis2.set_ylabel('Relative power (dB)')
                # axis1.set_xlim(0, 10)
                axis2.set_ylim(-120, -50)
                print('sensor 1')



        psdFig.draw()
        plt.pause(0.2)



# def psdfigure1(*args):
#     while 1:
#
#         if senID1.get() == '0':
#             print('nothing')
#         elif senID1.get() == '1':
#             # -------------------------------------------------
#             samples1 = sdr1.read_samples(56 * 1024)  # 256
#             fig2.clf()
#             axis1 = fig2.add_subplot(111)
#             p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)
#             p_density1 = 10 * np.log10(p_density1)
#             axis1.plot(fre1, p_density1)
#             axis1.set_title('power spectral density')
#             axis1.set_xlabel('frequency[MHz]')
#             axis1.set_ylabel('Relative power (dB)')
#             # axis1.set_xlim(0, 10)
#             axis1.set_ylim(-120, -50)
#             print('sensor 1')
#
#
#         elif senID1.get() == '2':
#             samples2 = sdr2.read_samples(56 * 1024)  # 256
#             fig2.clf()
#             axis1 = fig2.add_subplot(111)
#             p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)
#             p_density2 = 10 * np.log10(p_density2)
#             axis1.plot(fre2, p_density2)
#             axis1.set_title('power spectral density')
#             axis1.set_xlabel('frequency[MHz]')
#             axis1.set_ylabel('Relative power (dB)')
#             axis1.set_ylim(-120, -50)
#             print('sensor 2')
#
#         psdFig2.draw()
#         plt.pause(0.2)


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
def clickMe4():

    root.destroy()




if __name__ == '__main__':
    root = Tk()
    #----------------------------------
    root.title("SSN Model")

    # Add Labels
    SenNum=Label(root, text="Number of Sensors:").grid(row=1, column=0)
    SouLoc=Label(root, text="Source Location:").grid(row=2, column=0)
    coX=Label(root, text="X").grid(row=2, column=1)
    coY=Label(root, text="Y").grid(row=2, column=2)
    psd1=Label(root, text="power spectral density").grid(row=2, column=3)
    psd2=Label(root, text="sensor ID").grid(row=3, column=3)
    psd3=Label(root, text="sensor ID").grid(row=3, column=5)


    # Add textbox
    # 1
    num = IntVar()
    sen_num = Entry(root, textvariable=num).grid(row=1, column=1)
    # 2
    x=DoubleVar()
    co_x = Entry(root, textvariable=x).grid(row=3, column=1)
    y=DoubleVar()
    co_y = Entry(root, textvariable=y).grid(row=3, column=2)

    # Adding Buttons
    action1 = Button(root, text="start imaging", command=clickMe1)
    action1.grid(row=4, column=0)
    action2 = Button(root, text="hold on", command=clickMe2)
    action2.grid(row=4, column=1)
    action3 = Button(root, text="quit simulation", command=clickMe3)
    action3.grid(row=4, column=2)
    action4 = Button(root, text="finish", command=clickMe4)
    action4.grid(row=9, column=0)

    # add Combobox
    se_ID= StringVar()
    senID= ttk.Combobox(root, textvariable=se_ID)
    senID['values'] = (0, 1, 2)
    senID.grid(row=3, column=4)
    senID.current(0)
    senID.bind("<<ComboboxSelected>>", psdfigure)

    se_ID1 = StringVar()
    senID1 = ttk.Combobox(root, textvariable=se_ID1)
    senID1['values'] = (0, 1, 2)
    senID1.grid(row=3, column=6)
    senID1.current(0)
    senID1.bind("<<ComboboxSelected>>", psdfigure)

    #
    #fig = Figure(figsize=(4, 2))
    fig=plt.figure(1,figsize=(7, 4))
    axis0 = FigureCanvasTkAgg(fig, master=root)
    axis0.get_tk_widget().grid(row=5, column=0, columnspan=4, sticky=W)

    fig1 = Figure(figsize=(7, 4))
    psdFig = FigureCanvasTkAgg(fig1, master=root)
    psdFig.get_tk_widget().grid(row=5, column=4, columnspan=4, sticky=W)


    # fig2 = Figure(figsize=(4, 2))
    # psdFig2 = FigureCanvasTkAgg(fig2, master=root)
    # psdFig2.get_tk_widget().grid(row=12, columnspan=60)





    #----------------------------------

    #
    root.update()
    root.mainloop()