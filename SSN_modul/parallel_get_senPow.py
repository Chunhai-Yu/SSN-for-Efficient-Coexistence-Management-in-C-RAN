## to test the time-cost T for parallel(threding) samples.
# here i use two sensors, and each sensor is sampled for NN=100 times, the output is the average time-cost
# to get powers from sensor1 and sensor2 for one time
# the sampled values are stored in myglobals.power1 and myglobals.power2, it can be used in kriging in future

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

def parallel_sensor_power():

    N = 1
    Nu = 56
    M = 256# 512 best
    gain0=myglobals.gain
    # Get a list of detected device
    #first sensor
    sdr0 = RtlSdr(serial_number='10')
    sdr0.sample_rate = myglobals.sample_rate
    sdr0.center_freq = myglobals.center_freq
    sdr0.gain = gain0
    # second sensor
    sdr1 = RtlSdr(serial_number='11')
    sdr1.sample_rate = myglobals.sample_rate
    sdr1.center_freq = myglobals.center_freq
    sdr1.gain = gain0
    # third sensor
    sdr2 = RtlSdr(serial_number='12')
    sdr2.sample_rate = myglobals.sample_rate
    sdr2.center_freq = myglobals.center_freq
    sdr2.gain = gain0
    # fourth sensor
    sdr3 = RtlSdr(serial_number='13')
    sdr3.sample_rate = myglobals.sample_rate
    sdr3.center_freq = myglobals.center_freq
    sdr3.gain = gain0
    # fifth sensor
    sdr4 = RtlSdr(serial_number='14')
    sdr4.sample_rate = myglobals.sample_rate
    sdr4.center_freq = myglobals.center_freq
    sdr4.gain = gain0
    # sixth
    sdr5 = RtlSdr(serial_number='15')
    sdr5.sample_rate = myglobals.sample_rate
    sdr5.center_freq = myglobals.center_freq
    sdr5.gain = gain0
    # seventh
    sdr6 = RtlSdr(serial_number='16')
    sdr6.sample_rate = myglobals.sample_rate
    sdr6.center_freq = myglobals.center_freq
    sdr6.gain = gain0
    # 8
    sdr7 = RtlSdr(serial_number='17')
    sdr7.sample_rate = myglobals.sample_rate
    sdr7.center_freq = myglobals.center_freq
    sdr7.gain = gain0
    # 9
    sdr8 = RtlSdr(serial_number='18')
    sdr8.sample_rate = myglobals.sample_rate
    sdr8.center_freq = myglobals.center_freq
    sdr8.gain = gain0
    # 10
    sdr9 = RtlSdr(serial_number='19')
    sdr9.sample_rate = myglobals.sample_rate
    sdr9.center_freq = myglobals.center_freq
    sdr9.gain = gain0
    # 11
    sdr10 = RtlSdr(serial_number='20')
    sdr10.sample_rate = myglobals.sample_rate
    sdr10.center_freq = myglobals.center_freq
    sdr10.gain = gain0
    # 12
    sdr11 = RtlSdr(serial_number='21')
    sdr11.sample_rate = myglobals.sample_rate
    sdr11.center_freq = myglobals.center_freq
    sdr11.gain = gain0
    # 13
    sdr12 = RtlSdr(serial_number='22')
    sdr12.sample_rate = myglobals.sample_rate
    sdr12.center_freq = myglobals.center_freq
    sdr12.gain = gain0
    '''# 14
    sdr13 = RtlSdr(serial_number='23')
    sdr13.sample_rate = myglobals.sample_rate
    sdr13.center_freq = myglobals.center_freq
    sdr13.gain = gain0'''
   

    def receive_power0():

        while 1:
            fre0 = 0
            raw_data0 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples0 = sdr0.read_samples(Nu * 1024)  # 256
                p_density0, fre0 = selfpsd(samples0, NFFT=1024, Fs=sdr0.sample_rate, Fc=sdr0.center_freq)  # get psd using own function
                raw_data0[ii, :] = p_density0


            re_pow0, new_psd0, f_new0 = received_power2(raw_data0, fre0, 1, M)
            myglobals.power_threads[0].append(re_pow0)
            myglobals.psd_threads[0].append(new_psd0)
            myglobals.fre_threads[0].append(f_new0)
            # myglobals.power_threads[0]=re_pow0
            # myglobals.psd_threads[0]=new_psd0
            # myglobals.fre_threads[0]=f_new0
            #print('sensor0')

    def receive_power1():

        while 1:
            fre1 = 0
            raw_data1 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples1 = sdr1.read_samples(Nu * 1024)  # 256
                p_density1, fre1 = selfpsd(samples1, NFFT=1024, Fs=sdr1.sample_rate, Fc=sdr1.center_freq)  # get psd using own function
                raw_data1[ii, :] = p_density1


            re_pow1, new_psd1, f_new1 = received_power2(raw_data1, fre1, 1, M)
            myglobals.power_threads[1].append(re_pow1)
            myglobals.psd_threads[1].append(new_psd1)
            myglobals.fre_threads[1].append(f_new1)
            # myglobals.power_threads[1]=re_pow1
            # myglobals.psd_threads[1]=new_psd1
            # myglobals.fre_threads[1]=f_new1
            #print('sensor1')

    def receive_power2():

        while 1:
            fre2 = 0
            raw_data2 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples2 = sdr2.read_samples(Nu * 1024)  # 256
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

        while 1:
            fre3 = 0
            raw_data3 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples3 = sdr3.read_samples(Nu * 1024)  # 256
                p_density3, fre3 = selfpsd(samples3, NFFT=1024, Fs=sdr3.sample_rate, Fc=sdr3.center_freq)  # get psd using own function
                raw_data3[ii, :] = p_density3


            re_pow3, new_psd3, f_new3 = received_power2(raw_data3, fre3, 1, M)
            myglobals.power_threads[3].append(re_pow3)
            myglobals.psd_threads[3].append(new_psd3)
            myglobals.fre_threads[3].append(f_new3)
            # myglobals.power_threads[3]=re_pow3
            # myglobals.psd_threads[3]=new_psd3
            # myglobals.fre_threads[3]=f_new3
            #print('nothing3')

    def receive_power4():

        while 1:
            fre4 = 0
            raw_data4 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples4 = sdr4.read_samples(Nu * 1024)  # 256
                p_density4, fre4 = selfpsd(samples4, NFFT=1024, Fs=sdr4.sample_rate, Fc=sdr4.center_freq)  # get psd using own function
                raw_data4[ii, :] = p_density4


            re_pow4, new_psd4, f_new4 = received_power2(raw_data4, fre4, 1, M)
            myglobals.power_threads[4].append(re_pow4)
            myglobals.psd_threads[4].append(new_psd4)
            myglobals.fre_threads[4].append(f_new4)
            # myglobals.power_threads[4]=re_pow4
            # myglobals.psd_threads[4]=new_psd4
            # myglobals.fre_threads[4]=f_new4
            #print('nothing4')

    def receive_power5():

        while 1:
            fre5 = 0
            raw_data5 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples5 = sdr5.read_samples(Nu * 1024)  # 256
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

        while 1:
            fre6 = 0
            raw_data6 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples6 = sdr6.read_samples(Nu * 1024)  # 256
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

    def receive_power7():

        while 1:
            fre7 = 0
            raw_data7 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples7 = sdr7.read_samples(Nu * 1024)  # 256
                p_density7, fre7 = selfpsd(samples7, NFFT=1024, Fs=sdr7.sample_rate,
                                           Fc=sdr7.center_freq)  # get psd using own function
                raw_data7[ii, :] = p_density7

            re_pow7, new_psd7, f_new7 = received_power2(raw_data7, fre7, 1, M)
            myglobals.power_threads[7].append(re_pow7)
            myglobals.psd_threads[7].append(new_psd7)
            myglobals.fre_threads[7].append(f_new7)
            # myglobals.power_threads[7]=re_pow7
            # myglobals.psd_threads[7]=new_psd7
            # myglobals.fre_threads[7]=f_new7
            # print('nothing7')

    def receive_power8():

        while 1:
            fre8 = 0
            raw_data8 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples8 = sdr8.read_samples(Nu * 1024)  # 256
                p_density8, fre8 = selfpsd(samples8, NFFT=1024, Fs=sdr8.sample_rate,
                                           Fc=sdr8.center_freq)  # get psd using own function
                raw_data8[ii, :] = p_density8

            re_pow8, new_psd8, f_new8 = received_power2(raw_data8, fre8, 1, M)
            myglobals.power_threads[8].append(re_pow8)
            myglobals.psd_threads[8].append(new_psd8)
            myglobals.fre_threads[8].append(f_new8)
            # myglobals.power_threads[8]=re_pow8
            # myglobals.psd_threads[8]=new_psd8
            # myglobals.fre_threads[8]=f_new8
            # print('nothing8')

    def receive_power9():

        while 1:
            fre9 = 0
            raw_data9 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples9 = sdr9.read_samples(Nu * 1024)  # 256
                p_density9, fre9 = selfpsd(samples9, NFFT=1024, Fs=sdr9.sample_rate,
                                           Fc=sdr9.center_freq)  # get psd using own function
                raw_data9[ii, :] = p_density9

            re_pow9, new_psd9, f_new9 = received_power2(raw_data9, fre9, 1, M)
            myglobals.power_threads[9].append(re_pow9)
            myglobals.psd_threads[9].append(new_psd9)
            myglobals.fre_threads[9].append(f_new9)
            # myglobals.power_threads[9]=re_pow9
            # myglobals.psd_threads[9]=new_psd9
            # myglobals.fre_threads[9]=f_new9
            # print('nothing9')

    def receive_power10():

        while 1:
            fre10 = 0
            raw_data10 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples10 = sdr10.read_samples(Nu * 1024)  # 256
                p_density10, fre10 = selfpsd(samples10, NFFT=1024, Fs=sdr10.sample_rate,
                                             Fc=sdr10.center_freq)  # get psd using own function
                raw_data10[ii, :] = p_density10

            re_pow10, new_psd10, f_new10 = received_power2(raw_data10, fre10, 1, M)
            myglobals.power_threads[10].append(re_pow10)
            myglobals.psd_threads[10].append(new_psd10)
            myglobals.fre_threads[10].append(f_new10)
            # myglobals.power_threads[10]=re_pow10
            # myglobals.psd_threads[10]=new_psd10
            # myglobals.fre_threads[10]=f_new10
            # print('nothing10')

    def receive_power11():

        while 1:
            fre11 = 0
            raw_data11 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples11 = sdr11.read_samples(Nu * 1024)  # 256
                p_density11, fre11 = selfpsd(samples11, NFFT=1024, Fs=sdr11.sample_rate,
                                             Fc=sdr11.center_freq)  # get psd using own function
                raw_data11[ii, :] = p_density11

            re_pow11, new_psd11, f_new11 = received_power2(raw_data11, fre11, 1, M)
            myglobals.power_threads[11].append(re_pow11)
            myglobals.psd_threads[11].append(new_psd11)
            myglobals.fre_threads[11].append(f_new11)
            # myglobals.power_threads[11]=re_pow11
            # myglobals.psd_threads[11]=new_psd11
            # myglobals.fre_threads[11]=f_new11
            # print('nothing11')

    def receive_power12():

        while 1:
            fre12 = 0
            raw_data12 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples12 = sdr12.read_samples(Nu * 1024)  # 256
                p_density12, fre12 = selfpsd(samples12, NFFT=1024, Fs=sdr12.sample_rate,
                                             Fc=sdr12.center_freq)  # get psd using own function
                raw_data12[ii, :] = p_density12

            re_pow12, new_psd12, f_new12 = received_power2(raw_data12, fre12, 1, M)
            myglobals.power_threads[12].append(re_pow12)
            myglobals.psd_threads[12].append(new_psd12)
            myglobals.fre_threads[12].append(f_new12)
            # myglobals.power_threads[12]=re_pow12
            # myglobals.psd_threads[12]=new_psd12
            # myglobals.fre_threads[12]=f_new12
            # print('nothing12')

    def receive_power13():

        while 1:
            fre13 = 0
            raw_data13 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples13 = sdr13.read_samples(56 * 1024)  # 256
                p_density13, fre13 = selfpsd(samples13, NFFT=1024, Fs=sdr13.sample_rate,
                                             Fc=sdr13.center_freq)  # get psd using own function
                raw_data13[ii, :] = p_density13

            re_pow13, new_psd13, f_new13 = received_power2(raw_data13, fre13, 1, M)
            myglobals.power_threads[13].append(re_pow13)
            myglobals.psd_threads[13].append(new_psd13)
            myglobals.fre_threads[13].append(f_new13)
            # myglobals.power_threads[13]=re_pow13
            # myglobals.psd_threads[13]=new_psd13
            # myglobals.fre_threads[13]=f_new13
            # print('nothing13')

    def receive_power14():

        while 1:
            fre14 = 0
            raw_data14 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples14 = sdr14.read_samples(56 * 1024)  # 256
                p_density14, fre14 = selfpsd(samples14, NFFT=1024, Fs=sdr14.sample_rate,
                                             Fc=sdr14.center_freq)  # get psd using own function
                raw_data14[ii, :] = p_density14

            re_pow14, new_psd14, f_new14 = received_power2(raw_data14, fre14, 1, M)
            myglobals.power_threads[14].append(re_pow14)
            myglobals.psd_threads[14].append(new_psd14)
            myglobals.fre_threads[14].append(f_new14)
            # myglobals.power_threads[14]=re_pow14
            # myglobals.psd_threads[14]=new_psd14
            # myglobals.fre_threads[14]=f_new14
            # print('nothing14')

    def receive_power15():

        while 1:
            fre15 = 0
            raw_data15 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples15 = sdr15.read_samples(56 * 1024)  # 256
                p_density15, fre15 = selfpsd(samples15, NFFT=1024, Fs=sdr15.sample_rate,
                                             Fc=sdr15.center_freq)  # get psd using own function
                raw_data15[ii, :] = p_density15

            re_pow15, new_psd15, f_new15 = received_power2(raw_data15, fre15, 1, M)
            myglobals.power_threads[15].append(re_pow15)
            myglobals.psd_threads[15].append(new_psd15)
            myglobals.fre_threads[15].append(f_new15)
            # myglobals.power_threads[15]=re_pow15
            # myglobals.psd_threads[15]=new_psd15
            # myglobals.fre_threads[15]=f_new15
            # print('nothing15')

    def receive_power16():

        while 1:
            fre16 = 0
            raw_data16 = np.zeros((N, 1024))
            for ii in range(0, N):
                samples16 = sdr16.read_samples(56 * 1024)  # 256
                p_density16, fre16 = selfpsd(samples16, NFFT=1024, Fs=sdr16.sample_rate,
                                             Fc=sdr16.center_freq)  # get psd using own function
                raw_data16[ii, :] = p_density16

            re_pow16, new_psd16, f_new16 = received_power2(raw_data16, fre16, 1, M)
            myglobals.power_threads[16].append(re_pow16)
            myglobals.psd_threads[16].append(new_psd16)
            myglobals.fre_threads[16].append(f_new16)
            # myglobals.power_threads[16]=re_pow16
            # myglobals.psd_threads[16]=new_psd16
            # myglobals.fre_threads[16]=f_new16
            # print('nothing16')


    #if __name__ == '__main__':
    s0 = threading.Thread(name='sensor 0', target=receive_power0)
    s1 = threading.Thread(name='sensor 1', target=receive_power1)
    s2 = threading.Thread(name='sensor 2', target=receive_power2)
    s3 = threading.Thread(name='sensor 3', target=receive_power3)
    s4 = threading.Thread(name='sensor 4', target=receive_power4)
    s5 = threading.Thread(name='sensor 5', target=receive_power5)
    s6 = threading.Thread(name='sensor 6', target=receive_power6)
    s7 = threading.Thread(name='sensor 7', target=receive_power7)
    s8 = threading.Thread(name='sensor 8', target=receive_power8)
    s9 = threading.Thread(name='sensor 9', target=receive_power9)
    s10 = threading.Thread(name='sensor 10', target=receive_power10)
    s11 = threading.Thread(name='sensor 11', target=receive_power11)
    s12 = threading.Thread(name='sensor 12', target=receive_power12)
    #s13 = threading.Thread(name='sensor 13', target=receive_power13)
   

    s0.start()
    s1.start()
    s2.start()
    s3.start()
    s4.start()
    s5.start()
    s6.start()
    s7.start()
    s8.start()
    s9.start()
    s10.start()
    s11.start()
    s12.start()
    #s13.start()

    
