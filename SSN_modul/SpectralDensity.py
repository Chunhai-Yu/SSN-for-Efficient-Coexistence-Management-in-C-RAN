#
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
#
from SSN_modul.dB2watt import db2watt
from SSN_modul.Watt2dB import watt2db
#
class SpectralDensity:
    nBins = 128
    freqResolution = 20000 / 128
    freqL = 5230000
    freqH = 5250000
    powArray = np.zeros(128)

    def __init__(self,*args):# （packets2,f） packet2 is the value of PSD in measured frequenceband; f is measured frequenceband
        if len(args)>0:
            self.nBins = args[1].size
            self.freqH = args[1].max()
            self.freqL = args[1].min()
            self.freqResolution = (self.freqH - self.freqL) / (self.nBins - 1)
            self.powArray = db2watt(args[0])  # PSD

    def get_power(self):
        indStart = 1
        indEnd = self.nBins-1
        powarray = self.powArray[indStart:indEnd]*self.freqResolution # Power = PSD * Bandwidth
        pow=np.sum(powarray)
        powdB=watt2db(pow)
        return powdB

    def get_psd(self):
        indStart = 1
        indEnd = self.nBins - 1
        powarray = self.powArray[indStart:indEnd] * self.freqResolution  # Power = PSD * Bandwidth
        psd=powarray

        return psd

    def plot_psd(self,figure_handle):
        plt.figure(figure_handle)
        plt.plot(np.linspace(self.freqL,self.freqH,self.nBins),self.powArray,'r-')