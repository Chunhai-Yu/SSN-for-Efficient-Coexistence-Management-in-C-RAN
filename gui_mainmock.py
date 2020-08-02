import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import keyboard #Using module keyboard
import time
#
from SSN_modul import myglobals
from SSN_modul.Init_sensors import init_sensors
from SSN_modul.LCEngine import LCEngine
from SSN_modul.init_Sources import init_sources
from SSN_modul.Create_clusters import create_clusters
from SSN_modul.GCEngine import GCEngine
from SSN_modul.Database import Database
from SSN_modul.Actions import Actions

#=================================
def gui_main_image():
    nSSU = myglobals.nSSU
    SensorGroup = init_sensors(nSSU)
    nSource = myglobals.nSource
    SourceGroup = init_sources(nSource)
    CU = [0]
    CU[0] = LCEngine()
    CU[0].SensorGroup = SensorGroup
    CU[0].source = SourceGroup[0]
    CU[0].update_pairwise_distance()

    clusterConfig = np.array([1, 1])
    ClusterGroup = create_clusters(clusterConfig)
    CU[0].Clust = ClusterGroup[0]
    globalEngine = GCEngine()
    globalEngine.assign_LCE(CU)
    globalEngine.SourceGroup = SourceGroup[0]
    globalEngine.ClusterGroup = ClusterGroup
    #
    globalEngine.initialize_database()
    #


    try:
            # =================================
            map = globalEngine.get_heat_map()
            globalEngine.Data.add_new_frame(map)
            Img0 = globalEngine.Data.get_background()

            plt.figure(2)
            plt.imshow(Img0, interpolation='nearest')

            # nn=nn+1
            plt.pause(0.3)
    except:
        pass



plt.colorbar()
plt.show()


