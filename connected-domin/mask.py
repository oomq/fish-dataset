import argparse
import collections
import datetime
import glob
import json
import os
import os.path as osp
import sys
import uuid
import time
import cv2
import imgviz
import numpy as np

from PIL import Image

import labelme

try:
    import pycocotools.mask
except ImportError:
    print("Please install pycocotools:\n\n    pip install pycocotools\n")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="json2coco")
    parser.add_argument("--input_dir", help="input annotated directory",default="./images")
    parser.add_argument("--output_dir", help="output dataset directory",default="./output")
    parser.add_argument("--labels", help="labels file", default='./labels.txt')#required=True
    parser.add_argument( "--noviz", help="no visualization", action="store_true")
    args = parser.parse_args()

    if not args.noviz:
        vis_dir = osp.join(args.output_dir, "Visualization")
        if not os.path.exists(vis_dir):
            os.makedirs(vis_dir)

    print("Creating Visualization:", vis_dir)

    now = datetime.datetime.now()

    data = dict(
        info=dict(
            description="seedling datasets",
            url=None,
            version="label=4.5.6",
            year=now.year,
            contributor=None,
            date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"),
        ),
        #licenses=[dict(url=None, id=0, name=None,)],
        images=[
            # license, url, file_name, height, width, date_captured, id
        ],
        type="instances",
        annotations=[
            # segmentation, area, iscrowd, image_id, bbox, category_id, id
        ],
        categories=[
            # supercategory, id, name
        ],
    )

    class_name_to_id = {}
    for i, line in enumerate(open(args.labels).readlines()):
        class_id = i - 1  # starts with -1
        class_name = line.strip()
        if class_id == -1:
            assert class_name == "__ignore__"
            continue
        if class_id == 0:
            assert class_name == "__background__"
            continue        
        class_name_to_id[class_name] = class_id
        #print(class_id,class_name,'\n')
        data["categories"].append(
            dict(supercategory="1", id=class_id, name=class_name,)#一类目标+背景，id=0表示背景
        )
    print("categories 生成完成",'\n')
    
    
    label_files = glob.glob(osp.join(args.input_dir, "*.json"))#图像id从json文件中读取
    for image_id, filename in enumerate(label_files):
        print(image_id, filename)
        #print("Generating dataset from:", filename)

        label_file = labelme.LabelFile(filename=filename)

        base = osp.splitext(osp.basename(filename))[0]#图片名
        out_img_file = osp.join(args.output_dir, base + ".jpg")# 保存图片路径

        img = labelme.utils.img_data_to_arr(label_file.imageData)
        imgviz.io.imsave(out_img_file, img)
        masks = {}  # for area
        segmentations = collections.defaultdict(list)  # for segmentation
        for shape in label_file.shapes:
            points = shape["points"]
            label = shape["label"]
            group_id = shape.get("group_id")
            shape_type = shape.get("shape_type", "polygon")
            mask = labelme.utils.shape.shape_to_mask(img.shape[:2], points, shape_type)#labelme=4.5.6的shape_to_mask函数

            if group_id is None:
                group_id = uuid.uuid1()

            instance = (label, group_id)
            #print(instance)

            if instance in masks:
                masks[instance] = masks[instance] | mask
            else:
                masks[instance] = mask

            if shape_type == "rectangle":
                (x1, y1), (x2, y2) = points
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])
                points = [x1, y1, x2, y1, x2, y2, x1, y2]
            else:
                points = np.asarray(points).flatten().tolist()

            segmentations[instance].append(points)
        segmentations = dict(segmentations)
    

        if not args.noviz:
            labels, captions, masks = zip(
                *[
                    (class_name_to_id[cnm], cnm, msk)
                    for (cnm, gid), msk in masks.items()
                    if cnm in class_name_to_id
                ]
            )
            print(labels)

            viz = imgviz.instances2rgb(
                image=img,
                labels=labels,
                masks=masks,
                captions=captions,
                font_size=15,
                line_width=2,
                alpha=1,
                # colormap=[255,0,0],
            )
            out_viz_file = osp.join(
                args.output_dir, "Visualization", base + ".jpg"
            )
            imgviz.io.imsave(out_viz_file, viz)


if __name__ == "__main__":
    main()
    
    
    
    
    

