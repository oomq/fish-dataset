import random
import os
from labelme import utils
import json
import glob
import numpy as np
import cv2
from read_json import ReadAnno
import shutil

root = './'
data = './data'
mot = './mot'


def json2det(json_path, det1_path):
    fdet = open(det1_path+'/det.txt', 'w')
    for json in glob.glob(json_path+'/*.json'):
        json_anno = ReadAnno(json, process_mode="polygon")
        img_width, img_height = json_anno.get_width_height()
        filename = os.path.basename(json.replace(".json", ".jpg"))
        frame = int(filename[5:8])
        coordis = json_anno.get_coordis()
        for xmin, ymin, xmax, ymax, label in coordis:
            label_str = '{:d},-1,{:.2f},{:.2f},{:.2f},{:.2f},1,-1,-1,-1\n'.format(
                frame, xmin, ymin, xmax-xmin, ymax-ymin
            )
            fdet.write(label_str)
    fdet.close()


def json2gt(json_path, gt1_path):
    fgt = open(gt1_path+'/gt.txt', 'w')
    for json in glob.glob(json_path+'/*.json'):
        json_anno = ReadAnno(json, process_mode="polygon")
        img_width, img_height = json_anno.get_width_height()
        filename = os.path.basename(json.replace(".json", ".jpg"))
        frame = int(filename[5:8])
        coordis = json_anno.get_coordis()
        for xmin, ymin, xmax, ymax, label in coordis:
            label_str = '{:d},{:d},{:d},{:d},{:d},{:d},1,1,1\n'.format(
                frame, int(label), int(xmin), int(ymin), int(xmax-xmin), int(ymax-ymin)
            )
            fgt.write(label_str)
    fgt.close()


def img2video(img_path, video_path):
    i = 0

    for imgs in glob.glob(img_path + "/*.jpg"):
        frame = cv2.imread(imgs)
        if i == 0:
            h, w, _ = frame.shape  # 获取一帧图像的宽高信息
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(video_path + '/video.avi', fourcc, 25.0, (w, h), True)
            i = 1
        out.write(frame)  # 对视频文件写入一帧
    #out.release()  # 释放视频流

def gt2motresult(gt_path, motresult):
    shutil.copy(gt_path+'/gt.txt', motresult)



def main():

    for data_dir in os.listdir(data):
        det_path = os.path.join(mot, data_dir, 'det')
        gt_path = os.path.join(mot, data_dir, 'gt')
        img_path = os.path.join(mot, data_dir, 'img1')
        video_path = os.path.join(mot, data_dir, 'video')
        motresult_path = os.path.join(mot, 'mot_results')
        json_dir = os.path.join(data, data_dir)
        if not (os.path.exists(det_path) or os.path.exists(gt_path) or os.path.exists(img_path) or os.path.exists(video_path) ):
            os.makedirs(det_path)
            os.makedirs(gt_path)
            os.makedirs(img_path)
            os.makedirs(video_path)

        if not os.path.exists(motresult_path):
            os.makedirs(motresult_path)
        json2det(json_dir, det_path)
        json2gt(json_dir, gt_path)
        for img in glob.glob(json_dir+'/*.jpg'):
            shutil.copy(img, img_path)

        img2video(img_path, video_path)
        copygt_path = motresult_path + '/%s.txt'%data_dir
        gt2motresult(gt_path,copygt_path)

if __name__ == '__main__':
    main()