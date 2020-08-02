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
import time
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
from rtlsdr import *
import scipy.signal as signal
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
sdr0.center_freq = 602e6
sdr0.gain = 4

device_index1 = RtlSdr.get_device_index_by_serial(serial_numbers[1])
sdr1 = RtlSdr(device_index1)
sdr1.sample_rate = 3.2e6
sdr1.center_freq = 602e6
sdr1.gain = 4
N = 1
M=128
def receive_power1():
    rec=100
    while rec:
        rec=rec-1
        raw_data = np.zeros((N, 1024))
        for ii in range(0, N):
            samples = sdr0.read_samples(56 * 1024)  # 256
            # use matplotlib to estimate and plot the PSD
            p_density, fre = selfpsd(samples, NFFT=1024, Fs=sdr0.sample_rate, Fc=sdr0.center_freq, detrend=None, window=None, noverlap=None, pad_to=None,sides=None, scale_by_freq=None)
            #p_density, fre = plt.psd(samples, NFFT=1024, Fs=sdr0.sample_rate, Fc=sdr0.center_freq)

            raw_data[ii, :] = p_density

        figurhandler = 12
        re_pow, new_psd = received_power2(raw_data, fre, figurhandler,M)
        myglobals.power1.append(re_pow)
        #print('pow1', re_pow)
    return

def receive_power2():
    rec=100
    while rec:
        rec=rec-1
        raw_data = np.zeros((N, 1024))
        for ii in range(0, N):
            samples = sdr1.read_samples(56 * 1024)  # 256
            # use matplotlib to estimate and plot the PSD
            p_density, fre = selfpsd(samples, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq, detrend=None,
                                     window=None, noverlap=None, pad_to=None, sides=None, scale_by_freq=None)
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
sensingtime1 = (time.time() - start)
print(sensingtime1/100)