import numpy as np
def watt2db(pow):
    pow2=10*np.log10(pow)
    return pow2