import numpy as np
from SSN_modul import myglobals
from SSN_modul.Cluster import Cluster
#
def create_clusters(dim):
    if dim[0]*dim[1]==1:
        ClusterGroup = [0]
        ClusterGroup[0]=Cluster()
    else:
        print('error: more than one Cluster')
    xstep = myglobals.area_size[0] / dim[1]
    ystep = myglobals.area_size[1] / dim[0]
    Id=0
    for tx in range(0,dim[0]):
        for ty in range(0,dim[1]):
            ClusterGroup[tx].Config=dim
            xRange = [ty * xstep, (ty+1) * xstep]
            yRange = [tx * ystep, (tx+1) * ystep]
            ClusterGroup[tx].set_range(np.array([xRange[0],xRange[1], yRange[0],yRange[1]]))
            ClusterGroup[tx].Id = Id
    return ClusterGroup