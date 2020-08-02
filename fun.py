from numpy import *
def fun1(x,A,P,r,b):
    theta = ((A.T*A+x*P).I)*(A.T* b-0.5 * x * r)
    f = r.T*theta+theta.T* P * theta

    return f