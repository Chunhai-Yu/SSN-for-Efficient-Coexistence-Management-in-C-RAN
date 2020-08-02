## here we use received_power2
# received_power2 is used to calculate averaged psd and power for N times samples.
# psd: the sampled psd matrix, f: frequency area of samples, figurhandler: to show the averaged results, here not used,
# M: number of frequency bins to calculate psd and power
import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
def received_power(psd,f,figurhandler):
    N=psd.shape[0] # times of psd_samples
    M=f.shape[0] # number of frequency points
    delta_f=(f[-1]-f[0])/(M-1)

    Pow=np.zeros((1,M-1))
    pow_data=psd[:,0:M-1]*delta_f
    for i in range(0,pow_data.shape[1]):
        hist, bin_edges = np.histogram(pow_data[:,i].T, bins='auto', density=False)
        lotbin = np.argwhere(hist == np.max(hist))[0][0]
        bin_pow=(bin_edges[lotbin]+bin_edges[lotbin+1])/2
        Pow[0,i]=bin_pow

    Power=np.sum(Pow)

    #reconstruct PSD
    Psd=10 * np.log10(Pow[0] / (delta_f))
    # plot new psd
    plt.figure(figurhandler)
    plt.plot(f[0:M-1],Psd)
    plt.grid(True)



    return Power,Psd


def received_power2(psd,f,figurhandler,M):
    # N=psd.shape[0] # times of psd_samples
    M=M # number of frequency bins to calculate power
    #M=64
    delta_f=(np.max(f)-np.min(f))/M


    Pow=np.zeros((1,M))
    loc=np.arange(0,psd.shape[1]-1,psd.shape[1]/M,dtype='int') # make sure loc is int-type, because the index of matrix must be integer

    pow_data=psd[:,loc]*delta_f
    #start=time.time()
    # #
    # # use Histgram to get averaged psd and power
    for i in range(0,pow_data.shape[1]):
        hist, bin_edges = np.histogram(pow_data[:,i].T, bins='auto', density=False)
        lotbin = np.argwhere(hist == np.max(hist))[0][0]
        bin_pow=(bin_edges[lotbin]+bin_edges[lotbin+1])/2
        Pow[0,i]=bin_pow
    # #
    #his_t=time.time()-start
    #print('histogram',his_t)
    #
    Power=np.sum(Pow)
    #Power=np.sum(pow_data[0])

    Power=10 * np.log10(Power)

    #reconstruct PSD

    #Psd=10 * np.log10(Pow[0] / (delta_f))
    Psd=10 * np.log10(pow_data[0] / (delta_f))

    # # plot new psd, to show the averaged results
    # plt.figure(figurhandler)
    # plt.plot(f[loc],Psd)
    # print(Psd.shape)
    # plt.grid(True)
    # plt.title('average psd')
    f_new=f[loc]



    return Power,Psd,f_new
