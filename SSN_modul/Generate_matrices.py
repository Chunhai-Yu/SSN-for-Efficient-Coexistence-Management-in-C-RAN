#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
#
from SSN_modul.Fit_function import Gaussian_modul
from SSN_modul.Fit_function import Exponent_modul
from SSN_modul.Get_distance import get_distance
#
def generate_matrices(p,Dist,Pos_vec,coord):
    N = Dist.shape[0]
    pad_col = np.ones((N + 1, 1))
    pad_col[-1] = 0
    pad_row = np.ones((1,N))
    B = pad_col
    B[-1] = 1
    d1 = Dist.reshape(1, N * N)
    #SEMI2 = [Spherical_modul(i, ps1, ps2, ps3) for i in dd]
    semi = Exponent_modul(d1[0], p[0], p[1], p[2])


    # #===to check fit curves
    # plt.figure(30)
    # plt.scatter(d1[0], semi)
    # plt.xlabel('distance[m]')
    # plt.ylabel('Semivariance')
    # plt.title('Sample Semivariogram')
    # #===

    semi = semi.reshape(N, N)
    #semi = semi + np.eye(semi.shape[1], dtype=int) * 0.000000000000001

    semi1=np.vstack((semi, pad_row))
    A=np.hstack((semi1,pad_col))

    for tx in range(0,N):
        d2=get_distance(coord,Pos_vec[tx,:])
        B[tx,0]=Exponent_modul(d2, p[0], p[1], p[2])



    return A,B