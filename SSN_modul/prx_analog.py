#
from numpy import *
from SSN_modul import myglobals
from SSN_modul.Get_distance import get_distance

## for sensors
def data_log(Dist, source_loc, sensor_loc, Ptx):  # ,alpha,Pl0,Ptx,expect,std_err,Nm
    dij = Dist
    N = dij.shape[0]

    sigmaij = myglobals.std_err ** 2 * exp(-abs(dij) / myglobals.dcor)
    # # free space model
    di = zeros((1, N))
    Mu = zeros((1, N))
    for i in range(0, N):
        # free space model

        di[0,i] = get_distance(source_loc, sensor_loc[i, :])
        if di[0,i]<=myglobals.d0:
            Mu[0,i]=Ptx+20*log10((myglobals.c)/(4*pi*di[0,i]*myglobals.f))
        elif di[0,i]>myglobals.d0:
            Mu[0, i] = Ptx+20*log10((myglobals.c)/(4*pi*myglobals.f))-10 * myglobals.alpha * log10(di[0,i])

    # correlated shadowing !!!!!
    Prx = random.multivariate_normal(Mu[0], sigmaij, 1)


    return Prx

# ## for true map
# def data_for_true_log(source_loc, point_loc, Ptx):# log-norm shadowing
#     dd = get_distance(source_loc, point_loc)
#     if dd==0:
#         Prx=Ptx
#     else:
#         Mu = Ptx - myglobals.Pl0 - 10 * myglobals.alpha * log10(dd)
#         # log-normal shadowing
#         Sum = 0
#         for ii in range(0, myglobals.Nm):
#             s = random.normal(0, myglobals.std_err, 1)
#             Sum = Sum + s
#
#         Prx = Mu + Sum / myglobals.Nm
#         #
#     return Prx

def data_for_true_cor(dist, source_loc, points_loc, Ptx):# correlated shadowing
    dij = dist
    N = dij.shape[0]

    sigmaij = myglobals.std_err ** 2 * exp(-abs(dij) / myglobals.dcor)
    # free space model
    di = zeros((1, N))
    Mu = zeros((1, N))
    for i in range(0, N):
        di[0, i] = get_distance(source_loc, points_loc[i, :])
        if di[0, i]==0:
            Mu[0, i]=myglobals.Ptx
            #num=i

        elif di[0, i] <= myglobals.d0:
            Mu[0, i] = Ptx + 20 * log10((myglobals.c) / (4 * pi * di[0, i] * myglobals.f))
        elif di[0, i] > myglobals.d0:
            Mu[0, i] = Ptx + 20 * log10((myglobals.c) / (4 * pi * myglobals.f)) - 10 * myglobals.alpha * log10(di[0, i])


    # correlated shadowing !!!!!
    Prx = random.multivariate_normal(Mu[0], sigmaij, 1)

    return Prx

def data_average(Dist, source_loc, sensor_loc, Ptx):  # ,alpha,Pl0,Ptx,expect,std_err,Nm
    PPrx=zeros((1,Dist.shape[0]))
    for ll in range(0,myglobals.Nm):
        dij = Dist
        N = dij.shape[0]

        sigmaij = myglobals.std_err ** 2 * exp(-abs(dij) / myglobals.dcor)
        # # free space model
        di = zeros((1, N))
        Mu = zeros((1, N))
        for i in range(0, N):
            # free space model

            di[0, i] = get_distance(source_loc, sensor_loc[i, :])
            if di[0, i] <= myglobals.d0:
                Mu[0, i] = Ptx + 20 * log10((myglobals.c) / (4 * pi * di[0, i] * myglobals.f))
            elif di[0, i] > myglobals.d0:
                Mu[0, i] = Ptx + 20 * log10((myglobals.c) / (4 * pi * myglobals.f)) - 10 * myglobals.alpha * log10(
                    di[0, i])

        # correlated shadowing !!!!!
        Prx = random.multivariate_normal(Mu[0], sigmaij, 1)
        PPrx=PPrx+Prx


    PPrx=PPrx/myglobals.Nm
    return PPrx