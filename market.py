import random
import os
import cv2
from tqdm import tqdm
from PIL import Image

import json
from read_json import ReadAnno
import glob

def json_crop(json_path, reid_path, process_mode="rectangle"):
    json_path = json_path
    json_anno = ReadAnno(json_path, process_mode=process_mode)
    img_width, img_height = json_anno.get_width_height()
    #filename = json_anno.get_filename()
    filename = os.path.basename(json_path.replace(".json", ".jpg"))
    coordis = json_anno.get_coordis()
    #save_path = os.path.join(reid_path, filename.replace(".jpg", ""))
    img_path = os.path.join(json_dir, filename)
    img = Image.open(img_path)
    for xmin, ymin, xmax, ymax, label in coordis:
        idimg = img.crop((xmin-5,ymin-5,xmax+5,ymax+5))
        #idimg = idimg.resize((600, 372), Image.ANTIALIAS)
        save_path = os.path.join(reid_path, label, (label+'_'+filename))
        if not os.path.exists(os.path.join(reid_path, label)):
            os.makedirs(os.path.join(reid_path, label))
        idimg.save(save_path)


if __name__ == "__main__":
    root = './'
    data_path = os.path.join(root, 'data')
    data_dirs = os.listdir(data_path)
    for data_dir in data_dirs:
        print(data_dir + '\n')
        json_dir=os.path.join(data_path, data_dir)
        label_json = (data_path +"\\%s\*.json"  %(data_dir))
        jsonpath =glob.glob(label_json)
        reid_path = os.path.join(root, 'reid')
        if not os.path.exists(reid_path):
            os.makedirs(reid_path)
        for json in tqdm(jsonpath):
            json_crop(json, reid_path, process_mode="polygon")



