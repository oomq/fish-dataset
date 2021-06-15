import numpy as np

seq = '082'
root = './video/{}.txt'.format(seq)  #结果路径
occ_txt = './occ/occ{}.txt'.format(seq)
output_txt = './occ/{}.txt'.format(seq)

class occlusion(object):
    def __init__(self, input_path, data_path,result_path):
        super().__init__()
        self.input_path = input_path
        self.data_path = data_path
        self.result_path = result_path
        self.string = ''
        self.datas = []
        self.occ_datas =[]
        self.input = []
        self.output = []
        self.num = []
        self.occlusions_length = []
        self.occlusions_count =[]

        self.stats_dict = {"OL": {}, "FBO": {}, "OC":{}}

    def execute_str(self,line):
        msgs = line.split(';')
        for i, msg in enumerate(msgs):
            if i ==0:
                id1 = msgs[i].split(',')[0]
                id2 = msgs[i].split(',')[1]
                print(id1,id2)
            elif i ==1:
                frame1=  msgs[i].split(',')[0]
                frame2 = msgs[i].split(',')[1]
                frame2 = frame2.replace("\n", "")

        for ind, data in enumerate(self.datas):
            mata = self.datas[ind].split(',')  # input
            if mata[0] == '' or frame2 == '':
                break
            if (int(mata[0]) >= int(frame1)) and (int(mata[0]) < int(frame2) + 1) \
                    and (mata[1] == id1 or mata[1] == id2) and mata[-1] == '-1-1':
                mata[-1] = '1'
                self.output.append(','.join(mata))  # 写入
        self.occlusions_length = len(self.output)
        self.output = list(np.unique(self.output))


    def execute(self):
        fr1 = open(self.data_path, 'r')
        fr2 = open(self.input_path, 'r')
        self.string = fr1.read()
        self. datas = self.string.split('\n')  # input—data分成每行数据为一个个list索引
        print('g')
        line = fr2.readline()  # 读取a**.txt的第一行
        while line:
            self.execute_str(line)  # 处理数据（num为行数索引也代表真实ID）
            line = fr2.readline()  # 读取下一行
        self.string = '\n'.join(self.output)
        with open(self.result_path,'w') as fw:#写入txt
            fw.write(self.string)
        fr1.close()
        fr2.close()

    def eval_OL(self,line):
        msgs = line.split(';')
        frame1 = int(msgs[2].split(',')[0])
        frame2 = msgs[2].split(',')[1]
        frame2 = int(frame2.replace("\n", ""))
        self.occlusions_length.append(frame2-frame1+1)
        # FBO






    def eval_full(self):
        occ_txt = open(self.occ_txt, 'r')
        occ_string = occ_txt.read()
        self.occ_datas = occ_string.split('\n')

        for i, line in enumerate(self.occ_datas):
            msgs = line.split(';')
            frame1 = int(msgs[i].split(',')[0])
            frame2 = msgs[i].split(',')[1]
            frame2 = int(frame2.replace("\n", ""))
            self.occlusions_length.append(frame2 - frame1 + 1)
            






if __name__ == '__main__':
    fun = occlusion(occ_txt,root,output_txt)
    fun.execute()
    fun.eval()