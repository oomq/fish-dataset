import numpy as np
import os
import xlsxwriter as xls
import math
import matplotlib.pyplot as plt
import time
import xlrd
from concurrent.futures import wait, ALL_COMPLETED
import concurrent.futures

from tqdm import tqdm
import utils as u


path_input = "keypointtracklet/08"  # 源数据8
path_input_all = "keypointtracklet/"
result_path = 'output-test'
file_thres = 120
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
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        self.distance = [[], [], [], [], []]
        self.time = [0] * 5
        # self.tlwh  = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.vediolen = 0
        self.px = 0
        self.py = 0
        self.x = 0
        self.y = 0
        self.unit_dis = 0

        self.tracknum = 0
        self.kp_box_errorthres = 20
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
        self.swerves = [] # 转弯次数
        self.turn_times = 0
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
                                      [0,0,0]])#记录角度-最大角度-摆尾标志位

        self.beat_temp = 0
        self.swing_temp = 0
        self.avg_beat= []
        self.avg_swing = []

        self.small_thres = [4]*5
        self.count_frame = 0

        self.file_id_v =[[], [], [], [], []]
        self.file_id_i =[0] * 5

        self.scale = 0
        for line in scale_datas:
            q = [x for x in line.split(' ')]
            if q[0] == self.data_path.replace(path_input_all,""):
                width = q[3]
                self.scale = 350 / int(width)
                break
        # self.small_thres[id] = 1 / self.scale - 0.6

    def xls_writer(self):
        # global workbook
        workbook = xls.Workbook(result_path + "/track{}.xlsx".format(self.data_path).replace(path_input_all,""))
        worksheet = workbook.add_worksheet("{}".format(self.data_path).replace(path_input_all,""))
        #判断文件类型
        heading = ['平均速度/s', '静息时间/s', '平均速度/0.5h',
                   '平均速度/20mins', '平均速度/10mins', '平均速度/5mins',
                  '加速度/s', '聚集程度','转弯次数','快速转弯',"摆尾次数","摆尾幅度"]
        worksheet.write_row('A1', heading)  # 需要判断哪个单元开始

        worksheet.write_column('A2', self.second_v)  # 需要判断哪个单元开始
        worksheet.write_column('B2', self.second_rest_time)
        # worksheet.write_column('C2', self.halfhour_v)
        # worksheet.write_column('D2', self.twenty_v)
        # worksheet.write_column('E2', self.ten_v)
        # worksheet.write_column('F2', self.five_v)
        worksheet.write_column('G2', self.second_acc)
        worksheet.write_column('H2', self.fish_var)
        worksheet.write_column('I2', self.swerves)
        # worksheet.write_column('J2', self.swerves_faster)
        worksheet.write_column('K2', self.avg_beat)
        worksheet.write_column('L2', self.avg_swing)
        workbook.close()

    def execute(self):
        for num, file in tqdm(enumerate(os.listdir(self.data_path))):
            if file.endswith(".mp4") or self.count_frame >1900000:
                continue
            # if int(file[-6:-4]) <32:
            #     continue
            print(num, file)
            self.data = np.loadtxt(self.data_path + "/{}".format(file), delimiter=',')
            if num == 0:
                self.vediolen = int(self.data[int(self.data.shape[0]) - 1, 0])
            self.tracknum = max(int(self.data[10000, 8]),int(self.data[10000, 7]))
            self.keypointxymat = np.array([[0 for i in range(2)]for i in range(self.tracknum)])
            self.tlwh =np.array([[0 for i in range(4)]for i in range(self.tracknum)])
            self.turn_times_angle = np.array([[0 for i in range(2)] for i in range(self.tracknum)])
            self.angle = np.array([[0 for i in range(1)]for i in range(self.tracknum)])
            self.keypoint_beatandswing = np.array([[0 for i in range(2)] for i in range(self.tracknum)])

            start = time.time()
            self.execute_datas()
            end = time.time()
            print("inf-speed",end-start)
        # self.second_acceleration()
        print("d")
        self.xls_writer()
        print('writing')


    def renewtlwh(self, i):
        id = int(self.data[i, 1]) - 1
        self.keypointxymat[id][0] = self.data[i,12]
        self.keypointxymat[id][1] = self.data[i,13]
        self.keypoint_mat[id] = self.data[i,10:17]
        self.tlwh[id][0] = self.data[i, 2]  # t
        self.tlwh[id][1] = self.data[i, 3]  # l
        self.tlwh[id][2] = self.data[i, 4]  # w
        self.tlwh[id][3] = self.data[i, 5]  # h





    def second_record(self, frame, id, i,):
        for x in range(0,self.tracknum):
            boxdis_id = u.xydis(self.boxdis[x])
            kpdis_id = u.xydis(self.keypointdis[x])
            if boxdis_id <= self.small_thres[x] or kpdis_id<=self.small_thres[x]:
                self.second_id_dis[x].append(0)
                self.second_id_rest_time[x] += 1
            elif math.fabs(kpdis_id-boxdis_id) < self.kp_box_errorthres:
                self.second_id_dis[x].append(kpdis_id)
                self.second_id_time[x] += 1
            else:
                self.second_id_dis[x].append(boxdis_id)
                self.second_id_time[x] += 1


        x_dis = np.mean(self.second_id_dis)  ##sum->mean
        x_time = np.mean(self.second_id_time)
        rest_time = np.mean(self.second_id_rest_time)

        self.second_rest_time.append(rest_time)
        if x_time == 0:
            self.second_v.append(0)
        else:
            self.second_v.append(x_dis / x_time * self.scale)  # 缺scale.txt
        # 重新初始化
        self.second_id_dis = [[]for _ in range(self.tracknum)]
        self.second_id_time = np.array([[0]for _ in range(self.tracknum)])
        self.second_id_rest_time= np.array([[0]for _ in range(self.tracknum)])

    def tail_beat(self, frame, id, i):
        for idx, line in enumerate(self.keypoint_mat):  ##更新一帧
            self.keypoint_angle_swing[idx][0] = u.angle_2vet(line)
            max = u.get_distance_point2line(line)

            if max > self.keypoint_angle_swing[idx][1]:
                self.keypoint_angle_swing[idx][1] = max

        for row, _ in enumerate(self.keypoint_angle_swing):  ##判断一帧
            if -1 <= self.keypoint_angle_swing[row][0] <= 1 and (self.keypoint_angle_swing[row][2] == 1 or self.keypoint_angle_swing[row][2] == -1):
                self.keypoint_beatandswing[row][0] += 1
                self.keypoint_beatandswing[row][1] += self.keypoint_angle_swing[row][1]
                self.keypoint_angle_swing[row][2] = 0
            elif self.keypoint_angle_swing[row][0] >= 5:
                self.keypoint_angle_swing[row][2] = 1
            elif self.keypoint_angle_swing[row][0] <= -5:
                self.keypoint_angle_swing[row][2] = -1
            elif self.keypoint_angle_swing[row][0]>1 and self.keypoint_angle_swing[row][2] == -1:
                self.keypoint_beatandswing[row][0] += 1
                self.keypoint_beatandswing[row][1] += self.keypoint_angle_swing[row][1]
                self.keypoint_angle_swing[row][2] = 0
            elif self.keypoint_angle_swing[row][0]<-1 and self.keypoint_angle_swing[row][2] == 1:
                self.keypoint_beatandswing[row][0] += 1
                self.keypoint_beatandswing[row][1] += self.keypoint_angle_swing[row][1]
                self.keypoint_angle_swing[row][2] = 0


        # for row, _ in enumerate(self.keypoint_angle_swing):  ##判断一帧
        #     if -1 <= self.keypoint_angle_swing[row][0] <= 1 and self.keypoint_angle_swing[row][2] == 1:
        #         self.keypoint_beatandswing[row][0] += 1
        #         self.keypoint_beatandswing[row][1] += self.keypoint_angle_swing[row][1]
        #         self.keypoint_angle_swing[row][1] = 0
        #     if self.keypoint_angle_swing[row][0] >= 5 or self.keypoint_angle_swing[row][0] <= -5:
        #         self.keypoint_angle_swing[row][2] = 1
        #     if -1 <= self.keypoint_angle_swing[row][0] <= 1:
        #         self.keypoint_angle_swing[row][2] = 0

        if self.count_frame % eval_windows == 0:  ##1s内加入 ##累加
            self.beat_temp += np.mean(self.keypoint_beatandswing[:, 0])
            self.avg_beat.append(self.beat_temp)
            self.swing_temp += np.mean(self.keypoint_beatandswing[:, 1] * self.scale)
            self.avg_swing.append(self.swing_temp)
            self.keypoint_beatandswing = np.array([[0 for i in range(2)] for i in range(self.tracknum)])

    def second_acceleration(self): ##a
        for num in range(0,len(self.second_v)-1):
            self.second_acc.append(self.second_v[num] - self.second_v[num+1])

    def fishing_var(self,frame, id, i): ##var each/s
        ##keypoint
        # if self.count_frame % eval_windows != 0: ##1s内加入
        #     for line in self.keypoint_mat:
        #         self.var_x.append(line[2] * self.scale)
        #         self.var_y.append(line[3] * self.scale)
        # else:
        #     for line in self.keypoint_mat:
        #         self.var_x.append(line[2] * self.scale)
        #         self.var_y.append(line[3] * self.scale)
        #     self.fish_var.append(np.var(self.var_x)+np.var(self.var_y))
        #     self.var_x, self.var_y = [],[]
        ##box
        if self.count_frame % eval_windows != 0: ##1s内加入
            for line in self.boxcxcy:
                self.var_x.append(line[0] * self.scale)
                self.var_y.append(line[1] * self.scale)
        else:
            for line in self.boxcxcy:
                self.var_x.append(line[0] * self.scale)
                self.var_y.append(line[1] * self.scale)
            self.fish_var.append(np.var(self.var_x) + np.var(self.var_y))
            self.var_x, self.var_y = [], []

    def swerve(self,frame,id,i):

        self.pangle = self.angle.copy()
        for x in range(self.tracknum):
            self.angle[x] = math.degrees(u.angle(self.keypoint_mat[x][0:2],self.keypoint_mat[x][2:4]))
            self.turn_times_angle[x][1] += self.angle[x] - self.pangle[x]
            if self.turn_times_angle[x][1] >=90 or self.turn_times_angle[x][1] <=-90:
                self.turn_times_angle[x][0] +=1
                self.turn_times_angle[x][1] =0




    def execute_datas(self):
        self.boxcxcy = self.keypointxy = np.array([[0 for i in range(2)]for i in range(self.tracknum)])
        for i, line in enumerate(self.data):
            self.pboxcxcy = self.boxcxcy
            self.keypointpxy = self.keypointxy
            self.renewtlwh(i)
            if self.data[i, 0] in range(0, 20):  # 初始化前两帧 帧从2开始 warning
                self.keypointxy = self.keypointxymat
                self.boxcxcy = u.tlwh2xy(self.tlwh)
                continue

            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])

            if frame != int(self.data[i - 1, 0]): #每一帧
                self.tail_beat(frame, id, i)  ##摆尾统计
                self.swerve(frame, id, i)  ##转弯统计
                self.count_frame += 1
                if self.count_frame % eval_windows == 0:#每一秒
                    self.keypointxy = self.keypointxymat.copy()
                    self.boxcxcy = u.tlwh2xy(self.tlwh)
                    self.boxdis = self.boxcxcy - self.pboxcxcy
                    self.keypointdis = self.keypointxy - self.keypointpxy
                    self.second_record(frame, id, i)##速度统计
                    self.fishing_var(frame, id, i) ##聚集程度
                    self.turn_times += np.mean(self.turn_times_angle[:, 0])
                    self.swerves.append(self.turn_times)##转弯求和
                    self.turn_times_angle[:,0] =0

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
    #多文件单cpu
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
    first = time.time()
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    # for path_input in ["07","08","09"]:
    # file = ["keypointtracklet/07","keypointtracklet/08","keypointtracklet/09","keypointtracklet/j08"]
    # file =["keytracktest/08","keytracktest/09"]
    # workbook = xls.Workbook(result_path + "/track.xlsx")
    file = [(path_input_all + t) for t in os.listdir(path_input_all)]
    # name = [t.replace("track","").replace(".xlsx","") for t in os.listdir(result_path)]
    # file = [(path_input_all + t) for t in os.listdir(path_input_all) if not t in name]

    with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
        executor.map(process_eval, file)
        # work_list = [executor.submit(process_eval, i) for i in file]
        # ret = wait(fs=work_list, timeout=None, return_when=ALL_COMPLETED)
        # executor.submit(process_close, workbook)
    end = time.time()
    print("all-time", end-first)

