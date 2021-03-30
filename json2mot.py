import random
import os
from labelme import utils
import json
import glob
import numpy as np
from read_json import ReadAnno


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


for data_dir in os.listdir(data):
    det_path = os.path.join(mot, data_dir, 'det')
    gt_path = os.path.join(mot, data_dir, 'gt')
    img_path = os.path.join(mot, data_dir, 'img1')

    json_dir = os.path.join(data, data_dir)
    if not (os.path.exists(det_path) or os.path.exists(gt_path)):
        os.makedirs(det_path)
        os.makedirs(gt_path)
    json2det(json_dir, det_path)
    json2gt(json_dir, gt_path)




