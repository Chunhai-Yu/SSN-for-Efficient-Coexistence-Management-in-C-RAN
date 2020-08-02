#
import numpy as np
#
#
class Database:
    ImgSize=0
    Nframes = 1
    ImgHistory=0
    ImgBg = 0

    def initialize(self,imgSize):

        self.ImgSize=imgSize
        img=np.zeros((int(imgSize[0]),int(imgSize[1])))
        self.ImgBg=img
        Imghistory=np.zeros((int(imgSize[0]),int(imgSize[1]),self.Nframes))
        self.ImgHistory=Imghistory


    def add_new_frame(self,img):

        self.ImgHistory=np.roll(self.ImgHistory,1,axis=2)
        self.ImgHistory[:,:,1]=img


    def update_background(self):

        img=np.zeros((int(self.ImgSize[0]), int(self.ImgSize[1])))
        for tx in range(0,self.Nframes):
            img=img+self.ImgHistory[:,:,tx]
        self.ImgBg=img/self.Nframes

    def get_background(self):
        self.update_background()
        img=self.ImgBg

        return img