# test code for calculating received power of any sensor.
# draw error pictures

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from SSN_modul.v5_pic import picture
from SSN_modul.Generate_sensor_locations import generate_sensor_locations
from SSN_modul import myglobals
from SSN_modul.Get_distance import get_distance
import math
from SSN_modul.for_time import fortime


from rtlsdr import *
import scipy.signal as signal

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import time
import numpy as np
from SSN_modul.Received_power import received_power
from SSN_modul.Received_power import received_power2
from SSN_modul.self_psd import selfpsd
from SSN_modul.v5_pic import picture

# # Get a list of detected device serial numbers (str)
# serial_numbers = RtlSdr.get_device_serial_addresses()
# print('serial_numbers:',serial_numbers)

#first sensor

sdr0 = RtlSdr(serial_number='10')
sdr0.sample_rate = 1e6
sdr0.center_freq = 434*1e6
sdr0.gain = 1
# second sensor

sdr1 = RtlSdr(serial_number='11')
sdr1.sample_rate = 1e6
sdr1.center_freq = 434*1e6
sdr1.gain = 1
# third sensor

sdr2 = RtlSdr(serial_number='14')
sdr2.sample_rate = 1e6
sdr2.center_freq = 434*1e6
sdr2.gain = 1
# fourth sensor

sdr3 = RtlSdr(serial_number='15')
sdr3.sample_rate = 1e6
sdr3.center_freq = 434*1e6
sdr3.gain = 1
# fifth sensor

sdr4 = RtlSdr(serial_number='16')
sdr4.sample_rate = 1e6
sdr4.center_freq = 434*1e6
sdr4.gain = 1

#--------------------------- use github

N=1 # times of sample PSD values
raw_data0=np.zeros((N,1024))
raw_data1=np.zeros((N,1024))
raw_data2=np.zeros((N,1024))
raw_data3=np.zeros((N,1024))
raw_data4=np.zeros((N,1024))
fre0=0
fre1=0
fre2=0
fre3=0
fre4=0


while 1:

    for ii in range(0,N):

        samples0 = sdr0.read_samples(56 * 1024)#256
        p_density0, fre0 = selfpsd(samples0, NFFT=1024, Fs=sdr0.sample_rate, Fc=sdr0.center_freq) # get psd using own function
        raw_data0[ii,:]=p_density0

        samples1 = sdr1.read_samples(56 * 1024)  # 256
        p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)  # get psd using own function
        raw_data1[ii, :] = p_density1

        samples2 = sdr2.read_samples(56 * 1024)  # 256
        p_density2, fre2 = selfpsd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)  # get psd using own function
        raw_data2[ii, :] = p_density2

        samples3 = sdr3.read_samples(56 * 1024)  # 256
        p_density3, fre3 = selfpsd(samples3, NFFT=1024, Fs=sdr3.sample_rate, Fc=sdr3.center_freq)  # get psd using own function
        raw_data3[ii, :] = p_density3

        samples4 = sdr4.read_samples(56 * 1024)  # 256
        p_density4, fre4 = selfpsd(samples4, NFFT=1024, Fs=sdr4.sample_rate, Fc=sdr4.center_freq)  # get psd using own function
        raw_data4[ii, :] = p_density4

    re_pow0, new_psd0, f_new0 = received_power2(raw_data0, fre0, 1, 128)
    re_pow1, new_psd1, f_new1 = received_power2(raw_data1, fre1, 1, 128)
    re_pow2, new_psd2, f_new2 = received_power2(raw_data2, fre2, 1, 128)
    re_pow3, new_psd3, f_new3 = received_power2(raw_data3, fre3, 1, 128)
    re_pow4, new_psd4, f_new4 = received_power2(raw_data4, fre4, 1, 128)

    sensorlocations = generate_sensor_locations(5, [0, 10, 0, 5])
    Prx=np.zeros((1,5))

    Prx[0, 0] = re_pow0
    Prx[0, 1] = re_pow1
    Prx[0, 2] = re_pow2
    Prx[0, 3] = re_pow3
    Prx[0, 4] = re_pow4

    pbpValue, receive = picture('kriging', 1, 1, 'pbp', Prx, sensorlocations)
    plt.figure(1)
    plt.imshow(pbpValue, origin='lower', interpolation='nearest')


    plt.figure(2)
    plt.cla()
    plt.plot(f_new0,new_psd0)


    plt.pause(0.01)



plt.show()






