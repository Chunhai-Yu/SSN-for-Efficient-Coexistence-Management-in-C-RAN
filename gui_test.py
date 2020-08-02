#test different methods
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
from SSN_modul.Pixel2coord import pixel2coord
from SSN_modul.Sources import Sources
from SSN_modul.prx_analog import data_log
from SSN_modul.Estimate_nearst import estimate_map_nearst_method
#
from SSN_modul.Coord2pixel import coord2pixel
from SSN_modul.Pixel2coord import pixel2coord
from SSN_modul.Find_pairwise_distance import find_pairwise_distance
from SSN_modul.prx_analog import data_log
from SSN_modul.prx_analog import data_for_true_cor
from SSN_modul.LS_location import LS_loc
from SSN_modul.Generate_sensor_locations import generate_sensor_locations


def guitest(MM,xcor,ycor):
    area_size = myglobals.area_size  # [10, 5]
    xrange = [0, area_size[0]]
    yrange = [0, area_size[1]]
    Range = np.array([xrange[0], xrange[1], yrange[0], yrange[1]])
    PixelRange = coord2pixel(Range) + [1, 0, 1, 0]

    Source_loc = [xcor, ycor]
    Ptx = -10
    MM = MM
    flag = 1
    method = 'kriging'
    # method='shepard'
    # method='neighbour'
    vari = 'bin'

    ##
    # Locations = np.array(
    #     [[0.5, 4], [3, 5], [7, 2.5], [1, 0.5], [8.5, 0.8], [3, 1.5], [4, 1], [5, 2], [6.2, 1.1], [2, 1.9], [2.5, 2.3],
    #      [3, 3], [7.5, 3.5], [3.5, 2.75], [0.6, 1.5], [1.25, 3.1], [7.1, 0.3], [8.1, 3.1],
    #      [4, 3.8], [2, 4.5], [5, 3.1], [6.1, 3.5], [6.2, 4.3], [8, 4.5], [2, 1]])

    ##for 50 sensors test
    # Locations=np.array(
    #     [[0.67364638, 2.28947991],[9.93341331, 0.95542107],[1.82242923, 1.53087528],[1.04751652, 3.05047091],[3.9480761,  3.5022931 ],
    #      [6.1083599,  4.75512156],[4.97983297, 0.52770699],[5.32639046, 3.55030126],[6.59182669, 0.51394635],[7.25343255, 4.88115543],
    #      [3.96248924, 4.6862628 ],[7.52347415, 3.73200227],[4.53042301, 1.61072596],[6.39027678, 2.19262825],[0.199442,   3.7110518 ],
    #      [3.28389192, 3.423724  ],[9.5403416,  0.25601425],[0.81477858, 0.98104154],[8.34015388, 4.47387084],[8.2669614,  0.0783419 ],
    #      [9.7288704,  3.7857175 ],[5.62445041, 4.08035627],[5.67375543, 0.66634032],[6.02209598, 2.56838373],[6.78476374, 0.66731677],
    #      [0.53226241, 0.64590897],[9.73884966, 1.92304957],[3.10276626, 3.4410621 ],[3.58134045, 2.09529237],[7.75843324, 1.37180076],
    #      [3.22643465, 2.62245479],[2.70272802, 2.81852081],[1.46448928, 4.68585227],[3.14660896, 2.38422047],[8.67692837, 4.99861914],
    #      [0.0192289,  3.22337307],[7.1758682,  4.05264881],[7.66234889, 0.1793061 ],[3.98083337, 4.56559927],[4.83294335, 0.25021726],
    #      [3.9727205,  1.28927461],[6.36246273, 0.01184955],[9.20024388, 3.63732518],[3.91988766, 0.23612493],[2.10838329, 0.85399577],
    #      [7.46888132, 0.85088804],[3.5466248,  3.60073434],[8.05463967, 1.54125835],[4.49369649, 1.3254797 ],[5.47086327, 3.07157279]])

    xmax = myglobals.area_size[0]
    ymax = myglobals.area_size[1]
    # Locations=np.zeros(((Nmx-1)*(Nmy-1),2))
    # xy=0
    # for ii in range(0, Nmx - 1):
    #     xx = xi[ii] + xmax / (2 * (Nmx - 1))
    #
    #     for jj in range(0, Nmy - 1):
    #         yy = yi[jj] + ymax / (2 * (Nmy - 1))
    #         Locations[xy,:]=np.array([xx,yy])
    #         xy=xy+1

    Locations = generate_sensor_locations(MM, [0, xmax, 0, ymax])
    # Locations = Locations[0:MM, :]
    # plt.figure(11)
    # plt.plot(2 * Locations[:, 1].T * myglobals.PixelResolution, 2 * Locations[:, 0].T * myglobals.PixelResolution, 'b*')
    # plt.xlabel('x/m')
    # plt.ylabel('y/m')
    # plt.title('simulation environment')

    tdist, tmean = find_pairwise_distance(Locations)
    Dist = tdist
    Prx = data_log(Dist, Source_loc, Locations, Ptx)

    # for locating #####################################
    # sour_loc, es_ptx = LS_loc(Locations, Prx)

    def estimate_map(Prx, Dist, Locations, method, vari):
        Pow = Prx
        if vari == 'pbp':
            rij = np.zeros((Pow.shape[1], Pow.shape[1]))
            for i in range(0, Pow.shape[1]):
                rij[i, :] = 0.5 * (Pow[0, i] - Pow) * (Pow[0, i] - Pow)

            dij = Dist
            # # # calculate mean-value of variogram that under same distance
            # dd = []
            # semi = []
            # for n in range(0, dij.shape[0]):
            #     for m in range(0, dij.shape[1]):
            #         if n == m:
            #             continue
            #         else:
            #             lo = np.argwhere(dij == dij[n, m])
            #
            #             dd.append(dij[n, m])
            #             se = []
            #             for l in range(0, lo.shape[0]):
            #                 se.append(rij[lo[l, 0], lo[l, 1]])
            #
            #             semi.append(np.sum(se) / lo.shape[0])
            # Bin_bound=dd
            # Variogram=semi

            # # calculate variogram directly
            dd = dij.reshape(1, Pow.shape[1] * Pow.shape[1])
            semi = rij.reshape(1, Pow.shape[1] * Pow.shape[1])
            Bin_bound = dd[0]
            Variogram = semi[0]

        elif vari == 'bin':
            VarResolution = 1
            rang = Range
            MaxDist = get_distance(np.array([rang[0], rang[2]]), np.array([rang[1], rang[3]]))
            bins = np.arange(0, MaxDist + VarResolution, VarResolution) + VarResolution

            Pow = Pow
            Variogram, Bin_bound = find_variogram(Dist, Pow, bins)
            # plt.figure(30)
            # plt.plot(Bin_bound, Variogram, 'b.-')
            # plt.xlabel('distance/m')
            # plt.ylabel('semivariogram')
            # plt.title('equal space method')
            # plt.show()

        # sometimes the last value of Variogram is smaller than the first one.
        # Then it can't fit'RuntimeError: Optimal parameters not found:
        # The maximum number of function evaluations is exceeded.'

        # if Variogram[len(Variogram)-1]<Variogram[0]:
        #     print(Variogram)
        #     print(Bin_bound)
        #     Variogram=Variogram[0:len(Variogram)-1]
        #     Bin_bound=Bin_bound[0:len(Bin_bound)-1]

        pg1, pg2, pg3 = opt.curve_fit(Exponent_modul, Bin_bound, Variogram, bounds=([0, 0, 0], [np.inf, np.inf, np.inf]), method='trf')[0]  # bounds=([-np.inf,0,-np.inf,], [np.inf,np.inf,np.inf])
        # pg1, pg2, pg3 = opt.curve_fit(Spherical_modul, Bin_bound, Variogram)[0]
        #pg1, pg2, pg3 = opt.curve_fit(Exponent_modul, Bin_bound, Variogram)[0]

        p = [pg1, pg2, pg3]
        # print(p)
        rang = PixelRange
        img = np.zeros((int(rang[1]) - int(rang[0]) + 1, int(rang[3]) - int(rang[2]) + 1))
        for i in range(0, img.shape[0]):
            tx = rang[0] + i
            for j in range(0, img.shape[1]):
                ty = rang[2] + j
                pxcoord = np.array([tx, ty])
                coord = pixel2coord(pxcoord)

                if method == 'kriging':
                    # Kriging_method
                    # Pow = Prx
                    Pos = Locations
                    A, B = generate_matrices(p, Dist, Pos, coord)
                    W = np.linalg.solve(A, B)
                    W = W[0:Pow.shape[1], 0].T

                    Pow_est = sum(sum(W * Pow))
                    img[i, j] = Pow_est
                elif method == 'shepard':
                    Pos = Locations
                    PowerFactor = 2
                    flag = 1
                    n = Pow.shape[1]

                    W = np.zeros((1, n))
                    for nn in range(0, n):
                        td = get_distance(Pos[nn, :], coord)
                        if td == 0:
                            flag = 0
                            Pow_est = Pow[0, nn]
                            break
                        W[0, nn] = 1 / (td ** PowerFactor)
                    if flag == 1:
                        Pow_est = sum(sum(W * Pow)) / sum(sum(W))
                    img[i, j] = Pow_est
                elif method == 'neighbour':
                    Pos = Locations
                    Pow = Prx
                    grid_z0 = griddata(Pos, Pow.T, coord, method='nearest')
                    # grid_z0 = naturalneighbor.griddata(Pos, Pow.T, coord)
                    img[i, j] = grid_z0

        Img = img
        return Img

    ##
    def map_true():
        rang = PixelRange
        img = np.zeros((int(rang[1]) - int(rang[0]) + 1, int(rang[3]) - int(rang[2]) + 1))
        zone = np.zeros((img.shape[0] * img.shape[1], 2))
        ik = 0
        for ix in range(0, img.shape[0]):
            txx = rang[0] + ix
            for jy in range(0, img.shape[1]):
                tyy = rang[2] + jy
                pxcoord = np.array([txx, tyy])
                coord = pixel2coord(pxcoord)
                zone[ik, :] = coord
                ik = ik + 1
        td, tm = find_pairwise_distance(zone)
        img0 = data_for_true_cor(td, Source_loc, zone, Ptx)

        img0 = img0.reshape(int(rang[1]) - int(rang[0]) + 1, int(rang[3]) - int(rang[2]) + 1)

        print(img0.shape)
        Img = img0
        return Img



    #
    if flag == 1:
        Img = estimate_map(Prx, Dist, Locations, method, vari)
    elif flag == 0:
        Img = estimate_map_nearst_method(SS, Locations, Prx, PixelRange)
    elif flag == -1:
        Img = map_true()

    # Img=neighbour(Locations,Prx,PixelRange)

    IMG = Img

    # # IMG = np.where(IMG < -80., -100, IMG)
    #
    # lo = np.argwhere(IMG == np.max(IMG))
    # lo = (lo + np.array([1, 1])) * myglobals.PixelResolution
    # print(lo)
    # print(np.max(IMG))
    # # IMG = np.where(IMG < -60, -100, IMG)
    # plt.figure(2)
    # plt.imshow(IMG, interpolation='nearest')
    #
    # # nn=nn+1
    # # plt.pause(0.5)
    # plt.colorbar()
    # plt.show()
    #
    # # fig = plt.figure(2)
    # # ax = fig.gca(projection='3d')
    # # nx=IMG.shape[0]
    # # ny = IMG.shape[1]
    # # Y = np.linspace(0,nx-1,nx)
    # # X = np.linspace(0,ny-1,ny)
    # # X, Y = np.meshgrid(X, Y)
    # #
    # #
    # # surf=ax.plot_surface(X, Y, IMG, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    # # plt.xlabel('x[m]')
    # # plt.ylabel('y[m]')
    # # plt.title('Estimated REM')
    # # plt.show()
    return IMG