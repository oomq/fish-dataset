import numpy as np
import os

path_input = "02"  # 源数据
result_path = 'output'
file_thres = 2
small_thres =3
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
        for i,line in enumerate(self.data):
            self.renewtlwh(i)
            if self.data[i, 0] in range(1,3):
                continue
            self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离
            if self.unit_dis > small_thres:
                id = int(self.data[i, 1]) - 1
                self.distance[id].append(self.unit_dis)
                self.time[id] += 1



if __name__ == '__main__':
    fun = Fun( path_input,result_path)
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
















