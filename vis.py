import numpy as np
import os

path_input = "02"  # 源数据
result_path = 'output'
file_thres = 1000
small_thres =3
big_thres = 27
eval_windows =25 #设置统计单元大小
# fr1 = open("scale.txt", 'r')
# string = fr1.read()
# datas = string.split('\n')
# scale = 0
# for line in datas:
#     q = [x for x in line.split(' ')]
#     if q[0] == data_path:
#         width = q[3]
#         scale = 350 / int(width)
#         break


class Fun(object):
    def __init__(self, data_path, result_path):
        super().__init__()
        self.data_path = data_path
        self.result_path = result_path
        self.distance = [[],[],[],[],[]]
        self.time = [0]*5
        self.tlwh = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.vediolen = 0
        self.px = 0
        self.py = 0
        self.x = 0
        self.y = 0
        self.unit_dis = 0
        self.each_file_distance = []
        self.each_file_time = []
        self.second_dis = [[],[],[],[],[]]
        self.second_id_dis =[[],[],[],[],[]]
        self.second_id_time= [0]*5
        self.second_v =[]


    def float2int(date):
        return int(date)

    def execute(self):
        for num, file in enumerate(os.listdir(self.data_path)):
            if int(file.replace(".txt", "").replace(self.data_path + "-", "")) > file_thres:
                # print(num, file)
                continue
            self.data = np.loadtxt(self.data_path + "/{}".format(file), delimiter=',')
            if num == 0:
                self.vediolen = int(self.data[int(self.data.shape[0]) - 1, 0])
            self.execute_datas()
            print(file)

        print('done')


    def renewtlwh(self,i):
        id= int(self.data[i, 1])-1
        if np.any(np.array(self.tlwh) ==0):
            self.tlwh[id][0] = self.data[i, 2]  # t
            self.tlwh[id][1] = self.data[i, 3]  # l
            self.tlwh[id][2] = self.data[i, 4]  # w
            self.tlwh[id][3] = self.data[i, 5]  # h
            return

        self.px = self.tlwh[id][0] + self.tlwh[id][2]/2
        self.py = self.tlwh[id][1] + self.tlwh[id][3]/2
        self.tlwh[id][0] = self.data[i, 2]#t
        self.tlwh[id][1] = self.data[i, 3]#l
        self.tlwh[id][2] = self.data[i, 4]#w
        self.tlwh[id][3] = self.data[i, 5]#h
        self.x = self.tlwh[id][0] + self.tlwh[id][2]/2
        self.y = self.tlwh[id][1] + self.tlwh[id][3]/2


    def execute_datas(self):
        frame_flag =0
        for i,line in enumerate(self.data):
            self.renewtlwh(i)
            if self.data[i, 0] in range(1,6):#初始化前两帧 帧从2开始 warning
                continue

            self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离
            id = int(self.data[i, 1]) - 1
            frame = int(self.data[i, 0])
            if frame % eval_windows != 0 :
                if self.unit_dis >= small_thres and self.unit_dis <= big_thres:
                    self.second_id_dis[id].append(self.unit_dis)
                    self.second_id_time[id]+=1
            else:
                if frame == int(self.data[i-1, 0]):
                    continue
                x_dis,x_time =0,0
                for x in range(0,5):
                    x_dis += np.sum(self.second_id_dis[x])  ##mean
                    x_time += np.mean(self.second_id_time[x])
                # if x_dis ==0:
                #     print(x_time)
                self.second_v.append(x_dis/x_time)   #缺scale.txt
                #重新初始化
                self.second_id_dis = [[], [], [], [], []]
                self.second_id_time = [0] * 5
                #记录新单元
                if self.unit_dis >= small_thres and self.unit_dis <= big_thres:
                    self.second_id_dis[id].append(self.unit_dis)
                    self.second_id_time[id]+=1
                #单文件
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


        #单文件
        # x_dis = 0
        # for x in range(0,5):
        #     x_dis+=np.sum(self.distance[x])
        # self.each_file_distance.append(x_dis)



if __name__ == '__main__':
    fun = Fun(path_input, result_path)
    fun.execute()


#分区间统计
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
