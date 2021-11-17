import numpy as np
import os
import bisect
import math
import matplotlib.pyplot as plt
# from pyecharts.charts import HeatMap
# from pyecharts import options as opts
# from pyecharts.faker import Faker

import seaborn as sns
sns.set()

data_path = r'test'
result_path = r'test'

# name_list = ["self.liyu","self.lianyu","self.heiyu","self.caoyu"]

class Track(object):
    def __init__(self):
        self.dis_ob= {'1':[],'2':[],'3':[]}
        self.rest_time = []
        self.rest_time_flag = 0
        self.close_box_time = []
        self.v_frame =[]

        ##hotmap
        self.hotmap_mat = np.zeros((10,19),dtype='int32')
        self.hotmap_width = np.linspace(0,1920,19)
        self.hotmap_highth = np.linspace(0,1080,10)


class Fun(object):
    def __init__(self, data_path, result_path):
        super().__init__()
        self.data_path = data_path
        self.result_path = result_path
        self.count_frame = 0
        self.tlwh = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.small_thres = [0] * 4
        self.name_list = ["liyu","lianyu","heiyu","caoyu"]
        self.fish = locals()
        for _name in self.name_list:#外部类实例化
            self.fish[_name] = Track()

    def tlwh2xy(self):#list->matrix
        ret = np.array(self.tlwh.copy())
        ret[:,:2] += (ret[:,2:])/2
        return ret[:,:2]

    def execute(self):
        for num,file in enumerate(os.listdir(data_path)):
            self.data = np.loadtxt(data_path+"/{}".format(file), delimiter=',')
            print(num, file)
            self.execute_datas()
            if num == 1:#看对比组和实验组有多少个txt
                lianyu_v = np.mean(self.fish['lianyu'].v_frame) * 25  #如下也是一样改成这样
                # liyu_v = np.mean(self.liyu.v_frame) * 25
                # caoyu_v = np.mean(self.caoyu.v_frame) * 25
                # heiyu_v = np.mean(self.heiyu.v_frame) * 25
                self.fish['lianyu'].v_frame = []
                # self.liyu.v_frame = []
                # self.caoyu.v_frame = []
                # self.heiyu.v_frame = []
                print('record')



    def plot(self):##待改
        pass
        plt.figure(figsize=(10, 5))
        plt.bar("spotted silver carp(C)", lianyu_v, width=0.5,color= 'b') #鲢鱼
        plt.bar("spotted silver carp(E)", [np.mean(self.lianyu.v_frame) * 25, ], width=0.5,color= 'r')
        plt.bar("grass carp(C)", liyu_v,  width=0.5,color= 'b') #草鱼
        plt.bar("grass carp(E)", [np.mean(self.caoyu.v_frame) * 25, ], width=0.5,color= 'r')  # 草鱼
        plt.bar("carp(C)", caoyu_v , width=0.5,color= 'b')#鲤鱼
        plt.bar("carp(E)", [np.mean(self.liyu.v_frame) * 25, ], width=0.5,color= 'r')
        plt.bar("hybrid snakehead(C)", heiyu_v , width=0.5,color= 'b')#杂交鳢
        plt.bar("hybrid snakehead(E)", [np.mean(self.heiyu.v_frame) * 25, ], width=0.5,color= 'r')
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
            if self.data[i, 0] in range(1, 3):  # 初始化前两帧 帧从2开始 warning
                continue
            # self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离
            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])
            # if id == 3:
            self.each_hotmap(id)
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


    def avg_tools(self,list, frame_interval):#求平均函数
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

    def each_avg_v(self):#bug 输出的不是列表
        # self.lianyu.v_frame = self.avg_tools(self.lianyu.v_frame,frame_interval=25*60*35)
        # self.liyu.v_frame = self.avg_tools(self.liyu.v_frame, frame_interval=25*60*35)
        # self.heiyu.v_frame = self.avg_tools(self.heiyu.v_frame, frame_interval=25*60*35)
        # self.caoyu.v_frame = self.avg_tools(self.caoyu.v_frame, frame_interval=25*60*35)
        for name_num, name in enumerate(self.name_list):
            locals()[name].v_frame = self.avg_tools(locals()[name].v_frame, frame_interval=25 * 60 * 35)

    def each_v(self,pcxcy,cxcy):
        v_dis_mat = cxcy-pcxcy
        # self.lianyu.v_frame.append((v_dis_mat[0,0]**2 + v_dis_mat[0,1]**2)**0.5)
        # self.heiyu.v_frame.append((v_dis_mat[1,0]**2 + v_dis_mat[1,1]**2)**0.5)
        # self.liyu.v_frame.append((v_dis_mat[2,0]**2 + v_dis_mat[2,1]**2)**0.5)
        # self.caoyu.v_frame.append((v_dis_mat[3,0]**2 + v_dis_mat[3,1]**2)**0.5)
        for name_num, name in enumerate(self.name_list):
            locals()[name].v_frame.append((v_dis_mat[name_num,0]**2 + v_dis_mat[name_num,1]**2)**0.5)

    def each_rest_time(self,v_dis_mat):
        for name_num, name in enumerate(self.name_list):




    def plot_hotmap(self):##没运行过
        for _name in self.name_list:
            x_axis = self.fish[_name].hotmap_width
            y_axis = self.fish[_name].hotmap_highth
            fig = plt.figure()
            sns_plot = sns.heatmap(self.fish[id].hotmap_mat, cmap="RdBu_r",
                                   vmin=0, vmax=24000, linewidths=.5)
            # annot=True, fmt="d"####画图参数 显示数字、类型是int
            # fig.savefig("heatmap.pdf", bbox_inches='tight') # 减少边缘空白
            plt.show()

    def each_hotmap(self,id):
        _name = self.name_list[id]
        hotmap_x = bisect.bisect(self.fish[_name].hotmap_width,self.x)#找x，y在哪个网格
        hotmap_y = bisect.bisect(self.fish[_name].hotmap_highth,self.y)
        self.fish[_name].hotmap_mat[hotmap_y,hotmap_x] += 1


    def each_dis(self,cxcy):
        each_dis_mat = np.zeros((4,4),dtype='int32')#初始化4*4二维矩阵存相对距离
        for col in range(0,4):#循环计算各个点与其他点的距离（包括自身）
            for row  in range(0,4):
                each_dis_mat[col,row] = ((cxcy[col,0]-cxcy[row,0])**2+
                                         (cxcy[col, 0] - cxcy[row, 0])**2)*0.5

        for name_num, name in enumerate(self.name_list):
            string = [0, 1, 2, 3]
            string.remove(name_num) #除掉自身的数据保存在其他dis_obx的属性里
            for num, string_col in enumerate(string):
                # idea 1
                self.fish[name].dis_ob[str(num+1)].append(each_dis_mat[name_num,string_col])#
                # idea 2
                # eval("self."+name + ".dis_ob[str(num+1)].append(each_dis_mat[name_num,string_col])")
                # print("self."+name + ".dis_ob[str(num+1)].append(each_dis_mat[name_num,string_col])")

        print('d')

    def each_close_wall_time(self):
        #思路是把热图矩阵中间区域置0，直接求和计算贴壁的帧的总数
        limx1,limy1= 4,1#没调试贴壁空间
        limx2,limy2 = 16,8
        for _name in self.name_list:
            each_fish_mat = self.fish[_name].hotmap_mat.copy()
            each_fish_mat[limy1:limy2,limx1:limx2] = 0
            self.fish[_name].close_box_time.append(np.sum(each_fish_mat))






if __name__ == '__main__':
    fun = Fun(data_path, result_path)
    fun.execute()