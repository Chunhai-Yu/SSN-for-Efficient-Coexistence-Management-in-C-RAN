# draw error pictures
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from SSN_modul.diff_nethod_nearest import picture
from SSN_modul.Generate_sensor_locations import generate_sensor_locations
from SSN_modul import myglobals
from SSN_modul.Get_distance import get_distance
import math
from SSN_modul.for_time import fortime

# # #------------------------------------------------Analyse RMSE----different methods
# # # RMSE----different methods
# NN=1000 # times of loop
# Nmx=np.array([4,5,6,7])
# Nmy=np.array([4,5,6,7])
# MM=(Nmx-1)*(Nmy-1) # number of sensors method1
# #MM=Nmx*Nmy # method2
# xmax=myglobals.area_size[0]
# ymax=myglobals.area_size[1]
# MM=[15,20,25,30,35]
#
#
# nn=0 # number of successful simulations
# # RMSE for different methods
# RMSE1=np.zeros((1,len(MM))) # Kriging with point by point method
# #RMSE2=np.zeros((1,len(MM))) # Kriging with equal space method
# RMSE3=np.zeros((1,len(MM))) # shepard method
# RMSE4=np.zeros((1,len(MM))) # neighbour method
#
# for j in range(0,NN):
#     # # ------------------------
#     #myglobals.loc_source = generate_sensor_locations(1, [0, xmax, 0, ymax])[0]  # only for test different deployments
#     # print('locsource:',myglobals.loc_source)
#     # # ------------------------
#
#     rmse1=[]
#     #rmse2=[]
#     rmse3=[]
#     rmse4=[]
#     print(j)
#     #sensorlocation=generate_sensor_locations(50,[0,xmax,0,ymax])# (SensorsPerCluster, Range)
#
#
#
#     try:
#         flag0 = 0
#         for i in range(0, len(MM)):
#             print([j,i])
#             sensorlocations = generate_sensor_locations(MM[i], [0, xmax, 0, ymax])  # SensorsPerCluster, Range
#             ##sensorlocations=sensorlocation[0:MM[i],:]
#
#             # ## equal distribution sensor
#             # xi = np.linspace(0, xmax, Nmx[i])
#             # yi = np.linspace(0, ymax, Nmy[i])
#             # sensorlocations = np.zeros((MM[i], 2))
#             # xy = 0
#             # for ii in range(0, Nmx[i] - 1):
#             #     xx = xi[ii] + xmax / (2 * (Nmx[i] - 1))
#             #
#             #     for jj in range(0, Nmy[i] - 1):
#             #         yy = yi[jj] + ymax / (2 * (Nmy[i] - 1))
#             #         sensorlocations[xy, :] = np.array([xx, yy])
#             #         xy = xy + 1
#             # ## square equal distribution sensor method 2
#             #
#             # xi = np.linspace(0, xmax, Nmx[i])
#             # yi = np.linspace(0, ymax, Nmy[i])
#             # sensorlocations = np.zeros((MM[i], 2))
#             # xy = 0
#             # for ii in range(0, Nmx[i]):
#             #     xx = xi[ii]
#             #
#             #     for jj in range(0, Nmy[i]):
#             #         yy = yi[jj]
#             #         sensorlocations[xy, :] = np.array([xx, yy])+np.array([np.random.uniform(-1, 1)*0.1,np.random.uniform(-1, 1)*0.1])
#             #         xy = xy + 1
#
#
#             # picture(MM, method, SS, flag, vari, receive, sensorlocations)
#             # MM: number of sensors, method: interpolation method, SS: number of nearest sensors, here doesn't use
#             # flag: 1--use interpolation to get estimated REM, 0--use nearest method to get REM, -1--true REM
#             # vari: 'pbp'--point by point method to get variogram, 'bin'--equal space method to get variogram
#             receive=np.array([[0]])
#             trueValue, receive= picture('none', 1, -1, 'none',receive,sensorlocations)#,sensorlocations
#             print(np.max(trueValue))
#             lotrue = np.argwhere(trueValue == np.max(trueValue)) * myglobals.PixelResolution
#             print(lotrue)
#
#             pbpValue, receive = picture('kriging', 1, 1, 'pbp',receive,sensorlocations)
#             print(np.max(pbpValue))
#             lotpbp = np.argwhere(pbpValue == np.max(pbpValue)) * myglobals.PixelResolution
#             print(lotpbp)
#
#             # binValue, receive = picture('kriging', 1, 1, 'bin',receive,sensorlocations)
#             # print(np.max(binValue))
#             # lotbin = np.argwhere(binValue == np.max(binValue)) * myglobals.PixelResolution
#             # print(lotbin)
#
#             #-----------------------------------------
#             # avoid some obvious error situation to reduce error
#             if (np.max(pbpValue)>0 or lotpbp.shape[0]>3 ): #(np.max(pbpValue)>0 or np.max(binValue)>0 or lotpbp.shape[0]>3 or lotbin.shape[0]>3)
#                 flag0=1
#                 print('warning')
#                 break
#
#             # if (np.abs(np.max(pbpValue)-np.max(trueValue))>10 or np.abs(np.max(binValue)-np.max(trueValue))>10):#(np.max(pbpValue)>0 or np.max(binValue)>0):
#             #     flag0=1
#             #     print('warning')
#             #     break
#
#             # d1=get_distance(lotrue, lotpbp)
#             # d2=get_distance(lotrue, lotbin)
#             # if (d1>1.5 or d2>1.5):#(np.max(pbpValue)>0 or np.max(binValue)>0):
#             #     flag0=1
#             #     print('warning')
#             #     break
#             # -----------------------------------------
#
#             shepardValue, receive = picture('shepard', 1, 1, 'bin', receive,sensorlocations)
#             print(np.max(shepardValue))
#
#             neighbourValue, receive = picture('neighbour', 1, 1, 'bin', receive,sensorlocations)
#             print(np.max(neighbourValue))
#
#
#
#             v1 = np.sqrt(np.sum(np.sum((pbpValue - trueValue) * (pbpValue - trueValue))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#             rmse1.append(v1)
#             # v2 = np.sqrt(np.sum(np.sum((binValue - trueValue) * (binValue - trueValue))) / (
#             #         trueValue.shape[0] * trueValue.shape[1]))
#             # rmse2.append(v2)
#             v3 = np.sqrt(np.sum(np.sum((shepardValue - trueValue) * (shepardValue - trueValue))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#             rmse3.append(v3)
#             v4 = np.sqrt(np.sum(np.sum((neighbourValue - trueValue) * (neighbourValue - trueValue))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#             rmse4.append(v4)
#
#         if flag0==0:
#             RMSE1 = RMSE1 + np.array(rmse1)
#             #RMSE2 = RMSE2 + np.array(rmse2)
#             RMSE3 = RMSE3 + np.array(rmse3)
#             RMSE4 = RMSE4 + np.array(rmse4)
#
#             nn = nn + 1
#         elif flag0==1:
#              pass
#     except:
#         pass
#
#
# plt.figure(1)
# plt.title('RMSE Analysis')
# print(nn)
# RMSE1=RMSE1/nn
# #RMSE2=RMSE2/nn
# RMSE3=RMSE3/nn
# RMSE4=RMSE4/nn
# plt.plot(MM, RMSE1[0], 'ro-', label='Kriging Method pbp')
# #plt.plot(MM, RMSE2[0], 'g.-', label='Kriging Method esm')
# plt.plot(MM, RMSE3[0], 'b*-', label='IDW(shepard) Method')
# plt.plot(MM, RMSE4[0], 'ks-', label='neighbour Method')
# plt.legend()
# plt.grid()
# plt.xlabel('number of Sensors')
# plt.ylabel('RMSE/dB')
# plt.show()

