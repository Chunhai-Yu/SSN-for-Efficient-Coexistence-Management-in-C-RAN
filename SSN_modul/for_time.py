#
import numpy as np
import scipy.optimize as opt
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.linalg import solve
from scipy.interpolate import griddata

#
from SSN_modul.Get_distance import get_distance
from SSN_modul.Find_variogram import find_variogram
from SSN_modul import myglobals
from SSN_modul.Fit_function import Gaussian_modul
from SSN_modul.Fit_function import Spherical_modul
from SSN_modul.Fit_function import Exponent_modul
from SSN_modul.Generate_matrices import generate_matrices
from SSN_modul.Estimate_nearst import estimate_map_nearst_method
#
from SSN_modul.Coord2pixel import coord2pixel
from SSN_modul.Pixel2coord import pixel2coord
from SSN_modul.Find_pairwise_distance import find_pairwise_distance
from SSN_modul.prx_analog import data_log
from SSN_modul.prx_analog import data_average
from SSN_modul.prx_analog import data_for_true_cor
from SSN_modul.LS_location import LS_loc
import timeit
import time

# picture(MM,method,SS,flag,vari,receive,sensorlocations)
# MM: number of sensors, method: interpolation method, SS: number of nearest sensors, here doesn't use
# flag: 1--use interpolation to get estimated REM, 0--use nearest method to get REM, -1--true REM
# vari: 'pbp'--point by point method to get variogram, 'bin'--equal space method to get variogram


def fortime(receive,sensorlocations):#,sensorlocations
    area_size = myglobals.area_size#[10, 5]
    xrange = [0, area_size[0]]
    yrange = [0, area_size[1]]
    Range = np.array([xrange[0], xrange[1], yrange[0], yrange[1]])
    PixelRange = coord2pixel(Range) + [1, 0, 1, 0]

    Source_loc = myglobals.loc_source#[3, 4]
    Ptx = myglobals.Ptx#-10
    #MM = MM



    Locations=sensorlocations


    tdist, tmean = find_pairwise_distance(Locations)
    Dist = tdist
    # make sure different methods will process same data

    if all(receive[0]==0):
        #Prx = data_average(Dist, Source_loc, Locations, Ptx) # for LS, no sense to Kriging
        Prx = data_log(Dist, Source_loc, Locations, Ptx)

    else:
        Prx=receive




    # use different interpolation methods to get REM
    def estimate_map(Prx, Locations):
        Pow = Prx
        tdist, tmean = find_pairwise_distance(Locations)
        Dist = tdist

        ## pbp method
        rij = np.zeros((Pow.shape[1], Pow.shape[1]))
        for i in range(0, Pow.shape[1]):
            rij[i, :] = 0.5 * (Pow[0, i] - Pow) * (Pow[0, i] - Pow)

        dij = Dist

        # # calculate variogram directly
        dd=dij.reshape(1,Pow.shape[1]*Pow.shape[1])
        semi=rij.reshape(1,Pow.shape[1]*Pow.shape[1])
        Bin_bound = dd[0]
        Variogram = semi[0]


        # ### bin method
        # VarResolution = 1
        # rang = Range
        # MaxDist = get_distance(np.array([rang[0], rang[2]]), np.array([rang[1], rang[3]]))
        # bins = np.arange(0, MaxDist + VarResolution, VarResolution) + VarResolution
        # Pow = Pow
        # Variogram, Bin_bound = find_variogram(Dist, Pow, bins)


        # get coefficients for the Gaussian model
        #, bounds=([0,0,0],[np.inf,np.inf,np.inf]),method='trf'
        pg1, pg2, pg3 = opt.curve_fit(Exponent_modul, Bin_bound, Variogram, bounds=([0,0,0],[np.inf,np.inf,np.inf]),method='trf')[0]#bounds=([-np.inf,0,-np.inf,], [np.inf,np.inf,np.inf])
        #pg1, pg2, pg3 = opt.curve_fit(Spherical_modul, Bin_bound, Variogram)[0]
        p = [pg1, pg2, pg3]
        rang = PixelRange

        # to get the estimated map
        img = np.zeros((int(rang[1]) - int(rang[0]) + 1, int(rang[3]) - int(rang[2]) + 1))
        for i in range(0, img.shape[0]):
            tx = rang[0] + i
            for j in range(0, img.shape[1]):
                ty = rang[2] + j
                pxcoord = np.array([tx, ty])
                coord = pixel2coord(pxcoord)

                # Kriging_method
                # Pow = Prx
                Pos = Locations
                A, B = generate_matrices(p, Dist, Pos, coord)
                W = solve(A, B)
                W = W[0:Pow.shape[1], 0].T
                # print(np.sum(np.sum(W)))
                Pow_est = np.sum(np.sum(W * Pow))
                img[i, j] = Pow_est


        Img = img
        return Img



    #
    start = time.time()
    Img = estimate_map(Prx, Locations)
    krigingtime= (time.time() - start)






    IMG = Img


    return IMG, Prx, krigingtime