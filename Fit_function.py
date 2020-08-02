import numpy as np


def Gaussian_modul(x, p1, p2, p3):
    #return p1 + p2 * (1. - np.exp(-x /(p3/3)))  # exponent
    #print('what wrong')
    return p1+p2*(1.-np.exp((-x**2.)/((4*p3/7)**2.)))#gaussin

def Spherical_modul(x, p1, p2,p3):
    return np.piecewise(x, [x <= p3, x > p3],
                        [lambda x: p2 * ((3.*x)/(2.*p3) - (x**3.)/(2.*p3**3.)) + p1, p2 + p1])#spherical


def Exponent_modul(x, p1, p2, p3):
    return p1 + p2 * (1. - np.exp(-x / (p3 / 3)))  # exponent


def falsch_sph_modul(x, p1, p2, p3):
    return p2 * ((3. * x) / (2. * p3)) - (x ** 3.) / (2. * p3 ** 3.) + p1  # falsch-spherical

