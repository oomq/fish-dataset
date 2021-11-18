import cv2
import numpy as np
import matplotlib.pyplot as plt
# TRIANGLE阈值处理
filename = 'five'
# src = cv2.imread(r'test/{}.png'.format(filename), cv2.IMREAD_GRAYSCALE)
img = cv2.imread(r'test/{}.png'.format(filename))
src = img[:,:,2]


#裁剪边缘，以免影响连通域面积
# x1 = 100
# x2 = 1800
# y1 = 30
# src = src[y1:,x1:x2]
# src = cv2.GaussianBlur(src, (101, 101), 1)


src = cv2.blur(src,(4,4))
# cv2.imshow('Canny-ori', src)
import cv2
import numpy as np

'''
# img = cv2.GaussianBlur(src, (3, 3), 0)  # 用高斯平滑处理原图像降噪。
canny = cv2.Canny(src, 20, 50)  # 最大最小阈值
cv2.imshow('Canny', canny)
cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(5, 5))
diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(3 , 3))
result1 = cv2.dilate(canny,cross)
cv2.imshow('Canny-cross', result1)
result2 = cv2.erode(result1, diamond)
cv2.imshow('Canny-diamond', result2)
cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(7, 7))
result1 = cv2.dilate(result2,cross)
cv2.imshow('Canny-cross1', result1)
result2 = cv2.erode(result1, diamond)
cv2.imshow('Canny-diamond1', result2)
result1 = cv2.dilate(result2,cross)
cv2.imshow('Canny-cross2', result1)
diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
result2 = cv2.erode(result1, diamond)
cv2.imshow('Canny-diamond2', result2)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

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

# cv2.imshow("image", src)
# cv2.imshow('thresh_out', dst_tri)


# cv2.imshow('thresh_out1', dst_tri1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

num,labels= cv2.connectedComponents(dst_tri,4)

# print(num,labels)

label_area = [0]*num
for i in labels:
    for j in i:
        label_area[j] += 1


# print(label_num)
# if num < 6:
#     areamax = max(label_num[1:num+1])
#     area_ind=label_num.index(areamax)
#     print(areamax,area_ind)
areamax =[]
areamax = [(ind + 1) for ind, t in enumerate(label_area[1:num+1]) if (t>1500)]
print(areamax)
# for ind, t in enumerate(label_num[1:num+1]):
#     if (t>1000):
#         areamax.append((ind + 1))


# print(areamax)

# nrr =  ((labels == 1) | (labels == 3) )
# nrr =  ((labels == 1) | (labels == 2)  | (labels == 3) )

current_axis = plt.gca()
# plt.imshow(labels)
# plt.show()
print('d')
###遍历连通域矩阵过滤小面积的噪声
for col,col_val in enumerate(labels) :
    for row,row_val in enumerate(col_val):
        if not row_val in areamax:
            labels[col,row] = 0

# plt.imshow(labels)
# plt.show()

for col,col_val in enumerate(src) :
    for row,row_val in enumerate(col_val):
        if labels[col,row] == 0:
            src[col,row] = 0

canny = cv2.Canny(src, 20, 50)  # 最大最小阈值
cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(5, 5))
diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(3 , 3))
result1 = cv2.dilate(canny,cross)
result2 = cv2.erode(result1, diamond)
cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(7, 7))
result1 = cv2.dilate(result2,cross)
result2 = cv2.erode(result1, diamond)
result1 = cv2.dilate(result2,cross)
diamond = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
result2 = cv2.erode(result1, diamond)
# cv2.imshow('Canny', result2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

canny_mat = labels - result2/255

# cv2.imshow('Canny', canny_mat)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
canny_mat[canny_mat<1] =0
canny_mat=canny_mat.astype(np.int8)

num,canny_labels= cv2.connectedComponents(canny_mat,4)
label_area = [0]*num
for i in canny_labels:
    for j in i:
        label_area[j] += 1
areamax =[]
areamax = [(ind + 1) for ind, t in enumerate(label_area[1:num+1]) if (t>1500)]
for col,col_val in enumerate(canny_labels):
    for row,row_val in enumerate(col_val):
        if not row_val in areamax:
            canny_labels[col,row] = 0

plt.imshow(canny_labels)
plt.show()
mask_label=canny_labels.copy()
mask_label[mask_label > 1] = 0###把2 改成1
mask_label=mask_label.astype(np.uint8)
cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(7, 7))
mask_label_cross = cv2.dilate(mask_label,cross)

other = labels-mask_label_cross
other=other.astype(np.uint8)

plt.imshow(other)
plt.show()
plt.imshow(mask_label_cross)
plt.show()
masked_pic = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=mask_label_cross)
masked_pic2 = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=other)
plt.imshow(masked_pic)
plt.show()
plt.imshow(masked_pic2)
plt.show()
print('dd')



#找到》thres的index 然后计算连通域的包围框后，
# bbox =[]
# for conid in areamax:
#     test = np.where(labels==conid)
#     x1 = min(np.where(labels==conid)[1])
#     y1 = min(np.where(labels==conid)[0])
#     x2 = max(np.where(labels==conid)[1])
#     y2 = max(np.where(labels==conid)[0])
#     bbox.append([x1,y1,x2,y2])
#     current_axis.add_patch(plt.Rectangle((x1,y1),x2-x1,y2-y1, color="blue", fill=False, linewidth=2))
#
# plt.show()



# print(bbox)

# YOLO 格式:xywh 归一化
# with open('test/{}.txt'.format(filename),'w') as fo:
#     for i,box in enumerate(bbox):
#         str = '0 {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(
#             (box[0]+x1)/1920,(box[1]+y1)/1080,(box[2]+5)/1920,(box[3]+5)/1080
#         )
#         fo.writelines(str)