## to test the time-cost T for parallel(threding) samples.
# here i use two sensors, and each sensor is sampled for NN=100 times, the output is the average time-cost
# to get powers from sensor1 and sensor2 for one time
# the sampled values are stored in myglobals.power1 and myglobals.power2, it can be used in kriging in future


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

# Get a list of detected device serial numbers (str)
serial_numbers = RtlSdr.get_device_serial_addresses()

#---------------------------------------------------------first sensor
# Find the device index for a given serial number
device_index0 = RtlSdr.get_device_index_by_serial(serial_numbers[0])
sdr0 = RtlSdr(device_index0)
sdr0.sample_rate = 3.2e6
sdr0.center_freq = 1600*1e6
sdr0.gain = 4
#---------------------------------------------------------second sensor
device_index1 = RtlSdr.get_device_index_by_serial(serial_numbers[1])
sdr1 = RtlSdr(device_index1)
sdr1.sample_rate = 3.2e6
sdr1.center_freq = 1600*1e6
sdr1.gain = 4
N = 1
M=128
NN=100
def receive_power1():
    rec=NN # time of samples
    while rec:
        rec=rec-1
        raw_data = np.zeros((N, 1024))
        for ii in range(0, N):
            samples = sdr0.read_samples(56 * 1024)  # 256
            # use matplotlib to estimate and plot the PSD
            p_density, fre = selfpsd(samples, NFFT=1024, Fs=sdr0.sample_rate, Fc=sdr0.center_freq)
            #p_density, fre = plt.psd(samples, NFFT=1024, Fs=sdr0.sample_rate, Fc=sdr0.center_freq)

            raw_data[ii, :] = p_density

        figurhandler = 12
        re_pow, new_psd = received_power2(raw_data, fre, figurhandler,M)
        myglobals.power1.append(re_pow)
        #print('pow1', re_pow)
    return

def receive_power2():
    rec=NN
    while rec:
        rec=rec-1
        raw_data = np.zeros((N, 1024))
        for ii in range(0, N):
            samples = sdr1.read_samples(56 * 1024)  # 256
            # use matplotlib to estimate and plot the PSD
            p_density, fre = selfpsd(samples, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)
            #p_density, fre = plt.psd(samples, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)

            raw_data[ii, :] = p_density

        figurhandler = 12
        re_pow, new_psd = received_power2(raw_data, fre, figurhandler,M)
        myglobals.power2.append(re_pow)
        #print('pow2',re_pow)
    return

# def fetch_pow():
#     fet=10
#     while fet:
#         #fet=fet-1
#         myglobals.POW1.append(myglobals.power1[-1])
#         myglobals.POW2.append(myglobals.power2[-1])
#         print('myglobals.POW1', myglobals.POW1)
#         print('myglobals.POW2', myglobals.POW2)

#if __name__ == '__main__':
s1 = threading.Thread(name='sensor 1', target=receive_power1)
s2 = threading.Thread(name='sensor 2', target=receive_power2)
#fetch = threading.Thread(name='fetch powers', target=fetch_pow)
start = time.time()
s1.start()
s2.start()
#fetch.start()
s1.join()
s2.join()
#fetch.join()
sensingtime= (time.time() - start)
print(sensingtime/100)