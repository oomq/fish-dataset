import random
import os
from labelme import utils
import json
import glob

root = './'

data_path = os.path.join(root, 'data')

data_dirs= os.listdir(data_path)

for data_dir in data_dirs:
    #print(data_dir)
    json_dir=os.path.join(data_path, data_dir)
    jsonpath = (data_path +"\\%s\*.json"  %(data_dir))
    label_json =glob.glob(jsonpath)

