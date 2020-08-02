import numpy as np
from SSN_modul.Generate_sensor_locations import generate_sensor_locations


area_size=np.array([5,9.4])
#area_size=np.array([10,5])
nSSU=12
nSSU1=nSSU+1
#nSSU=0
nSource=1
xs=5
ys=2.4
loc_source=[xs,ys]
#loc_source=None # only for testing different deployments

Ptx=-10
gain=1
N=8
#PixelResolution=1
PixelResolution=0.5
#freq_center_kHz = 5240000
#freq_bandwidth_kHz = 20000
sample_rate = 225001
center_freq = 434*1e6

dcor=4
alpha=2.18#free space
#alpha=3.5# outdoor
d0=1# 1m
c=3*(10**8)
#f=2.4*(10**9)
f=434*(10**6)
Pl0=-20 * np.log10((c) / (4 * np.pi * f))
#Pl0=0
std_err=3# Indoor Small Office
#std_err=8 # outdoor
Nm=100

senpow=[]
v=0.04

# for thread sensors

power_threads=list(range(0,nSSU1+1))
for i in range(0,nSSU1+1):
    power_threads[i]=[]

psd_threads=list(range(0,nSSU1+1))
for i in range(0,nSSU1+1):
    psd_threads[i]=[]

fre_threads=list(range(0,nSSU1+1))
for i in range(0,nSSU1+1):
    fre_threads[i]=[]


# #
