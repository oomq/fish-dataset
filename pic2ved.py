import cv2
import glob
import os

img_path = '092'
vedio_path = 'video'

if not os.path.exists(vedio_path):
    os.mkdir(vedio_path)

h = 0
w = 0

def img2video(img_path, video_path):
    i = 0

    for imgs in glob.glob(img_path + "/*.jpg"):
        frame = cv2.imread(imgs)
        if i == 0:
            h, w, _ = frame.shape  # 获取一帧图像的宽高信息
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(video_path +'/'+img_path +'.avi', fourcc, 25.0, (w, h), True)
            i = 1
        out.write(frame)  # 对视频文件写入一帧
    #out.release()  # 释放视频流

def txt2gt(txt_path, gt_path):
    filenames = glob.glob(txt_path + "/*.txt")
    f = open(gt_path+ '/'+txt_path+'.txt', 'w')
    for filename in filenames:
        filepath =  filename
        for line in open(filepath):
            f.writelines(line)
        f.write('\n')
    f.close()

img2video(img_path,vedio_path)
txt2gt(img_path,vedio_path)
