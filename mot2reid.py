import glob
import numpy as np
import os
import cv2

def float2int(x):
    return int(x)

data_path = 'video-test'
reid_path = 'reid'
mot_output = (data_path +"\\*.txt" )
txt_path = glob.glob(mot_output)
for num,data_path in enumerate(txt_path):
    cap = cv2.VideoCapture()
    idx_frame,i = 0,0
    data = np.loadtxt("{}".format(data_path), delimiter=',',
                      dtype=int)
    cap.open(data_path.replace('txt', 'mp4'))
    while cap.grab():
        _,img =cap.retrieve()
        idx_frame +=1
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        while (data[i,0] ==idx_frame):

            xmin = data[i,2]-5
            ymin = data[i,3]-5
            xmax = data[i,2]+data[i,4]+5
            ymax = data[i,3]+data[i,5]+5

            #idimg = img.crop((xmin - 5, ymin - 5, xmax + 5, ymax + 5))
            idimg = img[ymin:ymax,xmin:xmax,:]
            save_path = os.path.join(reid_path, str(num*4 +data[i,1]), '%08d.jpg' % idx_frame)

            if not os.path.exists(os.path.join(reid_path, str(num*4 +data[i,1]))):
                os.makedirs(os.path.join(reid_path, str(num*4 +data[i,1])))
            cv2.imwrite(save_path, idimg)
            if i ==(data.shape[0]-1):
                break
            i += 1
        print(idx_frame)

