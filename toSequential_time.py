# to test the time-cost T for one sensor for one-time sample. if we get sensor-powers one by one,
# the total time-cost is equal to sensor_number*T

from rtlsdr import *
import scipy.signal as signal
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import time
from SSN_modul.Received_power import received_power
from SSN_modul.Received_power import received_power2
from SSN_modul.self_psd import selfpsd

NN=10 #
Tim=0
# Get a list of detected device serial numbers (str)
serial_numbers = RtlSdr.get_device_serial_addresses()
#---------------------------------------------------------first sensor
# Find the device index for a given serial number
device_index0 = RtlSdr.get_device_index_by_serial(serial_numbers[0])
sdr = RtlSdr(device_index0)
sdr.sample_rate = 3.2e6
sdr.center_freq = 1600*1e6
sdr.gain = 4
#
#--------------------------- use github
sensingtime=0
for gg in range(0,NN):
    start = time.time()
    N = 1
    raw_data = np.zeros((N, 1024))


    for ii in range(0, N):

        samples = sdr.read_samples(56 * 1024)  # 256

        # use matplotlib to estimate and plot the PSD
        #plt.figure(1)
        p_density, fre = selfpsd(samples, NFFT=1024, Fs=sdr.sample_rate, Fc=sdr.center_freq)

        raw_data[ii, :] = p_density
    #plt.close(1)
    figurhandler = 12
    M=128
    re_pow, new_psd = received_power2(raw_data, fre, figurhandler,M)
    sensingtime = (time.time() - start)
    Tim=Tim+sensingtime

Tim=Tim/NN
print(Tim)



# NN=100 # locations of source
# Nmx=np.array([3,4,5,6])
# Nmy=np.array([3,4,5,6])
# #MM=(Nmx-1)*(Nmy-1) # number of sensors method 1
# MM=Nmx*Nmy # number of sensors method 2
# #MM=[15,20,25,30,35]
#
# nn=0 # number of successful simulations
# # RMSE for different methods
# Tim=np.zeros((1,len(MM)))
# # Get a list of detected device serial numbers (str)
# serial_numbers = RtlSdr.get_device_serial_addresses()
# print(serial_numbers)
# # ---------------------------------------------------------first sensor
# # Find the device index for a given serial number
# device_index0 = RtlSdr.get_device_index_by_serial(serial_numbers[0])
# print(device_index0)
# sdr = RtlSdr(device_index0)
#
# for j in range(0,NN):
#     print(j)
#     #sensorlocation=generate_sensor_locations(50,[0,xmax,0,ymax])# (SensorsPerCluster, Range)
#     tim=[]
#     for i in range(0, len(MM)):
#         print([j,i])
#         # configure device
#         sdr.sample_rate = 3.2e6
#         sdr.center_freq = 602e6
#         sdr.gain = 4
#         # help(plt.psd)
#         start = time.time()
#         for k in range(1,MM[i]+1):
#
#
#             # --------------------------- use github
#
#             N = 1
#             raw_data = np.zeros((N, 1024))
#             for ii in range(0, N):
#                 samples = sdr.read_samples(56 * 1024)
#                 # use matplotlib to estimate and plot the PSD
#                 plt.figure(1)
#                 p_density, fre = plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate , Fc=sdr.center_freq )
#
#                 raw_data[ii, :] = p_density
#             # plt.close(1)
#             figurhandler = 12
#             re_pow, new_psd = received_power2(raw_data, fre, figurhandler)
#
#         sensingtime = (time.time() - start)
#         tim.append(sensingtime)
#
#     Tim=Tim+np.array(tim)
#
# Tim=Tim/NN
# print(Tim)
