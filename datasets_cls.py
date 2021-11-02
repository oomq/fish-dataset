import os
import glob
from os import listdir, getcwd
from os.path import join
from tqdm import tqdm
import xml.etree.ElementTree as ET #导入xml模块
import pickle
import cv2
import numpy as np
import PIL as Image

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    '''
    auto: True 表示resize后，填充图片的长和宽至32的倍数
    scalefill: True 表示按new_shape直接resize，不进行填充（auto=False时，这参数才能生效）
    scaleup: True 表示也进行上采样
    '''
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    '''只做下采样，不做上采样'''
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding #np.mod取余
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)

def class_gt(_dir,class_name,dataset,nums,save_dir,pad_pixel):
    result = {}
    for clss in class_name:
        result[clss]=0 
    #print(result)
    result["other"]=0
    result["sum"]=0
    
    #total参数设置进度条的总长度
    pbar = tqdm(total=nums,desc="%s-porcess"%dataset,unit="xml")

    for xmll in glob.glob(_dir+"/annotations/*.xml"):
        print(xmll)
        #time.sleep(0.05)
        pbar.update(1)#每次更新进度条的长度
        with open(xmll,"r",encoding="utf-8") as f:
            xml = ET.parse(f)
            # root = xml.getroot()
            # print(root.findall("object"))
            print(_dir+"/images/"+os.path.basename(xmll)[:-4]+".jpg")
            img_path = _dir+"/images/"+os.path.basename(xmll)[:-4]+".jpg"
            img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)


            for obj in xml.iter('object'):
                result["sum"] = result["sum"]+1
                xmin = int(obj.find('bndbox').find('xmin').text)
                ymin = int(obj.find('bndbox').find('ymin').text)
                xmax = int(obj.find('bndbox').find('xmax').text)
                ymax = int(obj.find('bndbox').find('ymax').text)
                
                if obj.find("name").text not in class_name:
                    result["other"] = result["other"]+1
                for clsn in class_name:
                    if obj.find("name").text == clsn: #按标注的标签名进行统计           
                        result[clsn] = result[clsn]+1
                        
                        pad = pad_pixel
                        
                        x1,y1,x2,y2 = xmin-pad,ymin-pad,xmax+pad,ymax+pad
                        y1_pad,y2_pad,x1_pad,x2_pad =0,0,0,0
                        img_h,img_w = img.shape[0],img.shape[1]
                        if ymin-pad < 0:                            
                            y1_pad = abs(ymin-pad)
                            y1=0
                        if ymax+pad > img_h:                            
                            y2_pad = ymax+pad-img_h
                            y2=img_h
                        if xmin-pad < 0:                            
                            x1_pad = abs(xmin-pad)
                            x1=0
                        if xmax+pad > img_w:                            
                            x2_pad = xmax+pad-img_w
                            x2=img_w
                            
                        gt_box = img[y1:y2,x1:x2]## 裁剪坐标为[y0:y1, x0:x1]
                        
                        top, bottom = int(round(y1_pad - 0.1)), int(round(y2_pad + 0.1))
                        left, right = int(round(x1_pad - 0.1)), int(round(x2_pad + 0.1))
                        gt_box = cv2.copyMakeBorder(gt_box, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114)) 
                
                        
                        #gt_box,_,_ = letterbox(gt_box,(224,224))
                        rs_box = cv2.resize(gt_box,(224,224))
                        rs_box = cv2.copyMakeBorder(rs_box[24:224-24,24:224-24], 24, 24, 24, 24, cv2.BORDER_CONSTANT, value=(114,114,114)) 
                        
                        cv2.imwrite(save_dir+"/%s/%s/%s_%s.jpg"%(dataset,obj.find("name").text,os.path.basename(xmll)[:-4],
                                                                 result[obj.find("name").text]),rs_box,[100])
                    
                    
                    
    pbar.close()#关闭占用资源
    return result

if __name__ == '__main__':
    
    #train_dir="E:/DL/detectron2/SwinT_detectron2/datasets/train"#图像和xml文件在同一个文件夹
    #test_dir="E:/DL/detectron2/SwinT_detectron2/datasets/test"#图像和xml文件在同一个文件夹
    #test_dir="F:/Postgraduate_time/My_research/data_process/all_in/fifth5/train-5/all"
    test_dir="H:/Orgin_datasets/pig-2-4-60/2/mon"
    
    
    class_name = ["0","1","2"]
    
    #save_cls_dir = "E:/DL/detectron2/SwinT_detectron2/datasets/swin-cls/"
    save_cls_dir = test_dir+"/"
    
    for dataset in ["val-p24/"]:#"train-16/",
        for cls_n in class_name:
            os.makedirs(save_cls_dir + dataset + cls_n, exist_ok=True)
    
    #train_num = len(os.listdir(train_dir+"/images"))
    test_num = len(os.listdir(test_dir+"/images"))
    #print(train_num,test_num)
    
    #results1 = class_gt(train_dir,class_name,"train-16",train_num,save_cls_dir)   
    results2 = class_gt(test_dir,class_name,"val-p24",test_num,save_cls_dir,16)
                   
    #print("\n\n训练集: ",train_num)
    print("测试集: ",test_num)











