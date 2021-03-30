import random
import os
from labelme import utils
import json
from read_json import ReadAnno
import glob

def json_transform_txt(json_path, txt_path, process_mode="rectangle"):
    json_path = json_path
    json_anno = ReadAnno(json_path, process_mode=process_mode)
    img_width, img_height = json_anno.get_width_height()
    #filename = json_anno.get_filename()
    filename = os.path.basename(json.replace(".json", ".jpg"))
    coordis = json_anno.get_coordis()
    save_path = os.path.join(txt_path, filename.replace(".jpg", ".txt"))
    with open(save_path, mode='w') as fp:
        for xmin, ymin, xmax, ymax, label in coordis:
            # top_x,top_y,down x,down y---->cen_x,cen_y,width,height
            x = round((xmin + (xmax - xmin) / 2) / img_width, 6)
            y = round((ymin + (ymax - ymin) / 2) / img_height, 6)
            width = round((xmax - xmin) /img_width,6)
            height = round((ymax - ymin) /img_height, 6)
            label_str = '{:s} {:f} {:f} {:f} {:f}\n'.format(
                label, x, y, width, height
            )
            fp.write(label_str)



if __name__ == "__main__":
    root = './'
    data_path = os.path.join(root, 'data')
    data_dirs = os.listdir(data_path)
    for data_dir in data_dirs:
        #print(data_dir)
        json_dir=os.path.join(data_path, data_dir)
        label_json = (data_path +"\\%s\*.json"  %(data_dir))
        jsonpath =glob.glob(label_json)
        txtpath = os.path.join(root, 'txt', data_dir)
        if not os.path.exists(txtpath):
            os.makedirs(txtpath)
        for json in jsonpath:
            json_transform_txt(json,txtpath, process_mode="polygon")

