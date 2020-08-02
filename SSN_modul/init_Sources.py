#
import numpy as np
#
from SSN_modul.Sources import Sources
from SSN_modul import myglobals
#
def init_sources(nSource):
    SourceGroup=list(range(0,nSource))
    Locations=np.array([myglobals.loc_source])
    Pow=np.array([myglobals.Ptx])

    for n in range(0,nSource):
        loc=Locations[n,:]
        pow=Pow[n]
        SourceGroup[n]=Sources(pow,loc)

    return SourceGroup