import numpy as np
import os

import math
import matplotlib.pyplot as plt


data_path = r'test'
result_path = r'test'


class Track(object):
    def __init__(self):
        self.dis_ob1 = []
        self.dis_ob2 = []
        self.dis_ob3 = []
        self.rest_time = []
        self.rest_time_flag = 0
        self.close_box_time = []


class Fun(object):
    def __init__(self, data_path, result_path):
        super().__init__()
        self.data_path = data_path
        self.result_path = result_path
        self.count_frame = 0
        self.liyu = Track()
        self.yu = Track()
        self.heiyu
    def execute(self):
        for num,file in enumerate(os.listdir(data_path)):
            self.data = np.loadtxt(data_path+"/{}".format(file), delimiter=',')
            print(num, file)
            self.execute_datas()

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

        for i, line in enumerate(self.data):
            if i == len(self.data):
                break
            #初始化
            self.renewtlwh(i)
            if self.data[i, 0] in range(1, 5):  # 初始化前两帧 帧从2开始 warning
                continue


            self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离
            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])

            if frame != int(self.data[i - 1, 0]):
                self.count_frame += 1
                self.each_dis()


    def each_dis(self):
        a = self.liyu.rest_time_flag
        print(a)

if __name__ == '__main__':
    fun = Fun(data_path, result_path)
    fun.each_dis()