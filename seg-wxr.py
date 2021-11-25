import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

# class Seg(object):
#     def __init__(self, frame):
#         self.src = frame
#         self.xx1 = 200
#         self.xx2 = 1800
#         self.yy1 = 30
#         self.src = self.src[self.yy1:,self.xx1:self.xx2]
#         self.maxval = 255
#         # self.areamax = []
#     def seg_one(self):
#         triThe, dst_tri = cv2.threshold(self.src, 105, self.maxval,cv2.THRESH_BINARY_INV)
#         num, labels = cv2.connectedComponents(dst_tri, 4)
#         label_num = [0] * num
#         for i in labels:
#             for j in i:
#                 label_num[j] += 1
#         # self.areamax = [(ind + 1) for ind, t in enumerate(label_num[1:num + 1]) if (t > 1500)]
#         areamax = [(ind + 1) for ind, t in enumerate(label_num[1:num + 1]) if (t > 1500)]
#         return len(areamax)

def seg(frame, thres, num_i, floder):

    src = frame

    xx1 = 200
    xx2 = 1600
    yy1 = 30
    src = src[yy1:, xx1:xx2]
    src = cv2.blur(src, (7, 7))
    # plt.imshow(src)
    # plt.show()
    maxval = 255
    triThe, dst_tri = cv2.threshold(src, thres, maxval, cv2.THRESH_BINARY_INV)  # cv2.THRESH_TRIANGLE + cv2.THRESH_BINARY
    # dst_tri = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 151, 6)
    cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (9, 9))
    diamond = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    dst_tri_cross = cv2.dilate(dst_tri, cross)
    dst_tri_diamond = cv2.erode(dst_tri_cross, diamond)
    cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (11, 11))
    dst_tri_cross = cv2.dilate(dst_tri_diamond, cross)
    diamond = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dst_tri_diamond = cv2.erode(dst_tri_cross, diamond)
    dst_tri_cross = cv2.dilate(dst_tri_diamond, cross)
    num, labels = cv2.connectedComponents(dst_tri_cross, 4)
    if num >5:
        cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (11, 11))
        dst_tri_cross = cv2.dilate(dst_tri_diamond, cross)
        num, labels = cv2.connectedComponents(dst_tri_cross, 4)
    labels = cv2.resize(labels.astype("uint8"),(400,300),interpolation=cv2.INTER_NEAREST)
    label_num = [0] * num
    start = time.time()
    for i in labels:
        for j in i:
            label_num[j] += 1
    mid1 = time.time()
    running_time_1 = mid1 - start
    # print('running time 1: %.5f sec' %running_time_1)
    areamax = [(ind + 1) for ind, t in enumerate(label_num[1:num + 1]) if (t > 200)]
    mid2 = time.time()
    running_time_2 = mid2 - mid1
    # print('running time 2: %.10f sec'%running_time_2)

    print(num_i, num,len(areamax))
    bbox = []
    # if len(areamax) != 4:
    current_axis = plt.gca()
    plt.imshow(labels)
    mid3 = time.time()
    for conid in areamax:
        test = np.where(labels == conid)
        x1 = min(np.where(labels == conid)[1])
        y1 = min(np.where(labels == conid)[0])
        x2 = max(np.where(labels == conid)[1])
        y2 = max(np.where(labels == conid)[0])
        bbox.append([x1, y1, x2, y2])
        current_axis.add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1, color="blue", fill=False, linewidth=2))

    # plt.show()
    plt.savefig('{}/{}.png'.format(floder, num_i))
    plt.cla()
    mid4 = time.time()
    running_time_3 = mid4 - mid3
    # print('running time 3: %.10f sec'%running_time_3)
    # current_axis
    return len(areamax)

def seg_vide(video_dir):
    cap = cv2.VideoCapture(video_dir)
    assert cap.isOpened(),"视频读取失败"
    success =True
    i = 0
    floder = video_dir.replace('.mp4', '')
    if not os.path.exists(floder):
        os.makedirs(floder)
    wrong_list = []
    while(success):
        success, frame = cap.read()
        if success:
            # print(i)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if seg(frame, 100, i, floder) < 4:
                wrong_list.append(i)
            i += 1
        else:
            print('Finish')
    cap.release()
    return wrong_list

def seg_img(img_dir):
    wrong_list = []
    i = 0

    for filename in os.listdir(img_dir):
        i += 1
        if filename.endswith('jpg'):
            frame = cv2.imread('{}/{}'.format(img_dir, filename), cv2.IMREAD_GRAYSCALE)
            if seg(frame, 80, i,floder) < 4:
                wrong_list.append(i)
            print(i)
    return wrong_list

def delete_txt(list, txt_path):
    fw = open(txt_path, 'a+')
    fw.seek(0)
    new_stus = ''
    for i in fw:
        i = i.split(',')
        if int(i[0]) not in list:
            s = ','.join(i)
            new_stus = new_stus + s
    fw.seek(0)
    fw.truncate()
    fw.write(new_stus)
    fw.flush()
    fw.close()
    print('Change txt done')

if __name__ == '__main__':
    # filename = '20E_034'
    # frame = cv2.imread(r'd1/vvvvv/fish-video/1020E/201213/img/{}.jpg'.format(filename), cv2.IMREAD_GRAYSCALE)
    # for filename in os.listdir("d1/vvvvv/fish-video/1020E/201213/img"):
    #     if filename.endswith('jpg'):
    #         src = cv2.imread(r'd1/vvvvv/fish-video/1020E/201213/img/{}'.format(filename), cv2.IMREAD_GRAYSCALE)
    #         print(seg(src, 105))
    # print(seg_img("d1/vvvvv/fish-video/1020E/201213/img"))
    file_path = 'video'
    for video_name in os.listdir(file_path):
        if video_name.endswith('.mp4'):
            print(video_name)
            txt_name = video_name.replace('mp4', 'txt')
            txt_path = '{}/{}'.format(file_path, txt_name)
            wrong_list = seg_vide('{}/{}'.format(file_path, video_name))
            delete_txt(wrong_list, txt_path)
            print(len(wrong_list))
            print(len(wrong_list)/375)
            # print(wrong_list)
    # seg = Seg(frame)
    # print(seg.seg_one())
    # print(seg(frame))

