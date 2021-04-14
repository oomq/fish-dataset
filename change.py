import re

path_a = './原视频和结果/a112.txt'
path_b = './output/112.txt'
path_c = './原视频和结果/112.txt'


class Fun(object):
    def __init__(self, input_path, data_path,result_path):
        super().__init__()
        self.input_path = input_path
        self.data_path = data_path
        self.result_path = result_path
        self.string = ''
        self.datas = []
        self.flag = []
        self.a = 0

    def execute(self):
        fr1 = open(self.data_path, 'r')
        fr2 = open(self.input_path, 'r')
        self.string = fr1.read()
        self.datas = self.string.split('\n')
        for f in range(len(self.datas)):
            self.flag.append(0)

        # print(self.string)
        line = fr2.readline()
        while line:
            self.execute_str(line)
            self.string = '\n'.join(self.datas)
            with open(self.result_path,'w') as fw:
                fw.write(self.string)
            line = fr2.readline()

        # with open(self.data_path, 'w') as fw:
        #     fw.write(self.string)
        fr1.close()
        fr2.close()
    # 处理一行
    def execute_str(self, s):
        f_id = s.split(' ')[0]
        msgs = s.split(' ')[1].split(';')
        # 处理一组
        for i,msg in enumerate(msgs):
            frame, id = msgs[i].split(',')
            id = id.replace('\n', '').replace('\r', '')
            if i+1 >= len(msgs):
                frame2 = self.datas[len(self.datas)-1].split(",")[0]
            else:
                frame2 = msgs[i + 1].split(",")[0]
            # ss = str(frame) + ',' + str(id)
            # print(type(frame))
            print(type(int(frame)))
            for ind, data in enumerate(self.datas):
                mata = self.datas[ind].split(',')
                #print(frame)
                if (int(mata[0]) >= int(frame)) and (int(mata[0]) < int(frame2) and self.flag[ind] == 0):
                    if mata[1] == id:
                        mata[1] = f_id
                        self.flag[ind] = 1
                        self.datas[ind] = ','.join(mata)
                #print(frame2)
                #print(mata[0], int(frame2))
                # if int(frame2) == 693:
                #     self.a =1
                if int(mata[0]) >= int(frame2):
                    break




                # if re.search('^' + ss, data):
                #     index = ind
                #     index2 = 0
                #     for _ in range(-5, 5):
                #         ind_ = index + _ if index - _ >= 0 else 0
                #         ind_ = ind_ if ind_ < len(self.datas) else len(self.datas) - 1
                #         ss_ = '^' + str(frame) + ',' + str(f_id)
                #         # print(ss_)
                #         if re.search(ss_, self.datas[ind_]):
                #             index2 = ind_
                #             break
                #     # print(data)
                #     # print(self.datas[index2])
                #     mata = self.datas[index].split(',')
                #     mata[1] = f_id
                #     self.datas[index] = ','.join(mata)
                #     mata2 = self.datas[index2].split(',')
                #     mata2[1] = id
                #     self.datas[index2] = ','.join(mata2)
                #     # print(self.datas[index])
                #     # print(self.datas[index2])
                #     # print('---------------------')
                #     break


if __name__ == '__main__':
    fun = Fun(path_a, path_b,path_c)
    fun.execute()
