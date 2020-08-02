#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
#
from SSN_modul import myglobals
from SSN_modul.SpectralDensity import SpectralDensity

#
class Sensors:
    Pow=0
    Loc = [0, 0]
    Vel = 0
    Id = 0
    ClusterId = 0
    #packetCount = 0
    #readyToProcess = 0
    psDensity = SpectralDensity()
    freq_center_kHz=0
    freq_bandwidth_kHz=0

    def __init__(self,*args):#(id,Loc)
        if len(args)>0:
            self.Id = args[0]
            self.Loc = args[1]

    def process(self,packets2,f):
        self.psDensity = SpectralDensity(packets2,f)

    def set_bandwidth(self,freq,bandwidth):
        self.freq_center_kHz = freq
        self.freq_bandwidth_kHz = bandwidth

    def draw(self,figure_handle):
        plt.figure(figure_handle)
        plt.plot(self.Loc[0],self.Loc[1],'bo')
        #plt.show()

    # def get_power(self):
    #     power=self.psDensity.get_power()
    #     self.Pow=power
    #     return power

    # -----------------------------------------------------
    def get_power(self, id):
        #print('id',id)

        power=myglobals.power_threads[id][-1]
        #power = myglobals.power_threads[id]
        #print(power)

        return power

    def get_new_psd(self,id):
        new_psd=myglobals.psd_threads[id][-1]
        new_f=myglobals.fre_threads[id][-1]
        #new_psd = myglobals.psd_threads[id]
        #new_f = myglobals.fre_threads[id]
        return new_psd, new_f



    def set_location(self,Loc):
        self.Loc=Loc

    def get_location(self):
        loc=self.Loc
        return loc