# ##-----------------------------------------------------------RMSE----Nearest number of sensors
# # RMSE----Nearest number of sensors
# NN=100# times of loop
# Nmx=5
# Nmy=5
# MM=Nmx*Nmy# number of sensors
# #MM = [50]
# xmax=myglobals.area_size[0]
# ymax=myglobals.area_size[1]
#
#
#
# nn=0 # number of successful simulations
# #SS=[25]
# SS=[15,18,20,22,25]
#
#
# RMSE1=np.zeros((1,len(SS)))
#
# for j in range(0,NN):
#     myglobals.loc_source = generate_sensor_locations(1, [0, xmax, 0, ymax])[0]
#     print(myglobals.loc_source)
#     print(j)
#     rmse1 = []
#     # ## equal distribution sensor
#     # xi = np.linspace(0, xmax, Nmx[0])
#     # yi = np.linspace(0, ymax, Nmy[0])
#     # sensorlocations = np.zeros((MM[0], 2))
#     # xy = 0
#     # for ii in range(0, Nmx[0] - 1):
#     #     xx = xi[ii] + xmax / (2 * (Nmx[0] - 1))
#     #
#     #     for jj in range(0, Nmy[0] - 1):
#     #         yy = yi[jj] + ymax / (2 * (Nmy[0] - 1))
#     #         sensorlocations[xy, :] = np.array([xx, yy])
#     #         xy = xy + 1
#
#     # random sensorlocations
#     #sensorlocations = generate_sensor_locations(MM[0], [0, xmax, 0, ymax])
#
#     # square equal distribution sensor method 1
#     # xi = np.linspace(0, xmax, Nmx[i])
#     # yi = np.linspace(0, ymax, Nmy[i])
#     # sensorlocations = np.zeros((MM[i], 2))
#     # xy = 0
#     # for ii in range(0, Nmx[i] - 1):
#     #     xx = xi[ii] + xmax / (2 * (Nmx[i] - 1))
#     #
#     #     for jj in range(0, Nmy[i] - 1):
#     #         yy = yi[jj] + ymax / (2 * (Nmy[i] - 1))
#     #         sensorlocations[xy, :] = np.array([xx, yy])
#     #         xy = xy + 1
#
#     ## square equal distribution sensor method 2
#     xi = np.linspace(0, xmax, Nmx)
#     yi = np.linspace(0, ymax, Nmy)
#     sensorlocations = np.zeros((MM, 2))
#     xy = 0
#     for ii in range(0, Nmx):
#         xx = xi[ii]
#
#         for jj in range(0, Nmy):
#             yy = yi[jj]
#             sensorlocations[xy, :] = np.array([xx, yy])
#             xy = xy + 1
#
#     # # circle equal distribution sensor
#     # sensorlocations = np.zeros((MM, 2))
#     # xy = 0
#     # ci_nu = int(np.sqrt(MM))
#     # for kk in range(0, ci_nu):
#     #     rr = ymax / 2 / ci_nu * (kk + 1)
#     #     for gg in range(0, ci_nu):
#     #         angel = (2 * np.pi / ci_nu) * gg
#     #         yy = rr * math.cos(angel) + ymax / 2
#     #         xx = rr * math.sin(angel) + xmax / 2
#     #         sensorlocations[xy, :] = np.array([xx, yy])
#     #         xy = xy + 1
#
#     try:
#         flag0 = 0
#         receive=np.array([[0]])
#         trueValue, receive= picture('none', 1, -1, 'none',receive,sensorlocations)#,sensorlocations
#         print(np.max(trueValue))
#         lotrue = (np.argwhere(trueValue == np.max(trueValue)) +np.array([1,1]) )* myglobals.PixelResolution
#         print(lotrue)
#         for i in range(0, len(SS)):
#             print([j, i])
#             num1value, receive = picture('none', SS[i], 0, 'none', receive,sensorlocations)
#             print(np.max(num1value))
#             num1 = (np.argwhere(num1value == np.max(num1value))+np.array([1,1]) )* myglobals.PixelResolution
#             print(num1)
#             # avoid some obvious error situation to reduce error
#             if (np.max(num1value)>0 or num1.shape[0]>3 ):
#                 flag0=1
#                 print('warning')
#                 break
#             v = np.sqrt(np.sum(np.sum((trueValue - num1value) * (trueValue - num1value))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#             rmse1.append(v)
#         if flag0==0:
#             RMSE1 = RMSE1 + np.array(rmse1)
#
#             nn = nn + 1
#         elif flag0==1:
#              pass
#     except:
#         pass
#
#
#
# RMSE1=RMSE1/nn
# print(nn)
#
# plt.figure(1)
# plt.title('RMSE Analysis')
# plt.plot(SS, RMSE1[0], 'r.-')
#
# plt.xlabel('number of nearest Sensors')
# plt.ylabel('RMSE/dB')
#
#
# plt.show()

