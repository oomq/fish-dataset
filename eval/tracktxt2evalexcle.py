import numpy as np
import os
import bisect
import math
import matplotlib.pyplot as plt
from pyecharts.charts import HeatMap
from pyecharts import options as opts
from pyecharts.faker import Faker

import seaborn as sns
sns.set()

data_path = r'test'
result_path = r'test'

name_list = ["self.liyu","self.lianyu","self.heiyu","self.caoyu"]

class Track(object):
    def __init__(self):
        self.dis_ob1 = []
        self.dis_ob2 = []
        self.dis_ob3 = []
        self.rest_time = []
        self.rest_time_flag = 0
        self.close_box_time = []
        self.v_frame =[]


class Fun(object):
    def __init__(self, data_path, result_path):
        super().__init__()
        self.data_path = data_path
        self.result_path = result_path
        self.count_frame = 0
        self.tlwh = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.small_thres = [0] * 5
        self.lianyu = Track()
        self.heiyu = Track()
        self.liyu = Track()
        self.caoyu = Track()

        ##hotmap
        self.hotmap_mat = np.zeros((10,19),dtype='int32')
        self.hotmap_width = np.linspace(0,1920,19)
        self.hotmap_highth = np.linspace(0,1080,10)


    def tlwh2xy(self):#list->matrix
        ret = np.array(self.tlwh.copy())
        ret[:,:2] += (ret[:,2:])/2
        return ret[:,:2]

    def execute(self):
        for num,file in enumerate(os.listdir(data_path)):
            self.data = np.loadtxt(data_path+"/{}".format(file), delimiter=',')
            print(num, file)
            self.execute_datas()

        plt.figure(figsize=(10, 5))
        plt.bar("lianyu", [np.mean(self.lianyu.v_frame) * 25, ], width=0.5)
        plt.bar("caoyu", [np.mean(self.caoyu.v_frame) * 25, ], width=0.5)
        plt.bar("liyu", [np.mean(self.liyu.v_frame) * 25, ], width=0.5)
        plt.bar("heiyu", [np.mean(self.heiyu.v_frame) * 25, ], width=0.5)
        plt.ylabel("V/(px/s)")
        plt.xlabel("Name")
        plt.savefig("output.jpg", )
        plt.show()

    def renewtlwh(self, i):
        id = int(self.data[i, 1]) - 1
        # if self.count_frame == 18:
        #     print(self.count_frame)
        if np.any(np.array(self.tlwh) == 0):
            self.tlwh[id][0] = self.data[i, 2]  # t
            self.tlwh[id][1] = self.data[i, 3]  # l
            self.tlwh[id][2] = self.data[i, 4]  # w
            self.tlwh[id][3] = self.data[i, 5]  # h
            return

        self.px = self.tlwh[id][0] + self.tlwh[id][2] / 2
        self.py = self.tlwh[id][1] + self.tlwh[id][3] / 2
        self.tlwh[id][0] = self.data[i, 2]  # t
        self.tlwh[id][1] = self.data[i, 3]  # l
        self.tlwh[id][2] = self.data[i, 4]  # w
        self.tlwh[id][3] = self.data[i, 5]  # h
        self.x = self.tlwh[id][0] + self.tlwh[id][2] / 2
        self.y = self.tlwh[id][1] + self.tlwh[id][3] / 2
        self.small_thres[id] = math.sqrt((self.tlwh[id][2] + self.tlwh[id][3]) / 100)


    def execute_datas(self):
        flag = 0
        for i, line in enumerate(self.data):
            #初始化
            self.renewtlwh(i)
            if self.data[i, 0] in range(1, 5):  # 初始化前两帧 帧从2开始 warning
                continue
            self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离
            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])
            if id == 3:
                self.each_hotmap()
            #等更新完一个tlwh再算个体距离
            if frame != int(self.data[i - 1, 0]):
                cxcy = self.tlwh2xy()
                if flag == 0:
                    pcxcy = cxcy
                    flag = 1
                self.each_dis(cxcy)
                self.count_frame += 1
                self.each_v(pcxcy,cxcy)
                pcxcy = cxcy
        print('d')
        # self.each_avg_v()


    def avg_tools(self,list, frame_interval):
        n = len(list) % frame_interval
        while n:  # 对于最后的几个数丢弃，不丢弃的话无法组成二维数组
            list.pop()
            n -= 1
        m = len(list) / frame_interval  # m是二维数组的0轴
        arr = np.array(list).reshape(m, frame_interval)  # arr是一个形状为【m，6】的数组
        avg = np.mean(arr, axis=1)  # 求出每行的平均值
        for i in range(0, avg.size):  # 把每行的平均值赋值给这一行
            arr[i] = avg[i]
        return arr.reshape(1, arr.size)[0]  # 返回一个列表

    def each_avg_v(self):
        self.lianyu.v_frame = self.avg_tools(self.lianyu.v_frame,frame_interval=25*60*35)
        self.liyu.v_frame = self.avg_tools(self.liyu.v_frame, frame_interval=25*60*35)
        self.heiyu.v_frame = self.avg_tools(self.heiyu.v_frame, frame_interval=25*60*35)
        self.caoyu.v_frame = self.avg_tools(self.caoyu.v_frame, frame_interval=25*60*35)

    def each_v(self,pcxcy,cxcy):
        v_dis_mat = cxcy-pcxcy
        self.lianyu.v_frame.append((v_dis_mat[0,0]**2 + v_dis_mat[0,1]**2)**0.5)
        self.heiyu.v_frame.append((v_dis_mat[1,0]**2 + v_dis_mat[1,1]**2)**0.5)
        self.liyu.v_frame.append((v_dis_mat[2,0]**2 + v_dis_mat[2,1]**2)**0.5)
        self.caoyu.v_frame.append((v_dis_mat[3,0]**2 + v_dis_mat[3,1]**2)**0.5)



    def plot_hotmap(self):
        x_axis = self.hotmap_width
        y_axis = self.hotmap_highth
        fig = plt.figure()
        sns_plot = sns.heatmap(self.hotmap_mat, cmap="RdBu_r",
                               vmin=0, vmax=24000, linewidths=.5)
        # annot=True, fmt="d"
        # fig.savefig("heatmap.pdf", bbox_inches='tight') # 减少边缘空白
        plt.show()

    def each_hotmap(self):
        hotmap_x = bisect.bisect(self.hotmap_width,self.x)
        hotmap_y = bisect.bisect(self.hotmap_highth,self.y)
        self.hotmap_mat[hotmap_y,hotmap_x] += 1


    def each_dis(self,cxcy):
        # for col,name in enumerate(name_list):
        #     x = cxcy[col,0]
        #     y = cxcy[col,1]
        #     for iteration_time in range(col+1,4):
        #         dis = ((x - cxcy[iteration_time,1]) ** 2 + (y - cxcy[iteration_time,1]) ** 2) ** 0.5
        each_dis_mat = np.zeros((4,4),dtype='int32')#初始化4*4二维矩阵存相对距离
        for col in range(0,4):
            for row  in range(0,4):
                each_dis_mat[col,row] = ((cxcy[col,0]-cxcy[row,0])**2+
                                         (cxcy[col, 0] - cxcy[row, 0])**2)*0.5

        self.lianyu.dis_ob1.append(each_dis_mat[0,1])
        self.lianyu.dis_ob2.append(each_dis_mat[0, 2])
        self.lianyu.dis_ob3.append(each_dis_mat[0, 3])

        self.heiyu.dis_ob1.append(each_dis_mat[1,1])
        self.heiyu.dis_ob2.append(each_dis_mat[1, 2])
        self.heiyu.dis_ob3.append(each_dis_mat[1, 3])

        self.liyu.dis_ob1.append(each_dis_mat[2,1])
        self.liyu.dis_ob2.append(each_dis_mat[2, 2])
        self.liyu.dis_ob3.append(each_dis_mat[2, 3])

        self.caoyu.dis_ob1.append(each_dis_mat[3,1])
        self.caoyu.dis_ob2.append(each_dis_mat[3, 2])
        self.caoyu.dis_ob3.append(each_dis_mat[3, 3])






if __name__ == '__main__':
    fun = Fun(data_path, result_path)
    fun.execute()
