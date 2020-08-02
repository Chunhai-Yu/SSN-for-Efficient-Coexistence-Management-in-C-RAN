import numpy as np
from SSN_modul.Bisection_method import bisection
from SSN_modul import myglobals
def LS_loc(Pos,Pow):
    b=np.zeros((Pos.shape[0],1))
    c=np.sum(Pos*Pos,axis=1)
    b[:, 0]=c

    A=np.zeros((Pos.shape[0],4))
    A1=2*Pos
    A[:,0:2]=A1
    # Pl0=20 * log10((myglobals.c) / (4 * pi * myglobals.f))
    h = (-myglobals.Pl0 - Pow) / (5 * myglobals.alpha)
    A3 = np.power(10, h)
    mid1=A3.T
    A[:,2]=mid1[:,0]
    mid2=-np.ones((Pos.shape[0],1))
    A[:,3]=mid2[:,0]

    P = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    r=np.zeros((4,1))
    r[3,0]=-1


    x1 = -1e5
    x2 = 1e5
    tol = 1e-10
    A=np.mat(A)

    P=np.mat(P)
    r=np.mat(r)
    b=np.mat(b)

    #print(A.T*A)
    k, lamda, L_lamda1 = bisection(x1, x2, tol, A, P, r, b)

    # solve Lagrange dual problem
    theta = ((A.T * A + lamda * P).I) * (A.T * b - 0.5 * lamda * r)  # estimated theta
    x_estimation = theta[0, 0]

    y_estimation = theta[1, 0]
    L_theta = 2 * theta.T * (A.T * A + lamda * P) - 2 * b.T * A + lamda * r.T

    Ptx_estimation = np.log10(theta[2, 0]) * 5 * myglobals.alpha  # estimated Ptx



    return [x_estimation,y_estimation],Ptx_estimation