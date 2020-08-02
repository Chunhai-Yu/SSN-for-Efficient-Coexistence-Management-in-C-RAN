from SSN_modul.myglobals import PixelResolution

def pixel2coord(pxcoord):
    coord=pxcoord*PixelResolution
    return coord