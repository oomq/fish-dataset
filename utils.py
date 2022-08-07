import numpy as np
import math

def angle_2vet(line):
    pointA, pointB, pointC = (line[0], line[1]), (line[2], line[3]), (line[4], line[5])
    pointA = np.array(pointA)
    pointB = np.array(pointB)
    pointC = np.array(pointC)
    dy, dx = pointB - pointA
    angel_head = math.atan2(dy, dx)
    dy, dx = pointB - pointC
    angel_tail = math.atan2(dy, dx)
    # if angel_head>math.pi:
    return math.degrees(angel_head - angel_tail)


def get_distance_point2line( line):  ##  计算点到直线的距离
    """
    Args:
        point: [x0, y0]
        line: [x1, y1, x2, y2]
    """
    point = (line[4], line[5])  ##keypointtail
    line_point1, line_point2 = np.array(line[0:2]), np.array(line[2:4])
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    m = np.linalg.norm(line_point1 - line_point2)
    if m == 0:
        # print('error')
        return 0
    else:
        distance = np.abs(np.cross(vec1, vec2)) / m
    return distance

def xydis(mat):
    return (mat[0]**2 +mat[1]**2)**0.5

def tlwh2xy(tlwh):  # list->matrix
    ret = np.array(tlwh.copy())
    ret[:, :2] =ret[:, :2] + (ret[:, 2:]) / 2
    return ret[:, :2]

def float2int(date):
    return int(date)

def angle(point1,point2):
    return math.atan2(point1[1]-point2[1],point1[0]-point2[0])