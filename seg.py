import cv2
import numpy as np
import matplotlib.pyplot as plt
# TRIANGLE阈值处理
filename = 'four'
src = cv2.imread(r'test/{}.png'.format(filename), cv2.IMREAD_GRAYSCALE)
#裁剪边缘，以免影响连通域面积
# x1 = 100
# x2 = 1800
# y1 = 30
# src = src[y1:,x1:x2]
# src = cv2.GaussianBlur(src, (101, 101), 1)
src = cv2.blur(src,(5,5))
cv2.imshow('Canny-ori', src)
import cv2
import numpy as np


# img = cv2.GaussianBlur(src, (3, 3), 0)  # 用高斯平滑处理原图像降噪。
canny = cv2.Canny(src, 20, 50)  # 最大最小阈值

cv2.imshow('Canny', canny)

cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(5, 5))
diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
result1 = cv2.dilate(canny,cross)

cv2.imshow('Canny-cross', result1)
result2 = cv2.erode(result1, diamond)
cv2.imshow('Canny-diamond', result2)

result1 = cv2.dilate(result2,cross)
cv2.imshow('Canny-cross1', result1)
result2 = cv2.erode(result1, diamond)
cv2.imshow('Canny-diamond1', result2)
cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(7, 7))
result1 = cv2.dilate(result2,cross)
cv2.imshow('Canny-cross1', result1)


cv2.waitKey(0)
cv2.destroyAllWindows()

# img = src
# x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
# y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
#
# absX = cv2.convertScaleAbs(x)  # 转回uint8
# absY = cv2.convertScaleAbs(y)
#
# dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
#
# cv2.imshow("absX", absX)
# cv2.imshow("absY", absY)
#
# cv2.imshow("Result", dst)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()




triThe = 120
maxval = 255
#做一个滑动条调整阈值





triThe, dst_tri = cv2.threshold(src, triThe, maxval,cv2.THRESH_BINARY_INV)#cv2.THRESH_TRIANGLE + cv2.THRESH_BINARY
# dst_tri =cv2.adaptiveThreshold(src,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,51,1)

# triThe1, dst_tri = cv2.threshold(src, triThe, maxval, cv2.THRESH_TRIANGLE + cv2.THRESH_BINARY_INV)
print(triThe)
# print(triThe1)
cv2.imshow("image", src)
cv2.imshow('thresh_out', dst_tri)
# cv2.imshow('thresh_out1', dst_tri1)
cv2.waitKey(0)
cv2.destroyAllWindows()

num,labels= cv2.connectedComponents(dst_tri,4)

# print(num,labels)

label_num = [0]*num
for i in labels:
    for j in i:
        label_num[j] += 1
# print(label_num)
# if num < 6:
#     areamax = max(label_num[1:num+1])
#     area_ind=label_num.index(areamax)
#     print(areamax,area_ind)
areamax =[]

areamax = [(ind + 1) for ind, t in enumerate(label_num[1:num+1]) if (t>1500) ]

# for ind, t in enumerate(label_num[1:num+1]):
#     if (t>1000):
#         areamax.append((ind + 1))


# print(areamax)

# nrr =  ((labels == 1) | (labels == 3) )
# nrr =  ((labels == 1) | (labels == 2)  | (labels == 3) )
current_axis = plt.gca()
plt.imshow(labels)
# plt.show()


#找到》thres的index 然后计算连通域的包围框后，
bbox =[]
for conid in areamax:
    test = np.where(labels==conid)
    x1 = min(np.where(labels==conid)[1])
    y1 = min(np.where(labels==conid)[0])
    x2 = max(np.where(labels==conid)[1])
    y2 = max(np.where(labels==conid)[0])
    bbox.append([x1,y1,x2,y2])
    current_axis.add_patch(plt.Rectangle((x1,y1),x2-x1,y2-y1, color="blue", fill=False, linewidth=2))

plt.show()

# print(bbox)

# YOLO 格式:xywh 归一化
with open('test/{}.txt'.format(filename),'w') as fo:
    for i,box in enumerate(bbox):
        str = '0 {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(
            (box[0]+x1)/1920,(box[1]+y1)/1080,(box[2]+5)/1920,(box[3]+5)/1080
        )
        fo.writelines(str)
