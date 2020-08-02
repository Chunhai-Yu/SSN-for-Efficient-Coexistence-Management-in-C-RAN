#
import numpy as np

#
from SSN_modul.Coord2pixel import coord2pixel

#
class Cluster:
    Range = np.array([0, 100, 0, 100])
    PixelRange = np.array([0, 100, 0, 100])
    Id = 0
    Config=0

    def __init__(self,*args):#(Range)
        if len(args)>0:
            self.Range=args[0]
            self.PixelRange=coord2pixel(args[0])+[1,0,1,0]

    def set_range(self,Range):
        self.Range=Range
        self.PixelRange=coord2pixel(Range)+[1,0,1,0]