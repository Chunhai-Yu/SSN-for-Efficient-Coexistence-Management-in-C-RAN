#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
#
from SSN_modul import myglobals
from SSN_modul.Pol2cart import pol2cart

#
class Sources:
    Pow = 0.1
    Loc = np.array([0, 0])
    Vel = 0
    Angle=np.pi*np.random.rand(1,1)
    Id = 0

    def __init__(self,*args):#(Pow,Loc)
        if len(args)>0:
            self.Pow=args[0]
            self.Loc=args[1]
        else:
            self.Angle=np.pi*np.random.rand(1,1)

    def set_location(self,Loc):
        self.Loc=Loc

    def set_power(self,Pow):
        self.Pow=Pow

    def set_velocity(self,Vel):
        self.Vel=Vel

    def update(self):
        [tx,ty]=pol2cart(self.Angle, self.Vel)
        self.Loc=np.mod(self.Loc+np.array([tx,ty]),myglobals.area_size)

    def draw(self,figure_handle):
        plt.figure(figure_handle)
        plt.plot(self.Loc[0],self.Loc[1],'rs')
        #plt.show()