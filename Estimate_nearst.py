#
import numpy as np
import scipy.optimize as opt
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.linalg import solve
#
from SSN_modul.Sensors import Sensors
from SSN_modul.Cluster import Cluster
from SSN_modul.Generate_sensor_locations import generate_sensor_locations
from SSN_modul.Find_pairwise_distance import find_pairwise_distance
from SSN_modul.Get_distance import get_distance
from SSN_modul.Find_variogram import find_variogram
from SSN_modul import myglobals
from SSN_modul.Fit_function import Gaussian_modul
from SSN_modul.Fit_function import Spherical_modul
from SSN_modul.Fit_function import Exponent_modul

from SSN_modul.Generate_matrices import generate_matrices
from SSN_modul.Pixel2coord import pixel2coord
from SSN_modul.Sources import Sources
from SSN_modul.prx_analog import data_log

#
from SSN_modul.Coord2pixel import coord2pixel
from SSN_modul.Pixel2coord import pixel2coord
from SSN_modul.Find_pairwise_distance import find_pairwise_distance
from SSN_modul.prx_analog import data_log

def estimate_map_nearst_method(N,Locations,Prx,PixelRange):  # for each point, use nearst N sensors

    Pos = Locations
    flag = 0
    Pow = Prx

    rang = PixelRange
    img = np.zeros((int(rang[1]) - int(rang[0]) + 1, int(rang[3]) - int(rang[2]) + 1))
    for i in range(0, img.shape[0]):
        tx = rang[0] + i
        for j in range(0, img.shape[1]):
            ty = rang[2] + j
            pxcoord = np.array([tx, ty])
            coord = pixel2coord(pxcoord)
            sen_dis = []

            for ii in range(0, Pos.shape[0]):
                dis = get_distance(coord, Pos[ii, :])
                # if dis==0:
                #     flag=1
                #     img[i,j]=Pow[0,ii]
                #     break
                # if dis==0:
                #     dis=0.00000000001
                sen_dis.append(dis)
            # if flag==1:
            #     continue
            sen_dis = np.array(sen_dis)
            num = np.argsort(sen_dis)

            pos = np.zeros((N, 2))
            pow = np.zeros((1, N))
            for kk in range(0, N):
                pos[kk, :] = Pos[num[kk], :]
                pow[0, kk] = Pow[0, num[kk]]

            dij, tmean = find_pairwise_distance(pos)


            rij = np.zeros((pow.shape[1], pow.shape[1]))
            for k in range(0, pow.shape[1]):
                rij[k, :] = 0.5 * (pow[0, k] - pow) * (pow[0, k] - pow)
            # # # calculate mean-value of variogram that under same distance
            # dd = []
            # semi = []
            # for n in range(0, dij.shape[0]):
            #     for m in range(0, dij.shape[1]):
            #         if n == m:
            #             continue
            #         else:
            #             lo = np.argwhere(dij == dij[n, m])
            #             dd.append(dij[n, m])
            #             se = []
            #             for l in range(0, lo.shape[0]):
            #                 se.append(rij[lo[l, 0], lo[l, 1]])
            #             semi.append(np.sum(se) / lo.shape[0])
            # Bin_bound = dd
            # Variogram = semi

            # # calculate variogram directly
            dd = dij.reshape(1, pow.shape[1] * pow.shape[1])
            semi = rij.reshape(1, pow.shape[1] * pow.shape[1])
            Bin_bound = dd[0]
            Variogram = semi[0]

            ###########

            # if Variogram[len(Variogram) - 1] < Variogram[0]:
            #     Variogram = Variogram[0:len(Variogram) - 1]
            #     Bin_bound = Bin_bound[0:len(Bin_bound) - 1]
            ###########


            pg1, pg2, pg3 = opt.curve_fit(Exponent_modul, Bin_bound, Variogram, bounds=([0,0,0],[np.inf,np.inf,np.inf]),method='trf')[0]
            # pg1, pg2, pg3 = opt.curve_fit(Spherical_modul, Bin_bound, Variogram)[0]
            p = [pg1, pg2, pg3]
            A, B = generate_matrices(p, dij, pos, coord)
            W = solve(A, B)
            W = W[0:pow.shape[1], 0].T
            img[i, j] = sum(sum(W * pow))
    return img