# ##----------------------------------------RMSE----comparison between LiVE and Kriging
# # # RMSE----different methods
# NN=1000 # times of loop
# Nmx=np.array([5,6,7,8,9])
# Nmy=np.array([5,6,7,8,9])
# MM=(Nmx-1)*(Nmy-1) # number of sensors
# MM=[15,20,25,30,35]
# xmax=myglobals.area_size[0]
# ymax=myglobals.area_size[1]
#
#
#
# nn=0 # number of successful simulations
# # RMSE for different methods
# RMSE1=np.zeros((1,len(MM))) # Kriging method
# RMSE2=np.zeros((1,len(MM))) # LiVE method
#
# for j in range(0,NN):
#
#     rmse1=[]
#     rmse2=[]
#     print(j)
#     #sensorlocation=generate_sensor_locations(50,[0,xmax,0,ymax])# (SensorsPerCluster, Range)
#
#
#     try:
#         flag0 = 0
#         for i in range(0, len(MM)):
#             print([j,i])
#             sensorlocations = generate_sensor_locations(MM[i], [0, xmax, 0, ymax])  # SensorsPerCluster, Range
#             ##sensorlocations=sensorlocation[0:MM[i],:]
#
#             # ## equal distribution sensor
#             # xi = np.linspace(0, xmax, Nmx[i])
#             # yi = np.linspace(0, ymax, Nmy[i])
#             # sensorlocations = np.zeros((MM[i], 2))
#             # xy = 0
#             # for ii in range(0, Nmx[i] - 1):
#             #     xx = xi[ii] + xmax / (2 * (Nmx[i] - 1))
#             #
#             #     for jj in range(0, Nmy[i] - 1):
#             #         yy = yi[jj] + ymax / (2 * (Nmy[i] - 1))
#             #         sensorlocations[xy, :] = np.array([xx, yy])
#             #         xy = xy + 1
#
#
#             # picture(MM, method, SS, flag, vari, receive, sensorlocations)
#             # MM: number of sensors, method: interpolation method, SS: number of nearest sensors, here doesn't use
#             # flag: 1--use interpolation to get estimated REM, 0--use nearest method to get REM, -1--true REM
#             # vari: 'pbp'--point by point method to get variogram, 'bin'--equal space method to get variogram
#             receive=np.array([[0]])
#             trueValue, receive= picture('none', 1, -1, 'none',receive,sensorlocations)#,sensorlocations
#             print(np.max(trueValue))
#             lotrue = np.argwhere(trueValue == np.max(trueValue)) * myglobals.PixelResolution
#             print(lotrue)
#
#             pbpValue, receive = picture('kriging', 1, 1, 'pbp',receive,sensorlocations)
#             print(np.max(pbpValue))
#             lotpbp = np.argwhere(pbpValue == np.max(pbpValue)) * myglobals.PixelResolution
#             print(lotpbp)
#
#             lsValue, receive = picture('none', 1, -2, 'none',receive,sensorlocations)
#             print(np.max(lsValue))
#             lotls = np.argwhere(lsValue == np.max(lsValue)) * myglobals.PixelResolution
#             print(lotls)
#
#             #-----------------------------------------
#             # avoid some obvious error situation to reduce error
#             if (np.max(pbpValue)>0 or np.max(lsValue)>0 or lotpbp.shape[0]>3 or lotls.shape[0]>3):
#                 flag0=1
#                 print('warning')
#                 break
#
#
#
#
#             v1 = np.sqrt(np.sum(np.sum((pbpValue - trueValue) * (pbpValue - trueValue))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#             rmse1.append(v1)
#             v2 = np.sqrt(np.sum(np.sum((lsValue - trueValue) * (lsValue - trueValue))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#             rmse2.append(v2)
#
#
#         if flag0==0:
#             RMSE1 = RMSE1 + np.array(rmse1)
#             RMSE2 = RMSE2 + np.array(rmse2)
#
#
#             nn = nn + 1
#         elif flag0==1:
#              pass
#     except:
#         pass
#
#
# plt.figure(1)
# plt.title('RMSE Analysis')
# print(nn)
# RMSE1=RMSE1/nn
# RMSE2=RMSE2/nn
#
# plt.plot(MM, RMSE1[0], 'r.-', label='Kriging Method')
# plt.plot(MM, RMSE2[0], 'g.-', label='LS Method')
# plt.grid()
# plt.legend()
# plt.xlabel('number of Sensors')
# plt.ylabel('RMSE/dB')
# plt.show()


