
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import keyboard #Using module keyboard
import time
#
'''key_input'q' means quit the loop, 's' means start the loop. 
The received power of five sensors are random generated.
The simple module for the testing-loop: Random powers of sensors->Do Kriging->Show map 
with keyboard control is implemented '''
'''run the code, then input 's' can get the map, and press 'q' 
(maybe need to press several time to get the input)can quit the loop'''
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
# Data=Database()
# globalEngine.Data=Data
globalEngine.initialize_database()
#
CUaction=Actions()
allow_key_commands = 1
while allow_key_commands:
    try:
        if keyboard.is_pressed('q'):#if key 'q' is pressed
            CUaction.Quit=1
            CUaction.Start=0
            print('quit simulation')
        elif keyboard.is_pressed('s'):#if key 's' is pressed
            CUaction.Start=1
            CUaction.Quit=0
    except:
        pass
    if CUaction.Start == 1:
        try:
            # =================================
            map = globalEngine.get_heat_map()
            globalEngine.Data.add_new_frame(map)
            Img0 = globalEngine.Data.get_background()
            # Img0=np.where(Img0 > -50., -30, Img0)
            # print(Img0)

            # globalEngine.draw_map(10)
            # globalEngine.draw_sensors(11)
            # globalEngine.draw_sources(11)
            plt.figure(2)
            plt.imshow(Img0, interpolation='nearest')

            # nn=nn+1
            plt.pause(0.3)
        except:
            pass


    elif CUaction.Quit == 1:
        break
    else:
        pass



plt.colorbar()
plt.show()


