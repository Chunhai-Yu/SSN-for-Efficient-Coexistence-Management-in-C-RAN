#

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def generate_sensor_locations(SensorsPerCluster,Range):
    Locations=np.zeros((SensorsPerCluster,2))

    # for i in range(0,SensorsPerCluster):
    #     coordx = Range[0] + (Range[1] - Range[0]) * np.random.rand(1,1)
    #     coordy = Range[2] + (Range[3] - Range[2]) * np.random.rand(1,1)
    #     Locations[i,:]=[coordx,coordy]

    Locations[:, 0] = np.random.uniform(Range[0], Range[1], size=(SensorsPerCluster,1))[:,0]
    Locations[:, 1] = np.random.uniform(Range[2], Range[3], size=(SensorsPerCluster, 1))[:,0]



    return Locations



# # generate 50 locations
# Loc=generate_sensor_locations(50,[1,10,1,5])
# print(Loc)
#
#
# plt.figure(11)
# plt.plot(Loc[:,1].T,Loc[:,0].T,'b*')
# plt.show()


