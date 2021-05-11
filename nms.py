from typing import Any

import numpy as np
import matplotlib.pyplot as plt

# boxes = np.array([
#     [100, 100, 210, 210, 0.72],  # 0
#     [280, 290, 420, 420, 0.8],  # 1
#     [220, 220, 320, 330, 0.92],  # 2
#     [105, 90, 220, 210, 0.71],  # 3
#     [230, 240, 325, 330, 0.81],  # 4
#     [305, 300, 420, 420, 0.9],  # 5
#     [215, 225, 305, 328, 0.6],  # 6
#     [150, 260, 290, 400, 0.99],  # 7
#     [102, 108, 208, 208, 0.72]])  # 8  #9个框

boxes = np.array([
    [100, 100, 210, 210, 0.72],  # 0
    [105, 90, 220, 210, 0.71],  # 3
    [150, 108, 220, 230, 0.3]])  # 8  #9个框


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

        idx = np.where(ious <= thresh)[0]  ## np.where(condition)输出符合条件的thresh应该是阈值

        index = index[idx + 1]  # because index start from 1

    return keep


def non_max_suppression_fast(boxes,probs,Nt=0.3,sigma=0.5,overlap_thresh=0.001,method=2):

    dets = boxes
    N = dets.shape[0]
    indexes = np.array([np.arange(N)])
    dets = np.concatenate((dets,indexes.T),axis=1)

    y1 = dets[:, 1]
    x1 = dets[:, 0]
    y2 = dets[:, 3]
    x2 = dets[:, 2]
    scores = probs
    areas = (x2-x1+1)*(y2-y1+1)

    for i in range(N):
        tBD = dets[i, :].copy()
        tscore = scores[i].copy()
        tarea = areas[i].copy()
        pos = i+1

        if i !=N-1:
            maxscore = np.max(scores[pos:],axis=0)
            maxpos = np.argmax(scores[pos:],axis=0)
        else:
            maxscore = scores[-1]
            maxpos = 0
        if tscore<maxscore:
            dets[i, :] = dets[maxpos+i+1, :]
            dets[maxpos+i+1, :] = tBD
            tBD = dets[i,:]

            scores[i] = scores[maxpos+i+1]
            scores[maxpos+i+1] = tscore
            tscore = scores[i]

            areas[i] = areas[maxpos+i+1]
            areas[maxpos+i+1] = tarea
            tarea = areas[i]

        xx1 = np.maximum(dets[i,0],dets[pos:,0])
        yy1 = np.maximum(dets[i,1],dets[pos:,1])
        xx2 = np.minimum(dets[i,2],dets[pos:,2])
        yy2 = np.minimum(dets[i,3],dets[pos:,3])

        w = np.maximum(0.0,xx2-xx1+1)
        h = np.maximum(0.0,yy2-yy1+1)
        inter = w*h
        ovr = inter/(areas[i]+areas[pos:]-inter)

        if method ==1:
            weight = np.ones(ovr.shape)
            weight[ovr>Nt] = weight[ovr>Nt]-ovr[ovr>Nt]
        elif method == 2:
            weight = np.exp(-(ovr*ovr)/sigma)
        else:
            weight = np.ones(ovr.shape)
            weight[ovr>Nt] = 0

        scores[pos:] = weight*scores[pos:]

    inds = dets[:, 4][scores>overlap_thresh]
    keep = inds.astype(int)
    keeps = keep.tolist()
    boxes = boxes[keeps].astype("int")
    probs = probs[keeps]

    return boxes,probs


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
    plot_bbox(boxes, 'k','before')  # before nms
    # keep = py_cpu_nms(boxes, thresh=0.5)
    keep,probs = non_max_suppression_fast(boxes[:,:4],probs=boxes[:,4],Nt=0.3,sigma=0.5,overlap_thresh=0.001,method=2)
    plot_bbox(keep, 'r','after')  # after nms
