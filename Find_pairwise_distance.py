import numpy as np
from SSN_modul.Get_distance import get_distance

def find_pairwise_distance(coord): # locations of sensors
    N=coord.shape[0]
    Dist = -1 * np.ones((N, N))
    Mean=0
    for tx in range(0,N):
        for ty in range(0,N):
            if Dist[ty,tx]<0:
                Dist[tx,ty]=get_distance(coord[tx,:],coord[ty,:])
            else:
                Dist[tx,ty]=Dist[ty,tx]
            Mean=Mean+Dist[tx,ty]
    Mean=Mean/(N**2)
    return Dist,Mean