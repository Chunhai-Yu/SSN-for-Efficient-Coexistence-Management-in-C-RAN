
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


def find_variogram(Dist,Pow_vec,Bin_bound):
    N=Dist.shape[0]
    flag=np.ones((N,N))
    Variogram = np.zeros(len(Bin_bound))
    Histogram = np.zeros(len(Bin_bound))
    ti=0
    for i in range(0,len(Bin_bound)):
        tz=Bin_bound[i]

        tsum = 0
        tnum = 0
        for tx in range(0,N):
            for ty in range(0,N):
                if (Dist[tx,ty]<=tz and flag[tx,ty]==1):
                    tnum=tnum+1
                    tsum=tsum+(Pow_vec[0,tx]-Pow_vec[0,ty])**2
                    flag[tx,ty]=0
        if tnum==0:
            Variogram[ti]=-1
        else:

            Variogram[ti] = (1 / 2 / tnum) * tsum

        Histogram[ti] = tnum
        #print(Histogram[ti])
        #print(tsum)
        ti = ti + 1



    ind_nonzero=np.where(Variogram > 0)[0]
    Variogram2=Variogram[ind_nonzero]
    Bin_bound2=Bin_bound[ind_nonzero]



    return Variogram2,Bin_bound2