import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

#
from SSN_modul import myglobals
from SSN_modul.Init_sensors import init_sensors
from SSN_modul.LCEngine import LCEngine
from SSN_modul.init_Sources import init_sources
from SSN_modul.Create_clusters import create_clusters
from SSN_modul.GCEngine import GCEngine
#=================================
#nn=0
# allow_key_commands = 1
# while allow_key_commands:#nn<3:
sources_loc=[[3,4],[5,2.5],[8,1]]
#myglobals.loc_source=sources_loc[nn]
myglobals.loc_source = sources_loc[0]
nSSU = myglobals.nSSU
nSource = myglobals.nSource
SensorGroup = init_sensors(nSSU)
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
globalEngine.initialize_database()
# =================================
# IMG=np.zeros((20,10))
# NN=1
# nn=0
# for ii in range(0,NN):
#     print(ii)
#try:
map = globalEngine.get_heat_map()
Img0 = globalEngine.Img
#Img0 = np.where(Img0 < -80., -100, Img0)

# globalEngine.draw_map(10)
globalEngine.draw_sensors(11)
globalEngine.draw_sources(11)
# IMG = IMG + Img0
# nn=nn+1
#except:
    #pass


#IMG=IMG/NN
IMG=Img0
print(Img0.shape)
print(np.max(IMG))
lo = np.argwhere(IMG==np.max(IMG))
print(lo)
#IMG = np.where(IMG < np.max(IMG)-2, -80, IMG)
plt.figure(2)
plt.imshow(IMG,interpolation='nearest')

# nn=nn+1
# plt.pause(0.5)
plt.colorbar()
plt.show()

# fig = plt.figure(2)
# ax = fig.gca(projection='3d')
# nx=IMG.shape[0]
# ny = IMG.shape[1]
# Y = np.linspace(0,nx-1,nx)
# X = np.linspace(0,ny-1,ny)
# X, Y = np.meshgrid(X, Y)
#
#
# surf=ax.plot_surface(X, Y, IMG, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# plt.xlabel('x[m]')
# plt.ylabel('y[m]')
# plt.title('Estimated REM')
# plt.show()

