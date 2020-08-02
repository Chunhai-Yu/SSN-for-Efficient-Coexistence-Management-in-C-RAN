## to test the time-cost T for parallel(threding) samples.
# here i use two sensors, and each sensor is sampled for NN=100 times, the output is the average time-cost
# to get powers from sensor1 and sensor2 for one time
# the sampled values are stored in myglobals.power1 and myglobals.power2, it can be used in kriging in future
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

#
from SSN_modul.gui_test import guitest
from SSN_modul.Actions import Actions
from SSN_modul.parallel_get_senPow import parallel_sensor_power
## this part is for sensing threadings

import matplotlib as mpl
mpl.use('TkAgg')
import threading
from SSN_modul import myglobals
import time
#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
from tkinter import *
from numpy import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import time
from SSN_modul.Received_power import received_power
from SSN_modul.Received_power import received_power2
from SSN_modul.self_psd import selfpsd


# Get a list of detected device
#first sensor
sdr0 = RtlSdr(serial_number='10')
sdr0.sample_rate = myglobals.sample_rate
sdr0.center_freq = myglobals.center_freq
sdr0.gain = 1
# second sensor
sdr1 = RtlSdr(serial_number='11')
sdr1.sample_rate = myglobals.sample_rate
sdr1.center_freq = myglobals.center_freq
sdr1.gain = 1
# third sensor
sdr2 = RtlSdr(serial_number='12')
sdr2.sample_rate = myglobals.sample_rate
sdr2.center_freq = myglobals.center_freq
sdr2.gain = 1
# fourth sensor
sdr3 = RtlSdr(serial_number='13')
sdr3.sample_rate = myglobals.sample_rate
sdr3.center_freq = myglobals.center_freq
sdr3.gain = 1
# fifth sensor
sdr4 = RtlSdr(serial_number='14')
sdr4.sample_rate = myglobals.sample_rate
sdr4.center_freq = myglobals.center_freq
sdr4.gain = 1
# sixth
sdr5 = RtlSdr(serial_number='15')
sdr5.sample_rate = myglobals.sample_rate
sdr5.center_freq = myglobals.center_freq
sdr5.gain = 1
# seventh
sdr6 = RtlSdr(serial_number='16')
sdr6.sample_rate = myglobals.sample_rate
sdr6.center_freq = myglobals.center_freq
sdr6.gain = 1
# 8
sdr7 = RtlSdr(serial_number='17')
sdr7.sample_rate = myglobals.sample_rate
sdr7.center_freq = myglobals.center_freq
sdr7.gain = 1
# 9
sdr8 = RtlSdr(serial_number='18')
sdr8.sample_rate = myglobals.sample_rate
sdr8.center_freq = myglobals.center_freq
sdr8.gain = 1
# 10
sdr9 = RtlSdr(serial_number='19')
sdr9.sample_rate = myglobals.sample_rate
sdr9.center_freq = myglobals.center_freq
sdr9.gain = 1
# 11
sdr10 = RtlSdr(serial_number='20')
sdr10.sample_rate = myglobals.sample_rate
sdr10.center_freq = myglobals.center_freq
sdr10.gain = 1
# 12
sdr11 = RtlSdr(serial_number='21')
sdr11.sample_rate = myglobals.sample_rate
sdr11.center_freq = myglobals.center_freq
sdr11.gain = 1


N = 1
M=256


def receive_power0(sdr, id):
    sdr0 = sdr
    fre0 = 0
    raw_data0 = np.zeros((N, 1024))
    for ii in range(0, N):
        samples0 = sdr0.read_samples(56 * 1024)  # 256
        p_density0, fre0 = selfpsd(samples0, NFFT=1024, Fs=sdr0.sample_rate,
                                   Fc=sdr0.center_freq)  # get psd using own function
        raw_data0[ii, :] = p_density0

    re_pow0, new_psd0, f_new0 = received_power2(raw_data0, fre0, 1, M)
    myglobals.power_threads[id].append(re_pow0)
    myglobals.psd_threads[id].append(new_psd0)
    myglobals.fre_threads[id].append(f_new0)
    # myglobals.power_threads[id]=re_pow0
    # myglobals.psd_threads[id]=new_psd0
    # myglobals.fre_threads[id]=f_new0
    # print(id)
# def receive_power0():
#
#
#     fre0 = 0
#     raw_data0 = np.zeros((N, 1024))
#     for ii in range(0, N):
#         samples0 = sdr0.read_samples(56 * 1024)  # 256
#         p_density0, fre0 = selfpsd(samples0, NFFT=1024, Fs=sdr0.sample_rate, Fc=sdr0.center_freq)  # get psd using own function
#         raw_data0[ii, :] = p_density0
#
#
#     re_pow0, new_psd0, f_new0 = received_power2(raw_data0, fre0, 1, M)
#     myglobals.power_threads[0].append(re_pow0)
#     myglobals.psd_threads[0].append(new_psd0)
#     myglobals.fre_threads[0].append(f_new0)
#     # myglobals.power_threads[0]=re_pow0
#     # myglobals.psd_threads[0]=new_psd0
#     # myglobals.fre_threads[0]=f_new0
#     #print('nothing0')

def receive_power1():


    fre1 = 0
    raw_data1 = np.zeros((N, 1024))
    for ii in range(0, N):
        samples1 = sdr1.read_samples(56 * 1024)  # 256
        p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)  # get psd using own function
        raw_data1[ii, :] = p_density1


    re_pow1, new_psd1, f_new1 = received_power2(raw_data1, fre1, 1, M)
    myglobals.power_threads[1].append(re_pow1)
    myglobals.psd_threads[1].append(new_psd1)
    myglobals.fre_threads[1].append(f_new1)
    # myglobals.power_threads[1]=re_pow1
    # myglobals.psd_threads[1]=new_psd1
    # myglobals.fre_threads[1]=f_new1
    #print('nothing1')

