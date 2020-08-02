# test code for calculating received power of any sensor.

from rtlsdr import *
import scipy.signal as signal
from numpy import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import time
import numpy as np
from SSN_modul.Received_power import received_power
from SSN_modul.Received_power import received_power2
from SSN_modul.self_psd import selfpsd

# Get a list of detected device serial numbers (str)
serial_numbers = RtlSdr.get_device_serial_addresses()
print('serial_numbers:',serial_numbers)
#---------------------------------------------------------first sensor
# Find the device index for a given serial number
device_index0 = RtlSdr.get_device_index_by_serial(serial_numbers[0]) # here is the first sensor
print('choosed device index:',device_index0)
sdr1 = RtlSdr(device_index0)
sdr1.sample_rate = 1e6
sdr1.center_freq = 434*1e6
sdr1.gain = 1
# second sensor
device_index1 = RtlSdr.get_device_index_by_serial(serial_numbers[1]) # here is the first sensor
print('choosed device index:',device_index1)
sdr2 = RtlSdr(device_index1)
sdr2.sample_rate = 1e6
sdr2.center_freq = 434*1e6
sdr2.gain = 1

#--------------------------- use github

N=1 # times of sample PSD values
#raw_data=zeros((N,1024))

while 1:

    for ii in range(0,N):

        #start = time.time()
        samples1 = sdr1.read_samples(56 * 1024)#256
        #sensingtime1 = (time.time() - start)
        #print('time for read_sample:',sensingtime1)


        # use matplotlib to estimate and plot the PSD
        plt.figure(1)
        #start = time.time()
        plt.cla()
        #p_density, fre = plt.psd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq) # get psd using github package


        #print(np.max(20*np.log(p_density)))

        p_density, fre = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq) # get psd using own function
        re_pow1, new_psd1, f_new1 = received_power2(p_density, fre, 1, 128)
        # # sensingtime2 = (time.time() - start)
        # # print('time for get psd:',sensingtime2)
        # p_density=10 * np.log10(p_density)
        # plt.plot(fre,p_density)
        # plt.xlabel('Frequency (MHz)')
        # plt.ylabel('Relative power (dB)')
        # plt.title('using own psd_code')
        #plt.pause(0.001)




        #raw_data[ii,:]=p_density
        samples2 = sdr2.read_samples(56 * 1024)
        plt.figure(2)
        plt.cla()
        p_density, fre = plt.psd(samples2, NFFT=1024, Fs=sdr2.sample_rate, Fc=sdr2.center_freq)  # get psd using github package
        # print(np.max(20*np.log(p_density)))
        plt.pause(0.001)

plt.show()
# ##plt.close(1)
# #plt.title('using rtl-sdr package psd_code')
# figurhandler=12
# start = time.time()
# M=128 # number of frequency bins to calculate average_psd and power, it should be smaller than number of frequency points
# re_pow,new_psd=received_power2(raw_data,fre,figurhandler,M)
# sensingtime3 = (time.time() - start)
# print('time for get received power:',sensingtime3)
#
# print('power:',re_pow)

# #plt.show()
# p_density=10 * np.log10(p_density)
# plt.plot(fre,p_density)
# plt.xlabel('Frequency (MHz)')
# plt.ylabel('Relative power (dB)')
# plt.title('using own psd_code')
# plt.show()



