import numpy as np
import os

path_input = "02"  # 源数据
result_path = 'output'
file_thres = 2
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
        self.distance = []*5
        self.time = []*5
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


    def renewtlwh(self,i):
        id= int(self.data[i, 1])-1
        if np.any(self.tlwh!=0):
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
            self.unit_dis = ((self.x - self.px) ** 2 + (self.y - self.py) ** 2) ** 0.5  # 计算一个两帧间距离

            id = int(self.data[i, 1]) - 1
            self.distance[id].append(self.unit_dis)
            self.time[id] += 1


if __name__ == '__main__':
    fun = Fun( path_input,result_path)
    fun.execute()
















