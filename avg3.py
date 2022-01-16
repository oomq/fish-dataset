import numpy as np
import os
import bisect
import math
import matplotlib.pyplot as plt
import xlwt
import xlsxwriter as xls
# from pyecharts.charts import HeatMap
# from pyecharts import options as opts
# from pyecharts.faker import Faker

import seaborn as sns

sns.set()

data_path = r'1023'
result_path_ori = r'output/'


# name_list = ["self.liyu","self.lianyu","self.heiyu","self.caoyu"]

class Track(object):
    def __init__(self):
        self.dis_ob = {'1': [], '2': [], '3': []}
        self.rest_time_frame = 0
        self.rest_time_flag = 0
        self.close_box_time = 0
        self.dis = []
        self.v_frame = []

        ##hotmap
        self.hotmap_mat = np.zeros((10, 19), dtype='int32')
        self.hotmap_width = np.linspace(0, 1920, 19)
        self.hotmap_highth = np.linspace(0, 1080, 10)


class Fun(object):
    def __init__(self, data_path_ori, data_base_name, result_path):
        super().__init__()
        self.data_path_ori = data_path_ori
        self.data_base_name = data_base_name
        self.result_path = result_path
        ###定义
        self.x = 0
        self.y = 0
        self.count_frame = 0
        self.tlwh = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.small_thres = [0] * 4
        self.name_list = ["lianyu", "heiyu", "liyu", "caoyu"]
        self.fish = locals()
        for _name in self.name_list:  # 外部类实例化
            self.fish[_name] = Track()
        ###阈值设置
        self.rest_thres = 3
        ##创建画布
        self.x_c = [0, 2, 4, 6]
        self.x_e = [0.5, 2.5, 4.5, 6.5]
        self.label = ["silver carp", "hybrid snakehead", "carp", "grass carp", ]

    def tlwh2xy(self):  # list->matrix
        ret = np.array(self.tlwh.copy())
        ret[:, :2] += (ret[:, 2:]) / 2
        return ret[:, :2]

    def execute(self):  # 处理一小时的txt
        for self.class_name in ["C", "E"]:
            self.worksheet = xlsoutput.add_worksheet('{}'.format(self.class_name + "{}".format(self.data_base_name)))
            txt_folder_path = self.data_path_ori + self.class_name + "/{}".format(self.data_base_name)
            for num, file in enumerate(os.listdir(txt_folder_path)):
                self.data = np.loadtxt(txt_folder_path + "/{}".format(file), delimiter=',')
                print(num, file)
                self.execute_datas()
            for x_label in range(0,4):
                x = np.mean(self.fish[self.name_list[math.floor(x_label)]].v_frame)/25
                self.worksheet.write_number('A{}'.format(x_label),
                                            np.mean(self.fish[self.name_list[x_label]].v_frame) / 25)



            # 画图
            # self.plot_v(self.class_name)
            # self.plot_rest_time(self.class_name)
            # self.plot_hotmap()
            # self.plot_close_box_time(self.class_name)
            # self.plot_each_dis(self.class_name)
            # self.plot_fulldis(self.class_name)
            # 重新初始化统计
            for _name in self.name_list:  # 外部类实例化
                self.fish[_name] = Track()



    def plot_each_dis(self, class_name):
        for num, _name in enumerate(self.name_list):
            if class_name == "C":
                exec("self.plt_each_dis%s = plt.figure(num='dis{}'.format(_name))" % num)
                plt.ylabel("close_dis/px")
                plt.xlabel("Name")
                label = self.label.copy()
                del label[num]
                print(label)
                plt.xticks([2.25, 4.25, 6.25], label)
                for x_label in range(1, 4):
                    plt.bar(self.x_c[x_label], np.sum(self.fish[_name].dis_ob[str(x_label)]), width=0.5,
                            color='r')
                    # plt.show()

            elif class_name == "E":
                plt.figure(num="dis{}".format(_name))
                for x_label in range(1, 4):
                    plt.bar(self.x_e[x_label], np.sum(self.fish[_name].dis_ob[str(x_label)]), width=0.5,
                            color='b')
                    # plt.show()
                exec(
                    "self.plt_each_dis%s.savefig('{}/dis_{}.jpg'.format(self.result_path, data_path + self.data_base_name + _name))" % num)

    def plot_fulldis(self, class_name):
        if class_name == "C":
            self.plt_fulldis = plt.figure(num="fulldis")
            plt.ylabel("dis/px")
            plt.xlabel("Name")
            plt.xticks(self.x_e + [0.25] * 4, self.label)
            for x_label in range(0, 4):
                plt.bar(self.x_c[x_label], np.sum(self.fish[self.name_list[math.floor(x_label)]].dis) / 25, width=0.5,
                        color='r')
            # plt.show()
        elif class_name == "E":
            plt.figure(num="fulldis")
            for x_label in range(0, 4):
                plt.bar(self.x_e[x_label], np.sum(self.fish[self.name_list[math.floor(x_label)]].dis) / 25,
                        width=0.5, color='b')
            # plt.show()
            self.plt_fulldis.savefig("{}/fulldis_{}.jpg".format(self.result_path, data_path + self.data_base_name))

    def plot_close_box_time(self, class_name):
        if class_name == "C":
            self.plt_close_box_time = plt.figure(num="close_box_time")
            plt.ylabel("time/s")
            plt.xlabel("Name")
            plt.xticks(self.x_e + [0.25] * 4, self.label)
            for x_label in range(0, 4):
                plt.bar(self.x_c[x_label], self.fish[self.name_list[math.floor(x_label)]].close_box_time / 25,
                        width=0.5, color='r')
            # plt.show()
        elif class_name == "E":
            plt.figure(num="close_box_time")
            for x_label in range(0, 4):
                plt.bar(self.x_e[x_label], self.fish[self.name_list[math.floor(x_label)]].close_box_time / 25,
                        width=0.5, color='b')
            # plt.show()
            self.plt_close_box_time.savefig(
                "{}/close_{}.jpg".format(self.result_path, data_path + self.data_base_name))

    def plot_hotmap(self):  ##没运行过
        for _name in self.name_list:
            x_axis = self.fish[_name].hotmap_width
            y_axis = self.fish[_name].hotmap_highth
            fig = plt.figure()
            sns_plot = sns.heatmap(self.fish[_name].hotmap_mat, cmap="RdBu_r", linewidths=.5)
            # vmin=0, vmax=24000
            # annot=True, fmt="d"####画图参数 显示数字、类型是int
            # fig.savefig("heatmap.pdf", bbox_inches='tight') # 减少边缘空白
            # plt.show()
            fig.savefig("{}/{}.jpg".format(self.result_path, data_path + self.class_name + self.data_base_name + _name))

    def plot_v(self, class_name, ):  ##待改
        if class_name == "C":
            self.plt_v = plt.figure(num="v")
            plt.ylabel("V/(px/s)")
            plt.xlabel("Name")
            plt.xticks(self.x_e + [0.25] * 4, self.label)
            for x_label in range(0, 4):
                plt.bar(self.x_c[x_label], np.mean(self.fish[self.name_list[math.floor(x_label)]].v_frame) / 25,
                        width=0.5, color='r')
            # plt.show()
        elif class_name == "E":
            plt.figure(num="v")
            for x_label in range(0, 4):
                plt.bar(self.x_e[x_label], np.mean(self.fish[self.name_list[math.floor(x_label)]].v_frame) / 25,
                        width=0.5, color='b')
            # plt.show()
            self.plt_v.savefig("{}/V_{}.jpg".format(self.result_path, data_path + self.data_base_name))

    def plot_rest_time(self, class_name):
        if class_name == "C":
            self.plt_rest_time = plt.figure(num="rest_time")
            plt.ylabel("rest_time/s")
            plt.xlabel("Name")
            plt.xticks(self.x_e + [0.25] * 4, self.label)
            for x_label in range(0, 4):
                plt.bar(self.x_c[x_label], np.sum(self.fish[self.name_list[math.floor(x_label)]].rest_time_frame) / 25,
                        width=0.5, color='r')
            # plt.show()
        elif class_name == "E":
            plt.figure(num="rest_time")
            for x_label in range(0, 4):
                plt.bar(self.x_e[x_label], np.sum(self.fish[self.name_list[math.floor(x_label)]].rest_time_frame) / 25,
                        width=0.5, color='b')
            # plt.show()
            self.plt_rest_time.savefig("{}/Rest_{}.jpg".format(self.result_path, data_path + self.data_base_name))

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
        # print("small_thres",self.small_thres)

    def execute_datas(self):
        flag = 0
        for i, line in enumerate(self.data):  # data（txt）
            # 初始化
            self.renewtlwh(i)
            if self.data[i, 0] in range(1, 3):  # 初始化前两帧 帧从2开始 warning
                continue
            # self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离
            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])
            # if id == 3:
            self.each_hotmap(id)
            # 等更新完一个tlwh再算个体距离
            if frame != int(self.data[i - 1, 0]):
                cxcy = self.tlwh2xy()
                if flag == 0:
                    pcxcy = cxcy
                    flag = 1
                self.each_close_dis(cxcy)  # 个体间距
                self.count_frame += 1
                v_dis_mat = cxcy - pcxcy  # v_dis_mat：这帧减上一帧中心点
                self.each_v(v_dis_mat)  # 平均速度
                self.each_rest_time(v_dis_mat)  # 静息时间
                self.ecah_fulldis(v_dis_mat)  # 游泳距离
                pcxcy = cxcy
        self.each_close_box_time()  # 靠墙时间
        # print('d')
        # self.each_avg_v()

    def avg_tools(self, list, frame_interval):  # 求平均函数
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

    def each_avg_v(self):  # bug 输出的不是列表
        # self.lianyu.v_frame = self.avg_tools(self.lianyu.v_frame,frame_interval=25*60*35)
        # self.liyu.v_frame = self.avg_tools(self.liyu.v_frame, frame_interval=25*60*35)
        # self.heiyu.v_frame = self.avg_tools(self.heiyu.v_frame, frame_interval=25*60*35)
        # self.caoyu.v_frame = self.avg_tools(self.caoyu.v_frame, frame_interval=25*60*35)
        for name_num, name in enumerate(self.name_list):
            self.fish[name].v_frame = self.avg_tools(self.fish[name].v_frame, frame_interval=25 * 60 * 35)

    def each_v(self, v_dis_mat):
        # self.lianyu.v_frame.append((v_dis_mat[0,0]**2 + v_dis_mat[0,1]**2)**0.5)
        # self.heiyu.v_frame.append((v_dis_mat[1,0]**2 + v_dis_mat[1,1]**2)**0.5)
        # self.liyu.v_frame.append((v_dis_mat[2,0]**2 + v_dis_mat[2,1]**2)**0.5)
        # self.caoyu.v_frame.append((v_dis_mat[3,0]**2 + v_dis_mat[3,1]**2)**0.5)
        for name_num, name in enumerate(self.name_list):
            self.fish[name].v_frame.append((v_dis_mat[name_num, 0] ** 2 + v_dis_mat[name_num, 1] ** 2) ** 0.5)

    def ecah_fulldis(self, v_dis_mat):
        for name_num, name in enumerate(self.name_list):
            self.fish[name].dis.append((v_dis_mat[name_num, 0] ** 2 + v_dis_mat[name_num, 1] ** 2) ** 0.5)

    def each_rest_time(self, v_dis_mat):
        for name_num, name in enumerate(self.name_list):
            if (v_dis_mat[name_num, 0] ** 2 + v_dis_mat[name_num, 1] ** 2) ** 0.5 <= self.rest_thres:
                self.fish[name].rest_time_frame += 1

    def each_hotmap(self, id):
        _name = self.name_list[id]
        hotmap_x = bisect.bisect(self.fish[_name].hotmap_width, self.x)  # 找x，y在哪个网格
        hotmap_y = bisect.bisect(self.fish[_name].hotmap_highth, self.y)
        self.fish[_name].hotmap_mat[hotmap_y, hotmap_x] += 1

    def each_close_dis(self, cxcy):
        each_dis_mat = np.zeros((4, 4), dtype='int32')  # 初始化4*4二维矩阵存相对距离
        for col in range(0, 4):  # 循环计算各个点与其他点的距离（包括自身）
            for row in range(0, 4):
                each_dis_mat[col, row] = ((cxcy[col, 0] - cxcy[row, 0]) ** 2 +
                                          (cxcy[col, 0] - cxcy[row, 0]) ** 2) ** 0.5
        for name_num, name in enumerate(self.name_list):
            string = [0, 1, 2, 3]
            string.remove(name_num)  # 除掉自身的数据保存在其他dis_obx的属性里
            for num, string_col in enumerate(string):
                # idea 1
                self.fish[name].dis_ob[str(num + 1)].append(each_dis_mat[name_num, string_col])
                # idea 2
                # eval("self."+name + ".dis_ob[str(num+1)].append(each_dis_mat[name_num,string_col])")
                # print("self."+name + ".dis_ob[str(num+1)].append(each_dis_mat[name_num,string_col])")
        # print('d')

    def each_close_box_time(self):
        # 思路是把热图矩阵中间区域置0，直接求和计算贴壁的帧的总数
        limx1, limy1 = 4, 1  # 没调试贴壁空间
        limx2, limy2 = 16, 8
        for _name in self.name_list:
            each_fish_mat = self.fish[_name].hotmap_mat.copy()
            each_fish_mat[limy1:limy2, limx1:limx2] = 0
            self.fish[_name].close_box_time = np.sum(each_fish_mat)


if __name__ == '__main__':
    xlsoutput = xls.Workbook("track-test.xlsx")
    for data_path in ["1020", "1023", "1026"]:
        data_path_ori = r'plt/{}'.format(data_path)
        for test, data_path_basename in enumerate(os.listdir(data_path_ori + "C")):  # 用data_path 里判断文件名后直接用C+E去找
            # if test == 1:
            #     break
            result_path = os.path.join(result_path_ori + data_path, data_path_basename)
            if not os.path.exists(result_path):
                os.makedirs(result_path)
            fun = Fun(data_path_ori, data_path_basename, result_path)
            fun.execute()  # 处理一小时的C+E
            plt.close('all')  # 关闭所有画布
    xlsoutput.close()

    # for idx in range(0,4):
    #     for _class_name in class_name:
    #         for data_path in ["1020", "1023", "1026"]:#
    #             data_path_ori = r'plt/{}'.format(data_path+_class_name)
    #             print(data_path_ori,os.listdir(data_path_ori)[idx])
    #             result_path=os.path.join(result_path_ori+str(idx)+_class_name)
    #             if not os.path.exists(result_path):
    #                 os.makedirs(result_path)