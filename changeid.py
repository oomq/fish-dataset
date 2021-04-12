import re

path_a = 'a.txt'
path_b = 'results.txt'


class Fun(object):
    def __init__(self, input_path, data_path):
        super().__init__()
        self.input_path = input_path
        self.data_path = data_path
        self.string = ''
        self.datas = []

    def execute(self):
        fr1 = open(self.data_path, 'r')
        fr2 = open(self.input_path, 'r')
        self.string = fr1.read()
        self.datas = self.string.split('\n')
        # print(self.string)
        line = fr2.readline()
        while line:
            self.execute_str(line)
            line = fr2.readline()
        self.string = '\n'.join(self.datas)
        with open(self.data_path, 'w') as fw:
            fw.write(self.string)
        fr1.close()
        fr2.close()

    def execute_str(self, s):
        f_id = s.split(' ')[0]
        msgs = s.split(' ')[1].split(';')
        for msg in msgs:
            frame, id = msg.split(',')
            ss = str(frame) + ',' + str(id)
            for ind, data in enumerate(self.datas):
                if re.search('^' + ss, data):
                    index = ind
                    index2 = 0
                    for _ in range(-5, 5):
                        ind_ = index + _ if index - _ >= 0 else 0
                        ind_ = ind_ if ind_ < len(self.datas) else len(self.datas) - 1
                        ss_ = '^' + str(frame) + ',' + str(f_id)
                        # print(ss_)
                        if re.search(ss_, self.datas[ind_]):
                            index2 = ind_
                            break
                    # print(data)
                    # print(self.datas[index2])
                    mata = self.datas[index].split(',')
                    mata[1] = f_id
                    self.datas[index] = ','.join(mata)
                    mata2 = self.datas[index2].split(',')
                    mata2[1] = id
                    self.datas[index2] = ','.join(mata2)
                    # print(self.datas[index])
                    # print(self.datas[index2])
                    # print('---------------------')
                    break


if __name__ == '__main__':
    fun = Fun(path_a, path_b)
    fun.execute()
