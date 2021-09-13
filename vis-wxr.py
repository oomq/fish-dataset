import numpy as np
import os
import xlsxwriter as xls
import math
path_input = "04"  # 源数据
result_path = 'output'
file_thres = 2
big_thres = 27
eval_windows = 25  # 设置统计单元大小
eval_big_windows = 25 * 60 * 30
fr1 = open("scale.txt", 'r')
string = fr1.read()
scale_datas = string.split('\n')



class Fun(object):
    def __init__(self, data_path, result_path):
        super().__init__()
        self.data_path = data_path
        self.result_path = result_path
        self.distance = [[], [], [], [], []]
        self.time = [0] * 5
        self.tlwh = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.vediolen = 0
        self.px = 0
        self.py = 0
        self.x = 0
        self.y = 0
        self.unit_dis = 0
        self.each_file_distance = []
        self.each_file_time = []
        self.second_dis = [[], [], [], [], []]
        self.second_id_dis = [[], [], [], [], []]
        self.second_id_time = [0] * 5
        self.second_id_rest_time = [0] * 5
        self.second_rest_time =[]
        self.second_v = []
        self.halfhour_id_dis = [[], [], [], [], []]
        self.halfhour_id_time = [0] * 5
        self.halfhour_v = []

        self.second_acc =[]
        self.fish_var =[]
        self.var_x =[]
        self.var_y=[]

        # 转弯
        self.angle = [0.0] * 5  # 角度
        self.swerves = [] # 转弯次数
        self.swerve_px = [0.0] * 5
        self.swerve_py = [0.0] * 5
        self.swerve_angle1 = 0.0
        self.swerve_angle = [0.0] * 5
        self.swerve_k = [0] * 5
        self.k = 0
        #
        self.small_thres = [0]*5
        self.count_frame = 0

        self.file_id_v =[[], [], [], [], []]
        self.file_id_i =[0] * 5
        # self.scale = 0
        # for line in scale_datas:
        #     q = [x for x in line.split(' ')]
        #     if q[0] == self.data_path:
        #         width = q[3]
        #         self.scale = 350 / int(width)
        #         break
        # self.small_thres = 1 / self.scale - 0.6

    def float2int(date):
        return int(date)

    def execute(self):
        for num, file in enumerate(os.listdir(self.data_path)):
            if int(file.replace(".txt", "").replace(self.data_path + "-", "")) != file_thres:
                # print(num, file)
                continue
            print(num, file)
            self.data = np.loadtxt(self.data_path + "/{}".format(file), delimiter=',')
            if num == 0:
                self.vediolen = int(self.data[int(self.data.shape[0]) - 1, 0])
            self.execute_datas()
        self.second_acceleration()
        self.xls_writer()
        print('writing')

    def renewtlwh(self, i):
        id = int(self.data[i, 1]) - 1
        if np.any(np.array(self.tlwh) == 0):
            self.tlwh[id][0] = self.data[i, 2]  # t
            self.tlwh[id][1] = self.data[i, 3]  # l
            self.tlwh[id][2] = self.data[i, 4]  # w
            self.tlwh[id][3] = self.data[i, 5]  # h
            return

        self.px = self.tlwh[id][0] + self.tlwh[id][2] / 2
        self.py = self.tlwh[id][1] + self.tlwh[id][3] / 2
        self.small_thres[id] = math.sqrt((self.tlwh[id][2] + self.tlwh[id][3])/100)
        self.tlwh[id][0] = self.data[i, 2]  # t
        self.tlwh[id][1] = self.data[i, 3]  # l
        self.tlwh[id][2] = self.data[i, 4]  # w
        self.tlwh[id][3] = self.data[i, 5]  # h
        self.x = self.tlwh[id][0] + self.tlwh[id][2] / 2
        self.y = self.tlwh[id][1] + self.tlwh[id][3] / 2


    def execute_datas(self):
        for i, line in enumerate(self.data):
            self.renewtlwh(i)
            if self.data[i, 0] in range(1, 6):  # 初始化前两帧 帧从2开始 warning
                continue
            self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离
            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])
            if frame != int(self.data[i - 1, 0]):
                self.count_frame += 1
            self.fishing_var(frame, id, i)
            self.second_record(frame, id, i)
            self.swerve(id,i)
            self.halfhour_record(frame, id, i)

    def second_acceleration(self):
        for num in range(0,len(self.second_v)-1):
            self.second_acc.append(self.second_v[num] - self.second_v[num+1])

    def fishing_var(self,frame, id, i):
        if self.count_frame % eval_windows != 0:
            for t,l,w,h in self.tlwh:
                if w !=0:
                    self.var_x.append(t + w/2)
                    self.var_y.append(l + h/2)
        else:
            if frame != int(self.data[i - 1, 0]):
                self.var_x, self.var_y = [],[]
                for t,l,w,h in self.tlwh:
                    if w !=0:
                        self.var_x.append(t + w/2)
                        self.var_y.append(l + h/2)
                self.fish_var.append(np.var(self.var_x)+np.var(self.var_y))
                return
            else:
                self.var_x, self.var_y = [],[]
                for t,l,w,h in self.tlwh:
                    if w !=0:
                        self.var_x.append(t + w/2)
                        self.var_y.append(l + h/2)

    # def swerve(self):
    # def renew_(self):

    def swerve(self,id,i):
        if self.count_frame % eval_windows != 0:
            dis = ((self.x - self.swerve_px[id]) ** 2 + (self.y - self.swerve_py[id]) ** 2) ** 0.5
            if self.swerve_k[id] == 0:
                self.swerve_px[id] = self.x
                self.swerve_py[id] = self.y
                self.swerve_k[id] = 1
            elif self.swerve_k[id] == 1:
                tan = math.atan2(self.y-self.swerve_py[id],self.x-self.swerve_px[id])
                self.swerve_angle[id] = math.degrees(tan)
                self.swerve_px[id] = self.x
                self.swerve_py[id] = self.y
                self.swerve_k[id] = 2
            elif dis>= self.small_thres[id] * 2 and dis <= big_thres:
                tan = math.atan2(self.y-self.swerve_py[id], self.x-self.swerve_px[id])

                self.swerve_angle1 = math.degrees(tan)
                self.angle[id] += math.degrees(tan) - self.swerve_angle[id]
                self.swerve_angle[id] = math.degrees(tan)
                self.swerve_px[id] = self.x
                self.swerve_py[id] = self.y
            if round(self.angle[id],1) >=90.0 or round(self.angle[id],1) <= -90.0:
                self.k +=1

                self.angle[id] = 0.0
                # print("{} ok".format(self.swerves))
        else:
            if self.data[i,0] != self.data[i-1,0]:
                self.swerves.append(self.k)

    def halfhour_record(self,frame,id,i):
        if self.count_frame % eval_big_windows != 0:
            if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                self.halfhour_id_dis[id].append(self.unit_dis)
                self.halfhour_id_time[id] +=1
        else:
            if frame != int(self.data[i - 1, 0]):
                x_dis, x_time = 0, 0
                for x in range(0, 5):
                    x_dis += np.sum(self.halfhour_id_dis[x])  ##mean
                    x_time += np.mean(self.halfhour_id_time[x])
                if x_time == 0:
                    self.halfhour_v.append(0)
                else:
                    self.halfhour_v.append(x_dis / x_time)  # 缺scale.txt
                # 重新初始化
                self.halfhour_id_dis = [[], [], [], [], []]
                self.halfhour_id_time = [0] * 5
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.halfhour_id_dis[id].append(self.unit_dis)
                    self.halfhour_id_time[id] += 1
                return
            else:
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.halfhour_id_dis[id].append(self.unit_dis)
                    self.halfhour_id_time[id] += 1


    def second_record(self, frame, id, i):
        if self.count_frame % eval_windows != 0:
            if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                self.second_id_dis[id].append(self.unit_dis)
                self.second_id_time[id] += 1
                self.file_id_v[id].append(self.unit_dis)
            elif self.unit_dis < self.small_thres[id]:
                self.second_id_rest_time[id] += 1
        else:
            if frame != int(self.data[i - 1, 0]):#避免更新单元重复计算
                x_dis, x_time, rest_time = 0, 0, 0
                for x in range(0, 5):

                    x_dis += np.sum(self.second_id_dis[x])  ##mean
                    x_time += np.mean(self.second_id_time[x])
                    rest_time += np.mean(self.second_id_rest_time[x])
                # if x_dis ==0:
                #     print(x_time)
                self.second_rest_time.append(rest_time)
                if x_time == 0:
                    self.second_v.append(0)
                else:
                    self.second_v.append(x_dis / x_time)  # 缺scale.txt
                # 重新初始化

                self.second_id_dis = [[], [], [], [], []]
                self.second_id_time = [0] * 5
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.second_id_dis[id].append(self.unit_dis)
                    self.second_id_time[id] += 1
                    self.file_id_v[id].append(self.unit_dis)
                elif self.unit_dis < self.small_thres[id]:
                    self.second_id_rest_time[id] += 1
                return
            else:
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.second_id_dis[id].append(self.unit_dis)
                    self.second_id_time[id] += 1
                elif self.unit_dis < self.small_thres[id]:
                    self.second_id_rest_time[id] += 1

                # 单文件
                # self.distance[id].append(self.unit_dis)
                # self.time[id] += 1
                # print('d')
                # x_dis =0
                # for x in range(0,6):
                #     x_dis += self.second_id_dis[x]

                # for a,b in zip(self.second_id_dis,self.second_id_time):
                #     if b!=0:
                #         v = a/b
                #     else:
                #         continue
                #     self.second_id_v.append(v)
                # self.second_id_dis =[[],[],[],[],[]]
                # self.second_id_time= [0]*5

                # 单文件
                # x_dis = 0
                # for x in range(0,5):
                #     x_dis+=np.sum(self.distance[x])
                # self.each_file_distance.append(x_dis)

    def xls_writer(self):

        worksheet = workbook.add_worksheet("{}".format(self.data_path))
        #判断文件类型

        worksheet.write_column('A1', self.second_v)  # 需要判断哪个单元开始
        worksheet.write_column('B1', self.second_rest_time)
        worksheet.write_column('C1', self.halfhour_v)
        worksheet.write_column('D1',self.second_acc)
        worksheet.write_column('E1',self.fish_var)
        worksheet.write_column('F1',self.swerves)


if __name__ == '__main__':
    #init scale
    #多文件
    # workbook = xls.Workbook(result_path+"/track.xlsx")
    # for line in scale_datas:
    #     q = [x for x in line.split(' ')]
    #     print(q[0])
    #     fun = Fun(q[0], result_path)
    #     fun.execute()
    # workbook.close()

    # 单文件
    workbook = xls.Workbook("track.xlsx")
    fun = Fun(path_input, result_path)
    fun.execute()
    workbook.close()

# 分区间统计
# from itertools import groupby
#
# lst = [
#     2648, 2648, 2648, 63370, 63370, 425, 425, 120,
#     120, 217, 217, 189, 189, 128, 128, 115, 115, 197,
#     19752, 152, 152, 275, 275, 1716, 1716, 131, 131,
#     98, 98, 138, 138, 277, 277, 849, 302, 152, 1571,
#     68, 68, 102, 102, 92, 92, 146, 146, 155, 155,
#     9181, 9181, 474, 449, 98, 98, 59, 59, 295, 101, 5
# ]
#
# for k, g in groupby(sorted(lst), key=lambda x: x // 50):
#     print('{}-{}: {}'.format(k * 50, (k + 1) * 50 - 1, len(list(g))))
