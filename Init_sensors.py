#
import numpy as np
#
from SSN_modul.Sensors import Sensors
from SSN_modul.Generate_sensor_locations import generate_sensor_locations
from SSN_modul import myglobals
#
def init_sensors(nSSU):
    SensorGroup=list(range(0,nSSU))

    Locations=np.array([[4.9,7.8],[3.1,8.2],[0.9,8],[1.2,6.2],[2.8,5.7],[5.2,6.1],[5,4],[2.6,3.6],[1.1,4.3],[1.2,2.2],[2.7,2.1],[5.2,1.6]])
    # Locations = np.array(
    #     [[0.5, 4], [3, 5], [7, 2.5], [1, 0.5], [8.5, 0.8], [3, 1.5], [4, 1], [5, 2], [6.2, 1.1], [2, 1.9], [2.5, 2.3],
    #      [3, 3], [7.5, 3.5],[3.5,2.75],[0.6,1.5],[1.25,3.1],[7.1,0.3],[8.1,3.1],
    #      [4, 3.8], [2, 4.5], [5, 3.1], [6.1, 3.5], [6.2, 4.3], [8,4.5], [2, 1]])

    # # --------------------------------------or generate Sensors_location random
    # xmax = myglobals.area_size[0]-0.5
    # ymax = myglobals.area_size[1]-0.5
    # Locations = generate_sensor_locations(nSSU, [0, xmax, 0, ymax])  # SensorsPerCluster, Range


    for n in range(0,nSSU):
        loc=Locations[n,:]
        SensorGroup[n]=Sensors(n,loc)

    return SensorGroup
