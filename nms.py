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

boxes = np.array([[1, 1, 100, 100],
                  [51, 1, 150, 100],

                                    ])  # 【文本框样本，格式：【x1,y1,x2,y2,scoer】】



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

    plt.text(x1, y1,'range(0,5)', size=15, alpha=0.2)
    plt.plot([x1, x2], [y1, y1], c)
    plt.plot([x1, x1], [y1, y2], c)
    plt.plot([x1, x2], [y2, y2], c)
    plt.plot([x2, x2], [y1, y2], c)
    plt.title(tip)
    plt.show()

def iou(bbox, candidates):
    # 计算iou
    """Computer intersection over union.

    Parameters
    ----------
    bbox : ndarray
        A bounding box in format `(top left x, top left y, width, height)`.
    candidates : ndarray
        A matrix of candidate bounding boxes (one per row) in the same format
        as `bbox`.

    Returns
    -------
    ndarray
        The intersection over union in [0, 1] between the `bbox` and each
        candidate. A higher score means a larger fraction of the `bbox` is
        occluded by the candidate.

    """
    bbox_tl, bbox_br = bbox[:2], bbox[:2] + bbox[2:]
    candidates_tl = candidates[:, :2]
    candidates_br = candidates[:, :2] + candidates[:, 2:]

    tl = np.c_[np.maximum(bbox_tl[0], candidates_tl[:, 0])[:, np.newaxis],
               np.maximum(bbox_tl[1], candidates_tl[:, 1])[:, np.newaxis]]
    br = np.c_[np.minimum(bbox_br[0], candidates_br[:, 0])[:, np.newaxis],
               np.minimum(bbox_br[1], candidates_br[:, 1])[:, np.newaxis]]

    wh = np.maximum(0., br - tl)

    area_intersection = wh.prod(axis=1)
    area_bbox = bbox[2:].prod()
    area_candidates = candidates[:, 2:].prod(axis=1)
    return area_intersection / (area_bbox + area_candidates - area_intersection)


def iou_cost(boxes):
    cost_matrix = np.zeros((len(boxes), len(boxes)))
    for row, det in enumerate(boxes):
        cost_matrix[row, :] = iou(det[:5], boxes)
    cost_matrix = np.triu(cost_matrix,1)

    return cost_matrix



if __name__ == '__main__':
    plot_bbox(boxes, 'k','before')  # before nms
    # print(boxes)
    h = iou_cost(boxes)
    # top_tri  = np.triu(h)  # 取上三角函数
    print('keep')
    # plot_bbox(boxes[keep], 'r','after')  # after nms