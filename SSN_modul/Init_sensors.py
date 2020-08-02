#
import numpy as np
#
from SSN_modul.Sensors import Sensors
from SSN_modul.Generate_sensor_locations import generate_sensor_locations
from SSN_modul import myglobals
#
def init_sensors(nSSU):
    SensorGroup=list(range(0,nSSU))

    Locations=np.array([[4.55,9.38],[2.35,9.34],[0.25,9.34],[0.25,6.20],[2.66,6.75],[4.83,6.9],[4.9,3.94],[2.85,3.90],[0.1,3.67],[0.19,0.3],[2.06,0.2],[4.68,0.63]])
    # Locations = np.array(
    #     [[0.5, 4], [3, 5], [7, 2.5], [1, 0.5], [8.5, 0.8], [3, 1.5], [4, 1], [5, 2], [6.2, 1.1], [2, 1.9], [2.5, 2.3],
    #      [3, 3], [7.5, 3.5],[3.5,2.75],[0.6,1.5],[1.25,3.1],[7.1,0.3],[8.1,3.1],
    #      [4, 3.8], [2, 4.5], [5, 3.1], [6.1, 3.5], [6.2, 4.3], [8,4.5], [2, 1]])

    '''# # --------------------------------------or generate Sensors_location random

    xmax = myglobals.area_size[0]-0.5
    ymax = myglobals.area_size[1]-0.5
    Locations = generate_sensor_locations(nSSU, [0, xmax, 0, ymax])  # SensorsPerCluster, Range
'''

    for n in range(0,nSSU):
        loc=Locations[n,:]
        SensorGroup[n]=Sensors(n,loc)

    return SensorGroup
