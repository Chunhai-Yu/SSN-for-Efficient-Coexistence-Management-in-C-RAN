#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#
from SSN_modul.Cluster import Cluster
from SSN_modul.LCEngine import LCEngine
from SSN_modul.Sources import Sources
from SSN_modul.Database import Database
from SSN_modul.Coord2pixel import coord2pixel
#
class GCEngine:
    LCEGroup = []
    #Id = 0
    Img = 0
    #ImgScene = 0
    SourceGroup = Sources() # for testing
    ClusterGroup = Cluster()
    Data = Database()

    SensorLoc = 0
    #EstSourceLoc = 0

    def updata_sourceloc(self):
        #self.LCEGroup[0].updata_source_loc()
        self.SourceGroup.Loc=self.LCEGroup[0].source.Loc

    def assign_LCE(self,LCEGroup):
        self.LCEGroup=LCEGroup
        Loc=np.zeros(2)
        for tx in range(0,len(LCEGroup)):
            loc=self.LCEGroup[tx].get_sensor_locations()
            Loc=np.vstack((Loc,loc))


        self.SensorLoc=Loc[1:Loc.shape[0],:]


    def initialize_database(self):
        tsumx = 0
        tsumy = 0
        for tx in range(0,len(self.ClusterGroup)):
            PixelRange=self.ClusterGroup[tx].PixelRange
            tsumx = tsumx + (PixelRange[1] - PixelRange[0] + 1)
            tsumy = tsumy + (PixelRange[3] - PixelRange[2] + 1)
        imgSize=[tsumx,tsumy]
        self.Data.initialize(imgSize)

    def psd_get(self,id):
        new_psd, new_f=self.LCEGroup[0].get_sensor_psd(id)
        return new_psd, new_f

    def update_sensorloc(self):
        self.SensorLoc = self.LCEGroup[0].get_sensor_locations()

    def combine_maps(self):
        num=len(self.LCEGroup)
        img0=self.LCEGroup[0].get_heat_map()
        if num>1:
            for i in range(1, num):
                imgi = self.LCEGroup[i].get_heat_map()
                img0 = np.hstack(img0, imgi)
        self.Img=img0

    def get_heat_map(self):
        self.combine_maps()
        map=self.Img
        return map

    def draw_sensors(self,figurehandler):
        Loc=coord2pixel(self.SensorLoc)
        plt.figure(figurehandler)
        plt.plot(Loc[:,1].T,Loc[:,0].T,'b*')

    def draw_sources(self,figurehandler):
        loc=self.SourceGroup.Loc
        loc=coord2pixel(loc)
        plt.figure(figurehandler)

        plt.plot(loc[1],loc[0],'r*')

    def draw_map(self,figurehandler):
        fig = plt.figure(figurehandler)
        ax = fig.gca(projection='3d')
        nx=self.Img.shape[0]
        ny = self.Img.shape[1]
        Y = np.linspace(0,nx-1,nx)
        X = np.linspace(0,ny-1,ny)
        X, Y = np.meshgrid(X, Y)


        surf=ax.plot_surface(X, Y, self.Img, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.xlabel('x[m]')
        plt.ylabel('y[m]')
        plt.title('Estimated REM')

        #print(self.Img[0:2,0:9])
        #print(type(self.Img))


        #plt.imshow(self.Img,interpolation = 'nearest')



