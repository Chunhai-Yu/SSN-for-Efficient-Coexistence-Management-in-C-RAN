import numpy as np
from SSN_modul import myglobals

def coord2pixel( coord, options='ceil' ):

    if options=='floor':
        pxcoord = np.floor(coord / myglobals.PixelResolution)
    else:
        pxcoord = np.ceil(coord / myglobals.PixelResolution)
    return pxcoord