# # # -----------------------------------------------------
# # #------------------------------------------------Analyse RMSE----different sensors deployment
# # # RMSE----different methods
# NN=500 # locations of source
# Nmx=np.array([3,4,5,6])
# Nmy=np.array([3,4,5,6])
# #MM=(Nmx-1)*(Nmy-1) # number of sensors method 1
# MM=Nmx*Nmy # number of sensors method 2
# xmax=myglobals.area_size[0]
# ymax=myglobals.area_size[1]
# #MM=[15,20,25,30,35]
#
# nn=0 # number of successful simulations
# # RMSE for different methods
# RMSE2=np.zeros((1,len(MM)))
#
#
# for j in range(0,NN):
#     # ------------------------
#     myglobals.loc_source = generate_sensor_locations(1, [0, xmax, 0, ymax])[0]  # only for test different deployments
#     print('locsource:',myglobals.loc_source)
#     # ------------------------
#     #rmse1=[]
#     rmse2=[]
#
#     print(j)
#     #sensorlocation=generate_sensor_locations(50,[0,xmax,0,ymax])# (SensorsPerCluster, Range)
#
#
#     try:
#         flag0 = 0
#         for i in range(0, len(MM)):
#             print([j,i])
#             #sensorlocations = generate_sensor_locations(MM[i], [0, xmax, 0, ymax])  # SensorsPerCluster, Range
#
#
#             ### square equal distribution sensor method 1
#             ## xi = np.linspace(0, xmax, Nmx[i])
#             ## yi = np.linspace(0, ymax, Nmy[i])
#             ## sensorlocations = np.zeros((MM[i], 2))
#             ## xy = 0
#             ## for ii in range(0, Nmx[i] - 1):
#             ##     xx = xi[ii] + xmax / (2 * (Nmx[i] - 1))
#             ##
#             ##     for jj in range(0, Nmy[i] - 1):
#             ##         yy = yi[jj] + ymax / (2 * (Nmy[i] - 1))
#             ##         sensorlocations[xy, :] = np.array([xx, yy])
#             ##         xy = xy + 1
#
#             ## square equal distribution sensor method 2
#             xi = np.linspace(0, xmax, Nmx[i])
#             yi = np.linspace(0, ymax, Nmy[i])
#             sensorlocations = np.zeros((MM[i], 2))
#             xy = 0
#             for ii in range(0, Nmx[i]):
#                 xx = xi[ii]
#
#                 for jj in range(0, Nmy[i]):
#                     yy = yi[jj]
#                     sensorlocations[xy, :] = np.array([xx, yy])+np.array([np.random.uniform(-1, 1)*0.1,np.random.uniform(-1, 1)*0.1])
#                     xy = xy + 1
#
#             # # circle equal distribution sensor
#             # sensorlocations = np.zeros((MM[i], 2))
#             # xy = 0
#             # ci_nu = int(np.sqrt(MM[i]))
#             # for kk in range(0, ci_nu):
#             #     rr = ymax / 2 / ci_nu * (kk + 1)
#             #     for gg in range(0, ci_nu):
#             #         angel = (2 * np.pi / ci_nu) * gg+(2*np.pi/ci_nu)/2*kk
#             #         yy = rr * math.cos(angel) + ymax / 2
#             #         xx = rr * math.sin(angel) + xmax / 2
#             #         sensorlocations[xy, :] = np.array([xx, yy])
#             #         xy = xy + 1
#
#
#
#
#
#
#             # picture(MM, method, SS, flag, vari, receive, sensorlocations)
#             # MM: number of sensors, method: interpolation method, SS: number of nearest sensors, here doesn't use
#             # flag: 1--use interpolation to get estimated REM, 0--use nearest method to get REM, -1--true REM
#             # vari: 'pbp'--point by point method to get variogram, 'bin'--equal space method to get variogram
#             receive=np.array([[0]])
#             trueValue, receive= picture('none', 1, -1, 'none',receive,sensorlocations)#,sensorlocations
#             print(np.max(trueValue))
#             lotrue = np.argwhere(trueValue == np.max(trueValue)) * myglobals.PixelResolution
#             print(lotrue)
#
#             binValue, receive = picture('kriging', 1, 1, 'pbp',receive,sensorlocations)
#             print(np.max(binValue))
#             lotbin = np.argwhere(binValue == np.max(binValue)) * myglobals.PixelResolution
#             print(lotbin)
#
#             #-----------------------------------------
#             # avoid some obvious error situation to reduce error
#             if (np.max(binValue)>0 or lotbin.shape[0]>3):
#                 flag0=1
#                 print('warning')
#                 break
#
#
#
#             v2 = np.sqrt(np.sum(np.sum((binValue - trueValue) * (binValue - trueValue))) / (
#                     trueValue.shape[0] * trueValue.shape[1]))
#             rmse2.append(v2)
#
#
#         if flag0==0:
#             RMSE2 = RMSE2 + np.array(rmse2)
#
#
#             nn = nn + 1
#         elif flag0==1:
#              pass
#     except:
#         pass
#
#
# plt.figure(1)
# plt.title('RMSE Analysis')
# print(nn)
# RMSE2=RMSE2/nn
#
#
# plt.plot(MM, RMSE2[0], 'g.-', label='Kriging Method pbp')
#
# plt.legend()
# plt.xlabel('number of Sensors')
# plt.ylabel('RMSE/dB')
# plt.show()

