import glob
import random
import imutils
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import itertools
import tqdm
import math


def float2int(x):
    return int(x)

def iou(list,img, cut_frame, idx_frame, num, reid_path):
    # #计算重合部分的上下左右4个边的值，注意最大最小函数的使用
    # leftA = boxA[0]
    # topA = boxA[1]
    # rightA = boxA[0]  + boxA[2]
    # bottomA = boxA[1] + boxA[3]
    #
    # leftB = boxB[0]
    # topB = boxB[1]
    # rightB = boxB[0] + boxB[2]
    # bottomB = boxB[1] + boxB[3]
    # left_max = max(leftA, leftB)
    # top_max = max(topA, topB)
    # right_min = min(rightA, rightB)
    # bottom_min = min(bottomA, bottomB)
    #
    # left_min = min(leftA, leftB)
    # top_min = min(topA, topB)
    # right_max = max(rightA, rightB)
    # bottom_max = max(bottomA, bottomB)
    #
    # # 计算重合部分面积
    # inter = max(0, (right_min - left_max) * max(0, (bottom_min - top_max)))
    # Sa = (rightA - leftA) * (bottomA - topA)
    # Sb = (rightB - leftB) * (bottomB - topB)
    file_num = 0
    for l_xyxy in itertools.combinations(list, 2):
        boxA = l_xyxy[0]
        boxB = l_xyxy[1]
        left_max = max(boxA[0], boxB[0])
        top_max = max(boxA[1], boxB[1])
        right_min = min(boxA[2], boxB[2])
        bottom_min = min(boxA[3], boxB[3])

        left_min = min(boxA[0], boxB[0])
        top_min = min(boxA[1], boxB[1])
        right_max = max(boxA[2], boxB[2])
        bottom_max = max(boxA[3], boxB[3])
        #计算重合部分面积
        inter = max(0, (right_min-left_max) * max(0, (bottom_min-top_max)))
        Sa = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
        Sb = (boxB[2]-boxB[0]) * (boxB[3]-boxB[2])
        # 计算所有区域的面积并计算IOU值，如果python是2，则增加浮点化操作
        uniou = Sa+Sb-inter
        iou =inter / uniou
        if iou > 0 and idx_frame - cut_frame >= (25*3):
            k = idx_frame - cut_frame
            idimg = img[top_min:bottom_max, left_min:right_max, :]
            # cv2.imwrite('{}/{}_{}_{}.jpg'.format(reid_path,num,idx_frame,file_num), idimg)
            # print(iou)
            # print(k)
            cut_frame = idx_frame
            file_num += 1
    return cut_frame

def imagerotate(image):
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    angel = random.randint(-180, 180)
    scale = 1.0

    M = cv2.getRotationMatrix2D(center, angel, scale)


    # new_width = int((height *np.abs(M[0, 1])) + (width * np.abs(M[0, 0])))
    # new_height = int((height *np.abs(M[0, 0])) + (width * np.abs(M[0, 1])))
    new_height = int(width * fabs(sin(radians(angel))) + height * fabs(cos(radians(angel))))
    new_width = int(height * fabs(sin(radians(angel))) + width * fabs(cos(radians(angel))))
    # M[0, 2] += (new_width - width) / 2
    # M[1, 2] += (new_height - height) / 2
    image_rotation = cv2.warpAffine(src=image, M=M, dsize=(new_height, new_width), borderValue=(255, 255, 255))
    return image_rotation




def select_max_region(mask):
    nums, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    background = 0
    for row in range(stats.shape[0]):
        if stats[row, :][0] == 0 and stats[row, :][1] == 0:
            background = row
    stats_no_bg = np.delete(stats, background, axis=0)
    max_idx = stats_no_bg[:, 4].argmax()
    max_region = np.where(labels==max_idx+1, 255, 0)

    return max_region.astype(np.uint8)

cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(3, 3))
diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(3 , 3))

