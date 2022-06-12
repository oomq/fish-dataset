import random
import os
#from labelme import utils
import json
from read_json import ReadAnno
import glob

def json_transform_txt(json_path, txt_path, process_mode="rectangle"):
    json_path = json_path
    json_anno = ReadAnno(json_path, process_mode=process_mode)
    img_width, img_height = json_anno.get_width_height()
    #filename = json_anno.get_filename()
    filename = os.path.basename(json_path.replace(".json", ".jpg"))
    coordis = json_anno.get_coordis()
    save_path = os.path.join(txt_path, filename.replace(".jpg", ".txt"))
    with open(save_path, mode='w') as fp:
        for xmin, ymin, xmax, ymax, label in coordis:    #在coordis获得了一个label里的坐标信息
            # topleft_x,topl_y,downright x,downr y---->center_x,cen_y,width,height
            x = round((xmin + (xmax - xmin) / 2) / img_width, 6)
            y = round((ymin + (ymax - ymin) / 2) / img_height, 6)
            width = round(((xmax - xmin)+10) /img_width,6)# +10为了框大一点点点
            height = round(((ymax - ymin)+10 )/img_height, 6)
            label = 0  #class = 0
            label_str = '{:d} {:f} {:f} {:f} {:f}\n'.format(  #设置每行写入格式
                label, x, y, width, height
            )
            fp.write(label_str) #写入txt文件

def json_transform_keypoints(json_path, txt_path, process_mode="rectangle"):
    json_path = json_path
    json_anno = ReadAnno(json_path, process_mode=process_mode)
    img_width, img_height = json_anno.get_width_height()
    #filename = json_anno.get_filename()
    filename = os.path.basename(json_path.replace(".json", ".jpg"))
    # coordis = json_anno.get_coordis()
    labels,keypoints = json_anno.get_keypoints()
    save_path = os.path.join(txt_path, filename.replace(".jpg", ".txt"))
    with open(save_path, mode='w') as fp:
        for _num, keypoint in enumerate(keypoints):    #在coordis获得了一个label里的坐标信息
            # topleft_x,topl_y,downright x,downr y---->center_x,cen_y,width,height
            # label = 0  #class = 0
            label_str = '{} {}\n'.format(  #设置每行写入格式
                labels[_num], keypoint
            )
            fp.write(label_str) #写入txt文件




if __name__ == "__main__":
    root = './'
    data_path = os.path.join(root, 'keypointfishdata')
    data_dirs = os.listdir(data_path)
    for data_dir in data_dirs:
        #print(data_dir)
        if data_dir.endswith('.zip') or data_dir.endswith('.rar'):  ## 判断文件的扩展名，只要 文件夹名字 ，排除里面是zip、rar文件
            continue
        json_dir=os.path.join(data_path, data_dir)
        label_json = (data_path +"\\%s\*.json"  %(data_dir)) #只选json文件
        jsonpath =glob.glob(label_json)
        txtpath = os.path.join(root, 'keypointstxt', data_dir)
        if not os.path.exists(txtpath):
            os.makedirs(txtpath)     #创建与json同名的txt
        for json in jsonpath:
            # json_transform_txt(json, txtpath, process_mode="polygon")
            json_transform_keypoints(json, txtpath, process_mode="keypoints")