# #------------------------------------------------Analyse time----kriging VS get power
import timeit
NN=1000 #
Nmx=np.array([3,4,5,6])
Nmy=np.array([3,4,5,6])
#MM=(Nmx-1)*(Nmy-1) # number of sensors method 1
MM=Nmx*Nmy # number of sensors method 2
xmax=myglobals.area_size[0]
ymax=myglobals.area_size[1]


nn=0 # number of successful simulations
# RMSE for different methods
Tim=np.zeros((1,len(MM)))


for j in range(0,NN):
    # ------------------------
    myglobals.loc_source = generate_sensor_locations(1, [0, xmax, 0, ymax])[0]  # only for test different deployments


    print(j)
    #sensorlocation=generate_sensor_locations(50,[0,xmax,0,ymax])# (SensorsPerCluster, Range)
    tim=[]

    try:
        flag0 = 0
        for i in range(0, len(MM)):
            print([j,i])

            ## square equal distribution sensor method 2
            xi = np.linspace(0, xmax, Nmx[i])
            yi = np.linspace(0, ymax, Nmy[i])
            sensorlocations = np.zeros((MM[i], 2))
            xy = 0
            for ii in range(0, Nmx[i]):
                xx = xi[ii]

                for jj in range(0, Nmy[i]):
                    yy = yi[jj]
                    sensorlocations[xy, :] = np.array([xx, yy])+np.array([np.random.uniform(-1, 1)*0.1,np.random.uniform(-1, 1)*0.1])
                    xy = xy + 1


            receive=np.array([[0]])

            binValue, receive, krigingtime = fortime(receive,sensorlocations)

            lotbin = np.argwhere(binValue == np.max(binValue)) * myglobals.PixelResolution

            tim.append(krigingtime)

            #-----------------------------------------
            # avoid some obvious error situation to reduce error
            if (np.max(binValue)>0 or lotbin.shape[0]>3):
                flag0=1
                print('warning')
                break



        if flag0==0:
            Tim=Tim+np.array(tim)

            nn = nn + 1
        elif flag0==1:
             pass
    except:
            pass

Tim=Tim/nn
print(Tim)
print(nn)

