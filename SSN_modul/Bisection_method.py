from numpy import *
from SSN_modul.fun import fun1
def bisection(x1,x2,tol,A,P,r,b):

    a1=x1
    b1=x2
    ya = fun1(a1, A, P, r, b)
    yb = fun1(b1, A, P, r, b)
    if ya*yb>0:
        print('attention')
    for i in range(1,3001):
        if fabs(b1-a1)/2>tol:
            ya = fun1(a1, A, P, r, b)
            yb = fun1(b1, A, P, r, b)
            x=(a1+b1)/2
            yx=fun1(x,A,P,r,b)
            if yx==0:
                a1=x
                b1=x
            elif yb*yx>0:
                b1=x
                yb=yx
            else:
                a1=x
                ya=yx
        else:
            break
    x = (a1 + b1) / 2
    yx = fun1(x, A, P, r, b)
    return i,x,yx