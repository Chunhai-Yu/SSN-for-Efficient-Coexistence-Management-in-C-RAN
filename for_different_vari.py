# draw error pictures
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from SSN_modul.different_variogram import picture
# RMSE----different variogram
NN=30

#MM=[6,9,12,15,17,19,21]
MM=[3,4,5,6,8]
nn=0
RMSE1=np.zeros((1,len(MM)))
RMSE2=np.zeros((1,len(MM)))

for j in range(0,NN):

    rmse1=[]
    rmse2=[]
    print(j)


    try:
        flag0 = 0
        for i in range(0, len(MM)):

            print([j,i])
            receive=np.array([[0]])
            trueValue, receive= picture(MM[i], 'none', 1, -1, 'none',receive)

            pbpValue, receive = picture(MM[i], 'kriging', 1, 1, 'pbp',receive)
            print(np.max(pbpValue))
            binValue, receive = picture(MM[i], 'kriging', 1, 1, 'bin',receive)
            print(np.max(binValue))
            if (np.max(pbpValue)>0 or np.max(binValue)>0):
                flag0=1
                print('Warning')
                break
            # v1=np.sqrt(np.sum(np.sum((krigingValue-trueValue)*(krigingValue-trueValue)))/(trueValue.shape[0]*trueValue.shape[1]))
            v1 = np.sqrt(np.sum(np.sum((pbpValue - trueValue) * (pbpValue - trueValue))) / (
                    trueValue.shape[0] * trueValue.shape[1]))
            rmse1.append(v1)
            v2 = np.sqrt(np.sum(np.sum((binValue - trueValue) * (binValue - trueValue))) / (
                    trueValue.shape[0] * trueValue.shape[1]))
            rmse2.append(v2)

        if flag0==0:
            RMSE1 = RMSE1 + np.array(rmse1)
            RMSE2 = RMSE2 + np.array(rmse2)

            nn = nn + 1
        elif flag0==1:
            pass

    except:
        pass


plt.figure(1)
plt.title('RMSE Analysis')
print(nn)
RMSE11=RMSE1/nn
RMSE22=RMSE2/nn
plt.plot(MM, RMSE11[0], 'r.-', label='Kriging Method pbp')
plt.plot(MM, RMSE22[0], 'g.-', label='Kriging Method bin')
plt.legend()
plt.xlabel('number of Sensors')
plt.ylabel('RMSE/dB')


plt.show()