def copypaste(img1,data,folder,idx_frame,fishnum,i):
    img = img1
    txt_data = data
    # num = random.randint(1,5)
    #鱼A作为mask 鱼B为背景

    fish_A = data[num]
    fish_B = txt_data[0]
    # mask_orignal = img[data[0,3]-5:data[0,3]+data[0,5]+5, data[0,2]-5:data[0,2]+data[0,4]+5]
    mask_orignal = img[fish_A[1]:fish_A[1]+fish_A[3], fish_A[0]:fish_A[0]+fish_A[2]]
    # mask_orignal = imagerotate(mask_orignal)
    angel = random.randint(-180, 180)
    mask_orignal = imutils.rotate_bound(mask_orignal, angel)
    ###test-vis
    # if not os.path.exists('cpdataset/jiyu12/{}'.format(folder)):
    #     os.mkdir('cpdataset/jiyu12/{}'.format(folder))
    # cv2.imwrite('cpdataset/jiyu12/{}/{}_{}.jpg'.format(folder,idx_frame, fishnum), mask_orignal)
    rows, cols, channels = mask_orignal.shape
    mask_gray = cv2.cvtColor(mask_orignal, cv2.COLOR_BGR2GRAY)
    # cv2.namedWindow('img', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('img', mask_orignal)
    mask_gray = cv2.blur(mask_gray, (3, 3))
    _, mask = cv2.threshold(mask_gray,130,255,cv2.THRESH_BINARY)
    result1 = cv2.erode(mask, diamond)
    result2 = cv2.dilate(result1, cross)
    result3 = select_max_region(result2)


    # plt.imshow(mask, 'gray')
    kernel = np.ones((5, 5), np.uint8)
    mask_dilate = cv2.erode(result3, kernel, iterations=1)
    # mask_dilate = result3
    # plt.figure()
    # plt.imshow(mask_dilate, 'gray')
    rows1, cols1= mask_gray.shape
    mask_inv = cv2.bitwise_not(mask_dilate)
    # max_y = max(fish_A[3],fish_B[3])
    # max_x = max(fish_A[2],fish_B[2])
    max_y = max(rows1,fish_B[3])
    max_x = max(cols1,fish_B[2])

    # img_background = img[fish_B[1]:fish_B[1]+max_y,fish_B[0]:fish_B[0]+max_x]
    img_background = img
    rows_bg, cols_bg, channels_bg = img_background.shape
    if rows_bg >= rows and cols_bg >= cols:
        center_x = cols_bg/2
        center_y = rows_bg/2
        rec = img_background[int(center_y - rows / 2):int(center_y + rows / 2),
              int(center_x - cols / 2):int(center_x + cols / 2)]
        #在中心区域画图
        # roi = img_background[int(center_y-rows/2):int(center_y+rows/2), int(center_x-cols/2):int(center_x+cols/2)]
        randx = random.randint(math.ceil(cols / 2),cols_bg-200)
        randy = random.randint(math.ceil(rows / 2),rows_bg-200)
        roi = img_background[int(randy - rows / 2):int(randy + rows / 2),
              int(randx- cols / 2):int(randx + cols / 2)]
        #mask背景
        img1_bg = cv2.bitwise_and(roi,roi,mask= mask_dilate)
        #mask前景
        img2_fg = cv2.bitwise_and(mask_orignal,mask_orignal,mask=mask_inv)

        dst = cv2.add(img1_bg,img2_fg)
        # img_background[int(center_y-rows/2):int(center_y+rows/2), int(center_x-cols/2):int(center_x+cols/2)] = dst
        img_background[int(randy - rows / 2):int(randy + rows / 2),
        int(randx - cols / 2):int(randx + cols / 2)] = dst
        # fish_img = img[fish_B[1]:fish_B[1]+fish_B[3],fish_B[0]:fish_B[0]+fish_B[2]]
        fish_img = img
        # cv2.imshow('fish', fish_img)
        # cv2.waitKey()
        cv2.destroyAllWindows()
        if not os.path.exists('cpdataset/jiyu/{}'.format(folder)):
            os.makedirs('cpdataset/jiyu/{}'.format(folder))
        print(image)
        if i == 3:
            # print(image.split('/')[-1])
            cv2.imwrite('cpdataset/jiyu/{}'.format(image.split('/')[-1]), fish_img)
            with open('cpdataset/jiyu/{}'.format(image.split('/')[-1].replace("jpg", "txt")), "a+") as f:
                fo = open(txt,"r")
                datafo = fo.read()
                f.writelines(datafo)

        line = "0 {:.6f} {:.6f} {:.6f} {:.6f}\n".format(randx/cols_bg-cols/cols_bg ,randy/rows_bg-rows/rows_bg,
                        cols/cols_bg, rows/rows_bg)
        with open('cpdataset/jiyu/{}'.format(image.split('/')[-1].replace("jpg","txt")),"a+") as f:
            f.write(line)


        # img_background[int(center_y-rows/2):int(center_y+rows/2)
        # , int(center_x-cols/2):int(center_x+cols/2)] = rec
        # cv2.imshow('1',img_background)
    # cv2.imshow('img',img1)
    # cv2.waitKey()
data_path = 'yolo/data/images/'
labels_path = 'yolo/data/labels/'
# data_path = r'D:\fish-video-output\reid'
# reid_path = r'D:\fish-video-output\reid\2'

def yolo2xyxy(data,height, width): #xywh2tlbr
    data[:,3] = data[:,3] *width
    data[:,4] = data[:,4] *height
    data[:,1] = data[:,1] *width - data[:,3]/2
    data[:,2] = data[:,2] *height - data[:,4]/2
    return data[:,1:].astype(np.uint16)



for folder in os.listdir(data_path):

    label_path = (labels_path + folder+ "\\*txt")
    txt_path = glob.glob(label_path)
    images_path = glob.glob(label_path.replace("labels","images").replace("txt","jpg"))
    # txt_path.remove("yolo/data/labels/{}\\clasess.txt".format(folder))
    for idx_frame,txt in enumerate(txt_path):
        data1 = np.loadtxt("{}".format(txt), delimiter=' ',dtype=float)
        image = txt.replace("labels", "images").replace("txt", "jpg")

        img = cv2.imread(image)
        height, width, depth = img.shape
        data = yolo2xyxy(data1,height, width)
        randnum = range(0, data.shape[0])  # 范围在0到100之间，需要用到range()函数。
        nums = random.sample(randnum, 3)
        i=0
        # for num, copypaste_data in enumerate(itertools.combinations(data, 2)):
        for num in nums:
            i += 1
            copypaste(img, data, folder, idx_frame,num,i)


                # cv2.imshow("1",img)
                # cv2.waitKey()
                # img = cv2.imread(image)