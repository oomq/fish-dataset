import numpy as np
import os
import xlsxwriter as xls
import math
import matplotlib.pyplot as plt
import time
import xlrd
from concurrent.futures import wait, ALL_COMPLETED
import concurrent.futures

path_input = "09"  # 源数据
result_path = 'output'
file_thres = 80
big_thres = 70
eval_windows = 25  # 设置统计单元大小
time_windows = 25
eval_big_windows = 25 * 60 * 30
eval_twenty_big_windows = 25 * 60 * 20
eval_ten_big_windows = 25 * 60 * 10
eval_five_big_windows = 25 * 60 * 5
fr1 = open("scale.txt", 'r')
string = fr1.read()
scale_datas = string.split('\n')
color = ['r','y','g','b','brown']
fig_turn = plt.figure(dpi=300)
ax = fig_turn.add_subplot(1, 1, 1)


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
        #长时间平均速度
        self.halfhour_id_dis = [[], [], [], [], []]
        self.halfhour_id_time = [0] * 5
        self.halfhour_v = []
        self.twenty_id_dis = [[], [], [], [], []]
        self.twenty_id_time = [0] * 5
        self.twenty_v = []
        self.ten_id_dis = [[], [], [], [], []]
        self.ten_id_time = [0] * 5
        self.ten_v = []
        self.five_id_dis = [[], [], [], [], []]
        self.five_id_time = [0] * 5
        self.five_v = []

        self.second_acc =[]
        self.fish_var =[]
        self.var_x =[]
        self.var_y=[]
        self.wh =[0,0],[0,0],[0,0],[0,0],[0,0]

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
        # 快转弯
        self.angle_faster = [0.0] * 5  # 角度
        self.swerves_faster = [] # 转弯次数
        self.swerve_px_faster = [0.0] * 5
        self.swerve_py_faster = [0.0] * 5
        self.swerve_angle1_faster = 0.0
        self.swerve_angle_faster = [0.0] * 5
        self.swerve_k_faster = [0] * 5
        self.k_faster = 0
        #
        ###摆尾
        # 头-身体-尾巴
        self.keypoint_mat = np.array([[0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0]])

        self.keypoint_angle_swing = np.array([[0,0,0],
                                      [0,0,0],
                                      [0,0,0],
                                      [0,0,0],
                                      [0,0,0]])#记录角度-摆尾标志位
        self.keypoint_beatandswing = np.array([[0,0],
                                              [0,0],
                                              [0,0],
                                              [0,0],
                                              [0,0]])

        self.avg_beat= []
        self.avg_swing = []

        self.small_thres = [0]*5
        self.count_frame = 0

        self.file_id_v =[[], [], [], [], []]
        self.file_id_i =[0] * 5

        self.scale = 0
        for line in scale_datas:
            q = [x for x in line.split(' ')]
            if q[0] == self.data_path:
                width = q[3]
                self.scale = 350 / int(width)
                break
        # self.small_thres[id] = 1 / self.scale - 0.6

    def float2int(date):
        return int(date)

    def execute(self):
        for num, file in enumerate(os.listdir(self.data_path)):
            if file.endswith(".mp4"):
                continue
            if int(file[-7:-4]) > file_thres:
                # print(num, file)
                continue
            print(num, file)
            self.data = np.loadtxt(self.data_path + "/{}".format(file), delimiter=',')
            if num == 0:
                self.vediolen = int(self.data[int(self.data.shape[0]) - 1, 0])
            start = time.time()
            self.execute_datas()
            end = time.time()
            print("inf-speed",end-start)
        self.second_acceleration()
        print("d")
        self.xls_writer()
        print('writing')

    '''
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
    '''



    def execute_datas(self):
        for i, line in enumerate(self.data):
            self.renewtlwh(i)
            if self.data[i, 0] in range(1, 6):  # 初始化前两帧 帧从2开始 warning
                continue

            self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离

            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])
            if frame != int(self.data[i - 1, 0]): #每一帧
                self.count_frame += 1
                self.tail_beat(frame, id, i)   ##摆尾统计
                self.fishing_var(frame, id, i) ##聚集程度
        #     self.plot_track(id)
        #     ax = plt.gca()  # 获取到当前坐标轴信息
        #     ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
        #     ax.invert_yaxis()  # 反转Y坐标轴
        # plt.show()



            self.second_record(frame, id, i)
            self.swerve(id, i)
            self.halfhour_record(frame, id, i)
            self.swerve_faster(id, i)
            self.twenty_record(frame, id, i)
            self.ten_record(frame, id, i)
            self.five_record(frame, id, i)

        print(self.keypoint_beatandswing)



    def renewtlwh(self, i):
        id = int(self.data[i, 1]) - 1
        self.px = self.x
        self.py =self.y
        self.x = self.data[i,12]
        self.y = self.data[i,13]
        self.keypoint_mat[id] = self.data[i,10:17]


    def angle_2vet(self,line):
        pointA, pointB, pointC = (line[0],line[1]),(line[2],line[3]),(line[4],line[5])
        pointA = np.array(pointA)
        pointB = np.array(pointB)
        pointC = np.array(pointC)
        dy, dx = pointB - pointA
        angel_head = math.atan2(dy, dx)
        dy, dx = pointB - pointC
        angel_tail = math.atan2(dy, dx)
        # if angel_head>math.pi:
        return math.degrees(math.pi - abs(angel_head) - abs(angel_tail))

    def get_distance_point2line(self, line):  ##  计算点到直线的距离
        """
        Args:
            point: [x0, y0]
            line: [x1, y1, x2, y2]
        """
        point = (line[4],line[5])##keypointtail
        line_point1, line_point2 = np.array(line[0:2]), np.array(line[2:4])
        vec1 = line_point1 - point
        vec2 = line_point2 - point
        m = np.linalg.norm(line_point1 - line_point2)
        if m == 0:
            print('error')
            return 0
        else:
            distance = np.abs(np.cross(vec1, vec2)) / m
        return distance

    def tail_beat(self,frame,id,i):
        for idx,line in enumerate(self.keypoint_mat):##更新一帧
            self.keypoint_angle_swing[idx][0] = self.angle_2vet(line)
            max = self.get_distance_point2line(line)

            if max > self.keypoint_angle_swing[idx][1]:
                self.keypoint_angle_swing[idx][1]=max

        for row,_ in enumerate(self.keypoint_angle_swing):##判断一帧
            if -1<=self.keypoint_angle_swing[row][0]<=1 and self.keypoint_angle_swing[row][2] == 1 :
                self.keypoint_beatandswing[row][0] +=1
                self.keypoint_beatandswing[row][1] += self.keypoint_angle_swing[row][1]
                self.keypoint_angle_swing[row][1] = 0
            if self.keypoint_angle_swing[row][0] >= 5 or self.keypoint_angle_swing[row][0] <= -5 :
                self.keypoint_angle_swing[row][2] = 1
            if -1<=self.keypoint_angle_swing[row][0]<=1 :
                self.keypoint_angle_swing[row][2] = 0

        if self.count_frame % eval_windows == 0:  ##1s内加入 ##累加
            self.avg_beat.append(np.mean(self.keypoint_beatandswing[:][0]))
            self.avg_swing.append(np.mean(self.keypoint_beatandswing[:][1]))




    def second_acceleration(self):
        for num in range(0,len(self.second_v)-1):
            self.second_acc.append(self.second_v[num] - self.second_v[num+1])

    def fishing_var(self,frame, id, i):
        if self.count_frame % eval_windows != 0: ##1s内加入
            for line in self.keypoint_mat:
                self.var_x.append(line[2] * self.scale)
                self.var_y.append(line[3] * self.scale)
        else:
            for line in self.keypoint_mat:
                self.var_x.append(line[2] * self.scale)
                self.var_y.append(line[3] * self.scale)
            self.fish_var.append(np.var(self.var_x)+np.var(self.var_y))
            self.var_x, self.var_y = [],[]



    # def swerve(self):
    def swerve(self,id,i):
        if self.count_frame % eval_windows == 0:
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
            elif dis>= self.small_thres[id]*10 and dis <= big_thres:
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

            if self.data[i,0] != self.data[i-1,0]:
                self.swerves.append(self.k)


    def swerve_faster(self,id,i):
        if self.count_frame %eval_windows !=0:
            if self.count_frame % 1 == 0:
                dis = ((self.x - self.swerve_px_faster[id]) ** 2 + (self.y - self.swerve_py_faster[id]) ** 2) ** 0.5
                if self.swerve_k_faster[id] == 0:
                    self.swerve_px_faster[id] = self.x
                    self.swerve_py_faster[id] = self.y
                    self.swerve_k_faster[id] = 1
                elif self.swerve_k_faster[id] == 1:
                    tan = math.atan2(self.y-self.swerve_py_faster[id],self.x-self.swerve_px_faster[id])
                    self.swerve_angle_faster[id] = math.degrees(tan)
                    self.swerve_px_faster[id] = self.x
                    self.swerve_py_faster[id] = self.y
                    self.swerve_k_faster[id] = 2
                elif dis>= self.small_thres[id]*10 and dis <= big_thres:
                    tan = math.atan2(self.y-self.swerve_py_faster[id], self.x-self.swerve_px_faster[id])
                    self.swerve_angle1_faster = math.degrees(tan)
                    self.angle_faster[id] += math.degrees(tan) - self.swerve_angle_faster[id]
                    self.swerve_angle_faster[id] = math.degrees(tan)
                    self.swerve_px_faster[id] = self.x
                    self.swerve_py_faster[id] = self.y

                if round(self.angle_faster[id],1) >=90.0 or round(self.angle_faster[id],1) <= -90.0:
                    self.k_faster +=1
                    self.angle_faster[id] = 0.0
                    # print("{} ok".format(self.swerves))

        else:
            if self.data[i,0] != self.data[i-1,0]:
                self.swerves_faster.append(self.k_faster)
            self.k_faster = 0
            self.angle_faster = [0.0] * 5



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
                    self.halfhour_v.append(x_dis / x_time *self.scale)  # 缺scale.txt
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

    def twenty_record(self,frame,id,i):
        if self.count_frame % eval_twenty_big_windows != 0:
            if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                self.twenty_id_dis[id].append(self.unit_dis)
                self.twenty_id_time[id] +=1
        else:
            if frame != int(self.data[i - 1, 0]):
                x_dis, x_time = 0, 0
                for x in range(0, 5):
                    x_dis += np.sum(self.twenty_id_dis[x])  ##mean
                    x_time += np.mean(self.twenty_id_time[x])
                if x_time == 0:
                    self.twenty_v.append(0)
                else:
                    self.twenty_v.append(x_dis / x_time *self.scale)  # 缺scale.txt
                # 重新初始化
                self.twenty_id_dis = [[], [], [], [], []]
                self.twenty_id_time = [0] * 5
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.twenty_id_dis[id].append(self.unit_dis)
                    self.twenty_id_time[id] += 1
                return
            else:
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.twenty_id_dis[id].append(self.unit_dis)
                    self.twenty_id_time[id] += 1

    def ten_record(self,frame,id,i):
        if self.count_frame % eval_ten_big_windows != 0:
            if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                self.ten_id_dis[id].append(self.unit_dis)
                self.ten_id_time[id] +=1
        else:
            if frame != int(self.data[i - 1, 0]):
                x_dis, x_time = 0, 0
                for x in range(0, 5):
                    x_dis += np.sum(self.ten_id_dis[x])  ##mean
                    x_time += np.mean(self.ten_id_time[x])
                if x_time == 0:
                    self.ten_v.append(0)
                else:
                    self.ten_v.append(x_dis / x_time *self.scale)  # 缺scale.txt
                # 重新初始化
                self.ten_id_dis = [[], [], [], [], []]
                self.ten_id_time = [0] * 5
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.ten_id_dis[id].append(self.unit_dis)
                    self.ten_id_time[id] += 1
                return
            else:
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.ten_id_dis[id].append(self.unit_dis)
                    self.ten_id_time[id] += 1

    def five_record(self,frame,id,i):
        if self.count_frame % eval_five_big_windows != 0:
            if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                self.five_id_dis[id].append(self.unit_dis)
                self.five_id_time[id] +=1
        else:
            if frame != int(self.data[i - 1, 0]):
                x_dis, x_time = 0, 0
                for x in range(0, 5):
                    x_dis += np.sum(self.five_id_dis[x])  ##mean
                    x_time += np.mean(self.five_id_time[x])
                if x_time == 0:
                    self.five_v.append(0)
                else:
                    self.five_v.append(x_dis / x_time *self.scale)  # 缺scale.txt
                # 重新初始化
                self.five_id_dis = [[], [], [], [], []]
                self.five_id_time = [0] * 5
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.five_id_dis[id].append(self.unit_dis)
                    self.five_id_time[id] += 1
                return
            else:
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.five_id_dis[id].append(self.unit_dis)
                    self.five_id_time[id] += 1


    def second_record(self, frame, id, i):
        if self.count_frame % eval_windows != 0:
            if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                self.second_id_dis[id].append(self.unit_dis)
                self.second_id_time[id] += 1
            elif self.unit_dis < self.small_thres[id]:
                self.second_id_rest_time[id] += 1
        else:
            if frame != int(self.data[i - 1, 0]):#避免更新单元重复计算
                x_dis, x_time, rest_time,k = 0, 0, 0,5
                for x in range(0, 5):
                    x_dis += np.sum(self.second_id_dis[x])  ##mean
                    x_time += np.mean(self.second_id_time[x])
                    rest_time += np.mean(self.second_id_rest_time[x])
                    if self.second_id_rest_time[x] == 0:
                        k -= 1

                if k != 0:
                    self.second_rest_time.append(rest_time/(time_windows*k))
                else:
                    self.second_rest_time.append(0)
                if x_time == 0:
                    self.second_v.append(0)
                else:
                    self.second_v.append(x_dis / x_time * self.scale)  # 缺scale.txt
                # 重新初始化
                self.second_id_dis = [[], [], [], [], []]
                self.second_id_time = [0] * 5
                self.second_id_rest_time=[0] * 5
                # 记录新单元
                if self.unit_dis >= self.small_thres[id] and self.unit_dis <= big_thres:
                    self.second_id_dis[id].append(self.unit_dis)
                    self.second_id_time[id] += 1
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


    def xls_writer(self):
        # global workbook
        workbook = xls.Workbook(result_path + "/track{}.xlsx".format(self.data_path).replace("keypointtracklet/",""))
        worksheet = workbook.add_worksheet("{}".format(self.data_path).replace("keypointtracklet/",""))
        #判断文件类型
        heading = ['平均速度/s', '静息时间/s', '平均速度/0.5h',
                   '平均速度/20mins', '平均速度/10mins', '平均速度/5mins',
                  '加速度/s', '聚集程度','转弯次数','快速转弯',"摆尾次数","摆尾幅度"]
        worksheet.write_row('A1', heading)  # 需要判断哪个单元开始

        worksheet.write_column('A2', self.second_v)  # 需要判断哪个单元开始
        worksheet.write_column('B2', self.second_rest_time)
        worksheet.write_column('C2', self.halfhour_v)
        worksheet.write_column('D2', self.twenty_v)
        worksheet.write_column('E2', self.ten_v)
        worksheet.write_column('F2', self.five_v)
        worksheet.write_column('G2', self.second_acc)
        worksheet.write_column('H2', self.fish_var)
        worksheet.write_column('I2', self.swerves)
        worksheet.write_column('J2', self.swerves_faster)
        worksheet.write_column('K2', self.avg_beat)
        worksheet.write_column('L2', self.avg_swing)
        workbook.close()



def process_eval(filename):
    # do sth here
    fun = Fun(filename, result_path)
    fun.execute()
    return None

def process_close(workbooook):
    # do sth here
    global workbook
    workbook = workbooook
    workbook.close()
    return None

def set_global(workbooook):
    global workbook
    workbook = workbooook


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
    # if not os.path.exists(result_path):
    #     os.mkdir(result_path)
    # workbook = xls.Workbook(result_path + "/track{}.xlsx".format(path_input))
    # fun = Fun(path_input, result_path)
    # fun.execute()
    # workbook.close()

    # 多文件多CPU
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    # for path_input in ["07","08","09"]:
    file = ["keypointtracklet/07","keypointtracklet/08","keypointtracklet/09","keypointtracklet/j08"]
    # file =["keytracktest/08","keytracktest/09"]
    # workbook = xls.Workbook(result_path + "/track.xlsx")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_eval, file)
        # work_list = [executor.submit(process_eval, i) for i in file]
        # ret = wait(fs=work_list, timeout=None, return_when=ALL_COMPLETED)
        # executor.submit(process_close, workbook)




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