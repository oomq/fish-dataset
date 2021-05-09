import numpy as np
import matplotlib.pyplot as plt

# boxes = np.array([[100, 100, 210, 210, 0.72],
#                   [250, 250, 420, 420, 0.8],
#                   [220, 220, 320, 330, 0.92],
#                   [100, 100, 210, 220, 0.72],
#                   [230, 240, 325, 330, 0.81],
#                   [220, 230, 315, 340, 0.9]])  # 【文本框样本，格式：【x1,y1,x2,y2,scoer】】

# boxes = np.array([[0, 0, 100, 100, 0.72],
#                   [50, 50, 100, 100, 0.8],
#                   [220, 220, 320, 330, 0.92],
#                   [100, 100, 210, 220, 0.72],
#                   [230, 240, 325, 330, 0.81],
#                   [220, 230, 315, 340, 0.9]])  # 【文本框样本，格式：【x1,y1,x2,y2,scoer】】

boxes = np.array([[0, 0, 100, 100, 0.72],
                  [50, 0, 150, 100, 0.8],
                  [200, 200, 300, 300, 0.92],
                  [300, 300, 400, 400, 0.9]])  # 【文本框样本，格式：【x1,y1,x2,y2,scoer】】



def py_cpu_nms(dets, thresh):
    # dets:(m,5)  thresh:scaler

    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]  # 取出坐标

    areas = (y2 - y1 + 1) * (x2 - x1 + 1)  # 计算面积
    scores = dets[:, 4]  # 取出分数
    keep = []

    index = scores.argsort()[::-1]  # .argsort()是从小到大排列，这整体为取出最大分数的序号

    while index.size > 0:
        i = index[0]  # 取出最大的，加到keep里
        keep.append(i)

        x11 = np.maximum(x1[i], x1[index[1:]])  # 计算有多少点是重复的为计算重合率做准备， np.maximum为取比较大的。所以可以算出重合的。
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])

        w = np.maximum(0, x22 - x11 + 1)  # 最大和最小坐标相减，是重合部分的宽
        h = np.maximum(0, y22 - y11 + 1)  # 最大和最小坐标相减，是重合部分的长

        overlaps = w * h  # 重叠部分面积

        ious = overlaps / (areas[i] + areas[index[1:]] - overlaps)  # 计算iou

        idx = np.where(ious >= thresh)[0]  ## np.where(condition)输出符合条件的thresh应该是阈值

        index = index[idx + 1]  # because index start from 1

    return keep

def plot_bbox(dets, c='k',tip='1'):
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    plt.figure()
    plt.plot([x1, x2], [y1, y1], c)
    plt.plot([x1, x1], [y1, y2], c)
    plt.plot([x1, x2], [y2, y2], c)
    plt.plot([x2, x2], [y1, y2], c)
    plt.title(tip)
    plt.show()

if __name__ == '__main__':
    # plot_bbox(boxes, 'k','before')  # before nms
    print(boxes)
    print('nms')
    keep = py_cpu_nms(boxes, thresh=0.2)
    print(boxes[keep])
    print('keep',keep)
    # plot_bbox(boxes[keep], 'r','after')  # after nms
