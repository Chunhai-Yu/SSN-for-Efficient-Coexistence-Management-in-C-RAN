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
from pykrige.ok import OrdinaryKriging
#
class LCEngine:
    Clust = Cluster()
    SensorGroup = []
    Id = 0
    Img = 0
    PairwiseDist = 0
    PairwiseDistMean = 0
    SensorPowers = 0
    p=0
    EstSourceLoc = []
    source=Sources()
    Variogram=0

    # #-------
    # def updata_source_loc(self):
    #     self.source.set_location([self.source.Loc[0]+myglobals.v,self.source.Loc[1]+myglobals.v])
    # #-------

    def config_sensors(self,freq_center_kHz,freq_bandwidth_kHz):
        nSSU = len(self.SensorGroup)
        for i in range(0,nSSU):
            self.SensorGroup[i].set_bandwidth(freq_center_kHz,freq_bandwidth_kHz)

    def add_sensor(self,newsensor):
        self.SensorGroup.append(newsensor)

    ## Estimation process methods

    def place_sensors(self,SensorsPerCluster): #SensorsPerCluster: number of sensors in each cluster
        range=self.Clust.Range
        sensorGroup=list(range(0,SensorsPerCluster))
        Locations=generate_sensor_locations(SensorsPerCluster,range)
        for i in range(0,SensorsPerCluster):
            sensorGroup[i]=Sensors()
            sensorGroup[i].set_location(Locations[i,:])
            sensorGroup[i].Id=i
            sensorGroup[i].ClusterId=self.Clust.Id
        self.SensorGroup=sensorGroup
        self.update_pairwise_distance()

    def update_pairwise_distance(self): ##
        Loc=self.get_sensor_locations()
        tdist, tmean = find_pairwise_distance(Loc)
        self.PairwiseDist=tdist
        self.PairwiseDistMean=tmean

    def get_sensor_locations(self): ##
        num=len(self.SensorGroup)
        Loc=np.zeros((num,2))
        for i in range(0,num):
            Loc[i,:]=self.SensorGroup[i].get_location()
        return Loc



    ## -----------------------------------------------------------------sensor power for testing
    # def update_sensor_powers(self):
    #     loc_source=self.source.Loc ## only one source
    #     Ptx=self.source.Pow
    #     loc_sensor=self.get_sensor_locations()
    #     Dist=self.PairwiseDist
    #     Prx=data_log(Dist,loc_source,loc_sensor,Ptx)
    #     self.SensorPowers=Prx

    # for GUI Threading-----------
    # def update_sensor_powers(self): ##
    #     self.SensorPowers = myglobals.senpow[-1]

    # def receive_senpow(self):
    #     loc_source=self.source.Loc ## only one source
    #     Ptx=self.source.Pow
    #     loc_sensor=self.get_sensor_locations()
    #     Dist=self.PairwiseDist
    #     Prx=data_log(Dist,loc_source,loc_sensor,Ptx)
    #     return Prx
    #-----------------

    # ## sensor power for testing_loop
    # def update_sensor_powers(self):
    #     num = len(self.SensorGroup)
    #     Pow = np.zeros((1,num))
    #     for i in range(0, num):
    #         Pow[0,i] = np.random.uniform(-40,-80)
    #     self.SensorPowers = Pow
    #     print(Pow)
    #---------------------------------------------------------

    def receive_senpow(self):
        Prx=np.zeros((1,myglobals.nSSU))
        for ii in range(0,myglobals.nSSU):
            Prx[0,ii]=myglobals.power_threads[ii][-1]
        return Prx
    ## used in SSN model . real-----------------------------------
    def update_sensor_powers(self):
        Prx = np.zeros((1, myglobals.nSSU))
        for ii in range(0, myglobals.nSSU):
            Prx[0, ii] = self.SensorGroup[ii].get_power(ii)
        self.SensorPowers=Prx

    def get_sensor_psd(self,id):
        new_psd, new_f=self.SensorGroup[id].get_new_psd(id)
        return new_psd, new_f

    def get_sensor_powers(self): ##
        self.update_sensor_powers()
        Pow=self.SensorPowers
        return Pow

    def fit_variogram(self): # calculate semivariogram using bin_bound ##
        VarResolution = 1
        range = self.Clust.Range
        MaxDist = get_distance(np.array([range[0], range[2]]), np.array([range[1], range[3]]))
        bins=np.arange(0,MaxDist+VarResolution,VarResolution)+VarResolution

        Pow=self.SensorPowers
        self.update_pairwise_distance()
        Variogram, Bin_bound = find_variogram(self.PairwiseDist, Pow, bins)

        self.Variogram=Variogram
        pg1, pg2, pg3 = \
        opt.curve_fit(Exponent_modul, Bin_bound, Variogram, bounds=([0, 0, 0], [np.inf, np.inf, np.inf]), method='trf')[
            0]
        self.p=[pg1,pg2,pg3]
        # plt.figure(30)
        # plt.plot(Bin_bound,Variogram,'b.-')

    def fit_variogram_pbp(self):# calculate semivariance point by point
        Pow = self.SensorPowers
        rij = np.zeros((Pow.shape[1], Pow.shape[1]))
        for i in range(0, Pow.shape[1]):
            rij[i, :] = 0.5 * (Pow[0, i] - Pow)*(Pow[0, i] - Pow)
        self.Variogram=rij
        self.update_pairwise_distance()
        dij=self.PairwiseDist
        # # calculate mean value of variogram that under same distance
        # dd = []
        # semi = []
        # for n in range(0,dij.shape[0]):
        #     for m in range(0,dij.shape[1]):
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
        # Bin_bound = dd
        # Variogram = semi
        # # calculate variogram directly
        dd = dij.reshape(1, Pow.shape[1] * Pow.shape[1])
        semi = rij.reshape(1, Pow.shape[1] * Pow.shape[1])
        Bin_bound = dd[0]
        Variogram = semi[0]

        pg1, pg2, pg3 = \
        opt.curve_fit(Exponent_modul, Bin_bound, Variogram, bounds=([0, 0, 0], [np.inf, np.inf, np.inf]), method='trf')[
            0]
        #pg1, pg2, pg3 = opt.curve_fit(Spherical_modul, Bin_bound, Variogram)[0]

        self.p = [pg1, pg2, pg3]








    # calculate Prx at any location
    def estimate_Kriging(self,p,coord): ##
        Pow=self.SensorPowers
        Pos=self.get_sensor_locations()
        A, B= generate_matrices(p, self.PairwiseDist, Pos, coord)
        W = solve(A, B)
        W=W[0:Pow.shape[1],0].T
        Pow_est = np.sum(np.sum(W*Pow))
        return Pow_est

    def estimate_map(self): ##
        self.update_sensor_powers()
        self.fit_variogram()
        #self.fit_variogram_pbp()
        p=self.p
        rang = self.Clust.PixelRange
        
        img=np.zeros((int(rang[1])-int(rang[0])+1,int(rang[3])-int(rang[2])+1))
        

        for i in range(0,img.shape[0]):
            tx=rang[0]+i
            for j in range(0,img.shape[1]):
                ty=rang[2]+j
                pxcoord=np.array([tx, ty])
                coord = pixel2coord(pxcoord)
                img[i,j]=self.estimate_Kriging(p,coord)
        self.Img=img
    def usekrige(self):
        Locations=self.get_sensor_locations()
        Prx=self.get_sensor_powers()
        data = np.hstack((Locations, Prx.T))
        gridx = np.arange(0.0, myglobals.area_size[0], 0.5)
        gridy = np.arange(0.0, myglobals.area_size[1], 0.5)
        OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='spherical', verbose=False, enable_plotting=False)
        z, ss = OK.execute('grid', gridx, gridy)
        self.Img=z

    ############ nearst method
    def estimate_map_nearst_method(self, N):  # for each point, use nearst N sensors
        self.update_sensor_powers()
        Pos = self.get_sensor_locations()
        Pow = self.SensorPowers
        rang = self.Clust.PixelRange
        img = np.zeros((int(rang[1]) - int(rang[0]) + 1, int(rang[3]) - int(rang[2]) + 1))
        for i in range(0, img.shape[0]):
            tx = rang[0] + i
            for j in range(0, img.shape[1]):
                ty = rang[2] + j
                pxcoord = np.array([tx, ty])
                coord = pixel2coord(pxcoord)
                sen_dis = []
                flag=0
                for ii in range(0, Pos.shape[0]):
                    dis = get_distance(coord, Pos[ii, :])
                    sen_dis.append(dis)
               
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

                # # calculate variogram directly
                dd = dij.reshape(1, pow.shape[1] * pow.shape[1])
                semi = rij.reshape(1, pow.shape[1] * pow.shape[1])
                Bin_bound = dd[0]
                Variogram = semi[0]

                pg1, pg2, pg3 = \
                opt.curve_fit(Exponent_modul, Bin_bound, Variogram, bounds=([0, 0, 0], [np.inf, np.inf, np.inf]),
                              method='trf')[0]
                #pg1, pg2, pg3 = opt.curve_fit(Spherical_modul, Bin_bound, Variogram)[0]
                p = [pg1, pg2, pg3]
                A, B = generate_matrices(p, dij, pos, coord)
                W = solve(A, B)
                W = W[0:pow.shape[1], 0].T
                img[i, j] = sum(sum(W * pow))
        self.Img = img
    ############

    def estimate_map_nearst_method1(self, N):  # for each point, use nearst N sensors
        self.update_sensor_powers()
        Pos = self.get_sensor_locations()
        Pow = self.SensorPowers
        rang = self.Clust.PixelRange
        img = np.zeros((int(rang[1]) - int(rang[0]) + 1, int(rang[3]) - int(rang[2]) + 1))
        for i in range(0, img.shape[0]):
            tx = rang[0] + i
            for j in range(0, img.shape[1]):
                ty = rang[2] + j
                pxcoord = np.array([tx, ty])
                coord = pixel2coord(pxcoord)
                sen_dis = []
                flag=0
                for ii in range(0, Pos.shape[0]):
                    dis = get_distance(coord, Pos[ii, :])
                    sen_dis.append(dis)
               
                sen_dis = np.array(sen_dis)
                num = np.argsort(sen_dis)

                pos = np.zeros((N, 2))
                pow = np.zeros((1, N))
                for kk in range(0, N):
                    pos[kk, :] = Pos[num[kk], :]
                    pow[0, kk] = Pow[0, num[kk]]

                data = np.hstack((pos, pow.T))
                gridx = [coord[0]]
                gridy = [coord[1]]
                #print(gridx)
                OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='spherical', verbose=False, enable_plotting=False)
                z, ss = OK.execute('points', gridx, gridy)
                img[i,j]=z[0]
        
        self.Img = img



    def get_heat_map(self):
        #self.estimate_map()
        #self.estimate_map_nearst_method(myglobals.N)
        #self.estimate_map_nearst_method1(myglobals.N)
        self.usekrige()

        map=self.Img  
        #-myglobals.gain
        
        return map

    def draw_map(self,figure_handler):
        fig = plt.figure(figure_handler)
        ax = fig.gca(projection='3d')
        rang = self.Clust.PixelRange
        X = np.arange(rang[0], rang[1]+1, 1)
        Y = np.arange(rang[2], rang[3]+1, 1)
        X, Y = np.meshgrid(X, Y)
        surf = ax.plot_surface(X, Y, self.Img, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.xlabel('x[m]')
        plt.ylabel('y[m]')
        plt.title('Estimated REM')
        #plt.show()
