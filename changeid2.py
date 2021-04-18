import re

path_fix = '原视频和结果/a091.txt'#修改文本
path_input = 'output/091.txt'#源数据
path_output = '原视频和结果/091.txt'#输出

class Fun(object):
    def __init__(self, input_path, data_path,result_path):
        super().__init__()
        self.input_path = input_path
        self.data_path = data_path
        self.result_path = result_path
        self.string = ''
        self.datas = []
        self.input = []
        self.output = []
        self.num = []

    def function(date):
        return int(date)

    def execute(self):
        fr1 = open(self.data_path, 'r')
        fr2 = open(self.input_path, 'r')
        self.string = fr1.read()
        self.datas = self.string.split('\n')
        index = 0
        num = 1
        line = fr2.readline()
        while line:
            self.execute_str(line,num)
            num += 1
            line = fr2.readline()

        #print(self.input[3691])
        #print(len(self.input))
        #排序

        self.output.sort(key = lambda x: (int(x.split(',')[0]), int(x.split(',')[1])))

        self.string = '\n'.join(self.output)
        with open(self.result_path,'w') as fw:
            fw.write(self.string)
        fr1.close()
        fr2.close()

    # 处理一行
    def execute_str(self, s,num):
        # print(num)
        msgs = s.split(';')
        # 处理一组
        for i,msg in enumerate(msgs):
            frame = msgs[i].split(',')[0]

            if i == (len(msgs)-1):
                id = msgs[i].split(',')[1] #a.txt changeid
                id = id.replace("\n", "")
            else :
                id = msgs[i].split(',')[1]
                next_id  = msgs[i+1].split(',')[1]

            if i+1 >= len(msgs):
                frame2 = self.datas[len(self.datas)-2].split(",")[0]
            else:
                frame2 = msgs[i + 1].split(",")[0] #a.txt

            for ind, data in enumerate(self.datas):
                mata = self.datas[ind].split(',')    #input
                if mata[0] == '' or frame2 == '':
                    break
                if (int(mata[0]) >= int(frame)) and (int(mata[0]) < int(frame2)-1) and mata[1] == id:
                    mata[1] = str(num)
                    self.output.append(','.join(mata))


if __name__ == '__main__':
    fun = Fun(path_fix, path_input,path_output)
    fun.execute()
