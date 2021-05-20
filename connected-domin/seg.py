import cv2
import numpy as np
import matplotlib.pyplot as plt
# TRIANGLE阈值处理
src = cv2.imread(r'6.jpg', cv2.IMREAD_GRAYSCALE)
src = cv2.blur(src,(5,5))

triThe = 0
maxval = 255
triThe, dst_tri = cv2.threshold(src, 120, maxval,cv2.THRESH_BINARY_INV)#cv2.THRESH_TRIANGLE + cv2.THRESH_BINARY
# triThe1, dst_tri1 = cv2.threshold(src, triThe, maxval, cv2.THRESH_TRIANGLE + cv2.THRESH_BINARY_INV)
print(triThe)
# print(triThe1)
cv2.imshow("image", src)
cv2.imshow('thresh_out', dst_tri)
# cv2.imshow('thresh_out1', dst_tri1)
cv2.waitKey(0)
cv2.destroyAllWindows()

num,labels= cv2.connectedComponents(dst_tri,4)

print(num,labels)

label_num = [0]*num
for i in labels:
    for j in i:
        label_num[j] += 1
print(label_num)
# if num < 6:
#     areamax = max(label_num[1:num+1])
#     area_ind=label_num.index(areamax)
#     print(areamax,area_ind)

if num < 6:
    areamax = [(ind + 1) for ind, t in enumerate(label_num[1:num+1]) if (t>1000) ]

    # for ind, t in enumerate(label_num[1:num+1]):
    #     if (t>1000):
    #         areamax.append((ind + 1))


print(areamax)

# nrr =  ((labels == 1) | (labels == 3) )
# nrr =  ((labels == 1) | (labels == 2)  | (labels == 3) )
current_axis = plt.gca()
plt.imshow(labels)
# plt.show()


#找到》thres的index 然后计算连通域的包围框后，
bbox =[]
for conid in  areamax:
    test = np.where(labels==conid)
    x1 = min(np.where(labels==conid)[1])
    y1 = min(np.where(labels==conid)[0])
    x2 = max(np.where(labels==conid)[1])
    y2 = max(np.where(labels==conid)[0])
    bbox.append([x1,y1,x2,y2])
    current_axis.add_patch(plt.Rectangle((x1,y1),x2-x1,y2-y1, color="blue", fill=False, linewidth=2))
print(bbox)
plt.show()