import numpy as np
def get_distance(coord1, coord2):


    Dist=np.sqrt(np.sum((coord1-coord2)**2))
    return Dist