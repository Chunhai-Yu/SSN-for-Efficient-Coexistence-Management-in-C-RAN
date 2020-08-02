# draw error pictures
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from SSN_modul.for_test import picture

##picture(MM,method,SS,flag)
# # RMSE----Number of sensors
NN=10

MM=[12,16,18,22]
nn=0
RMSE1=np.zeros((1,len(MM)))
RMSE2=np.zeros((1,len(MM)))
RMSE3=np.zeros((1,len(MM)))
for j in range(0,NN):
    print(j)
    rmse1=[]
    rmse2=[]
    rmse3=[]

    try:
        for i in range(0, len(MM)):
            print([j,i])
            trueValue = picture(MM[i], 'none', 1, -1)
            krigingValue = picture(MM[i], 'kriging', 1, 1)
            shepardValue = picture(MM[i], 'shepard', 1, 1)
            neighbourValue = picture(MM[i], 'neighbour', 1, 1)

            # v1=np.sqrt(np.sum(np.sum((krigingValue-trueValue)*(krigingValue-trueValue)))/(trueValue.shape[0]*trueValue.shape[1]))
            v1 = np.sqrt(np.sum(np.sum((krigingValue - trueValue) * (krigingValue - trueValue))) / (
                    trueValue.shape[0] * trueValue.shape[1]))
            rmse1.append(v1)
            v2 = np.sqrt(np.sum(np.sum((shepardValue - trueValue) * (shepardValue - trueValue))) / (
                    trueValue.shape[0] * trueValue.shape[1]))
            rmse2.append(v2)
            v3 = np.sqrt(np.sum(np.sum((neighbourValue - trueValue) * (neighbourValue - trueValue))) / (
                    trueValue.shape[0] * trueValue.shape[1]))
            rmse3.append(v3)
        RMSE1 = RMSE1 + np.array(rmse1)
        RMSE2 = RMSE2 + np.array(rmse2)
        RMSE3 = RMSE3 + np.array(rmse3)
        nn=nn+1
    except:
        pass

plt.figure(1)
plt.title('RMSE Analysis')

RMSE1=RMSE1/nn
RMSE2=RMSE2/nn
RMSE3=RMSE3/nn
plt.plot(MM, RMSE1[0], 'r.-', label='Kriging Method')
plt.plot(MM, RMSE2[0], 'g.-', label='Shepard Method')
plt.plot(MM, RMSE3[0], 'b.-', label='Neighbour Method')
plt.legend()
plt.xlabel('number of Sensors')
plt.ylabel('RMSE/dB')


plt.show()


# # RMSE----Nearest number of sensors
# NN=4
# MM=22
# SS=[22]
# #SS=[15,16,17,18,19,20]
#
#
# RMSE1=np.zeros((1,len(SS)))
#
# for j in range(0,NN):
#
#     print(j)
#     rmse1 = []
#     trueValue = picture(MM, 'none', 1, -1)
#     for i in range(0, len(SS)):
#
#         num1value = picture(MM, 'none', SS[i], 0)
#         v = np.sqrt(np.sum(np.sum((trueValue - num1value) * (trueValue - num1value))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#         rmse1.append(v)
#     RMSE1 = RMSE1 + np.array(rmse1)
#
#
#
# RMSE1=RMSE1/NN
# plt.figure(1)
# plt.title('RMSE Analysis')
# plt.plot(SS, RMSE1[0], 'r.-')
#
# plt.xlabel('number of nearest Sensors')
# plt.ylabel('RMSE/dB')
#
#
# plt.show()