def receive_power2():


    fre2 = 0
    raw_data2 = np.zeros((N, 1024))
    for ii in range(0, N):
        samples2 = sdr2.read_samples(56 * 1024)  # 256
        p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)  # get psd using own function
        raw_data2[ii, :] = p_density2


    re_pow2, new_psd2, f_new2 = received_power2(raw_data2, fre2, 1, M)
    myglobals.power_threads[2].append(re_pow2)
    myglobals.psd_threads[2].append(new_psd2)
    myglobals.fre_threads[2].append(f_new2)
    # myglobals.power_threads[2]=re_pow2
    # myglobals.psd_threads[2]=new_psd2
    # myglobals.fre_threads[2]=f_new2
    #print('nothing2')

def receive_power3():


    fre3 = 0
    raw_data3 = np.zeros((N, 1024))
    for ii in range(0, N):
        samples3 = sdr3.read_samples(56 * 1024)  # 256
        p_density3, fre3 = selfpsd(samples3, NFFT=1024, Fs=sdr3.sample_rate, Fc=sdr3.center_freq)  # get psd using own function
        raw_data3[ii, :] = p_density3


    re_pow3, new_psd3, f_new3 = received_power2(raw_data3, fre3, 1, M)
    myglobals.power_threads[3].append(re_pow3)
    myglobals.psd_threads[3].append(new_psd3)
    myglobals.fre_threads[3].append(f_new3)
    #myglobals.power_threads[3]=re_pow3
    #myglobals.psd_threads[3]=new_psd3
    #myglobals.fre_threads[3]=f_new3
    #print('nothing3')

def receive_power4():


    fre4 = 0
    raw_data4 = np.zeros((N, 1024))
    for ii in range(0, N):
        samples4 = sdr4.read_samples(56 * 1024)  # 256
        p_density4, fre4 = selfpsd(samples4, NFFT=1024, Fs=sdr4.sample_rate, Fc=sdr4.center_freq)  # get psd using own function
        raw_data4[ii, :] = p_density4


    re_pow4, new_psd4, f_new4 = received_power2(raw_data4, fre4, 1, M)
    myglobals.power_threads[4].append(re_pow4)
    myglobals.psd_threads[4].append(new_psd4)
    myglobals.fre_threads[4].append(f_new4)
    #myglobals.power_threads[4]=re_pow4
    #myglobals.psd_threads[4]=new_psd4
    #myglobals.fre_threads[4]=f_new4
    #print('nothing4')

def receive_power5():

    fre5 = 0
    raw_data5 = np.zeros((N, 1024))
    for ii in range(0, N):
        samples5 = sdr5.read_samples(56 * 1024)  # 256
        p_density5, fre5 = selfpsd(samples5, NFFT=1024, Fs=sdr5.sample_rate, Fc=sdr5.center_freq)  # get psd using own function
        raw_data5[ii, :] = p_density5


    re_pow5, new_psd5, f_new5 = received_power2(raw_data5, fre5, 1, M)
    myglobals.power_threads[5].append(re_pow5)
    myglobals.psd_threads[5].append(new_psd5)
    myglobals.fre_threads[5].append(f_new5)
    # myglobals.power_threads[5]=re_pow5
    # myglobals.psd_threads[5]=new_psd5
    # myglobals.fre_threads[5]=f_new5
    #print('nothing5')

def receive_power6():

    fre6 = 0
    raw_data6 = np.zeros((N, 1024))
    for ii in range(0, N):
        samples6 = sdr6.read_samples(56 * 1024)  # 256
        p_density6, fre6 = selfpsd(samples6, NFFT=1024, Fs=sdr6.sample_rate, Fc=sdr6.center_freq)  # get psd using own function
        raw_data6[ii, :] = p_density6


    re_pow6, new_psd6, f_new6 = received_power2(raw_data6, fre6, 1, M)
    myglobals.power_threads[6].append(re_pow6)
    myglobals.psd_threads[6].append(new_psd6)
    myglobals.fre_threads[6].append(f_new6)
    # myglobals.power_threads[6]=re_pow6
    # myglobals.psd_threads[6]=new_psd6
    # myglobals.fre_threads[6]=f_new6
    #print('nothing6')


#if __name__ == '__main__':

globalEngine = GCEngine()
CU = [0]
CU[0] = LCEngine()
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


NN=100
mm=NN
start = time.time()
while NN:
    NN=NN-1
    # ==========================get power
    receive_power0(sdr0, 0)
    receive_power0(sdr1, 1)
    receive_power0(sdr2, 2)
    receive_power0(sdr3, 3)
    receive_power0(sdr4, 4)
    receive_power0(sdr5, 5)
    receive_power0(sdr6, 6)
    receive_power0(sdr7, 7)
    receive_power0(sdr8, 8)
    receive_power0(sdr9, 9)
    receive_power0(sdr10, 10)
    receive_power0(sdr11, 11)

    # ===========================REM
    try:
        globalEngine.update_sensorloc()
        map = globalEngine.get_heat_map()
    except:
        pass
    Img0 = map
    loc_sen = globalEngine.SensorLoc

    plt.figure(2)
    plt.cla()
    plt.imshow(Img0, origin='lower', interpolation='nearest', vmin=-50, vmax=-10)
    plt.scatter(loc_sen[:, 1].T / myglobals.PixelResolution,
                loc_sen[:, 0].T / myglobals.PixelResolution, color='b')
    plt.pause(0.00000000000001)



sensingtime = (time.time() - start)
print('average time',sensingtime/mm)
plt.show()

