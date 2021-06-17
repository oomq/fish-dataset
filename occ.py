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
        self.video_length =0
        self.occlusions_frame = []
        self.occlusions_length = []
        self.occlusions_count = []
        self.occlusions_between = []
        self.occlusions_intersection =[]

        self.stats_dict = {"OL": {}, "FBO": {}, "OC":{}}

    def execute_str(self,line):
        msgs = line.split(';')
        for i, msg in enumerate(msgs):
            if i ==0:
                id1 = msgs[i].split(',')[0]
                id2 = msgs[i].split(',')[1]

            elif i ==1:
                frame1=  msgs[i].split(',')[0]
                frame2 = msgs[i].split(',')[1]
                frame2 = frame2.replace("\n", "")

        for ind, data in enumerate(self.datas):

            mata = self.datas[ind].split(',')  # input
            if mata[0] == '' or frame2 == '':
                break
            if int(mata[0]) > self.video_length:
                self.video_length = int(mata[0])

            if (int(mata[0]) >= int(frame1)) and (int(mata[0]) < int(frame2) + 1) \
                    and (mata[1] == id1 or mata[1] == id2) and mata[-1] == '-1-1':
                mata[-1] = '1'
                self.output.append(','.join(mata))  # 写入
        self.occlusions_count = len(self.output)
        self.output = list(np.unique(self.output))


    def execute(self):
        fr1 = open(self.data_path, 'r')
        fr2 = open(self.input_path, 'r')
        self.string = fr1.read()
        self. datas = self.string.split('\n')  # input—data分成每行数据为一个个list索引

        line = fr2.readline()  # 读取a**.txt的第一行
        while line:
            self.execute_str(line)  # 处理数据（num为行数索引也代表真实ID）
            line = fr2.readline()  # 读取下一行
        self.string = '\n'.join(self.output)
        with open(self.result_path,'w') as fw:#写入txt
            fw.write(self.string)
        fr1.close()
        fr2.close()

    def getIntersection(self,bbox,candidates):
        bbox_tl, bbox_br = bbox[:2],bbox[:2]+bbox[2:]
        candidates_tl = candidates[:, :2]
        candidates_br = candidates[:, :2] + candidates[:, 2:]

        tl = np.c_[np.maximum(bbox_tl[0], candidates_tl[:, 0])[:, np.newaxis],
                   np.maximum(bbox_tl[1], candidates_tl[:, 1])[:, np.newaxis]]
        br = np.c_[np.minimum(bbox_br[0], candidates_br[:, 0])[:, np.newaxis],
                   np.minimum(bbox_br[1], candidates_br[:, 1])[:, np.newaxis]]
        wh = np.maximum(0., br - tl)

        area_intersection = wh.prod(axis=1)

        return area_intersection

    def getOcclusionIntersection(self,boxes):
        cost_matrix = np.zeros(len(boxes), len(boxes))
        for row, box in enumerate(boxes):
            cost_matrix[row, :] = self.getIntersection(box, boxes)
        cost_matrix = np.triu(cost_matrix, 1)

        return cost_matrix

    def eval_IBO(self):
        f1 = open(self.result_path, 'r')
        string= f1.read()
        output = string.split('\n')
        boxes = []
        frame_flag = output[0][0]

        for ind, line in enumerate(output):
            if output[ind][0] == frame_flag:
                boxes.append(line)
            else:
                self.occlusions_intersection.append(self.getOcclusionIntersection(boxes).sum())




    def eval_full(self):
        occ_txt = open(self.input_path, 'r')
        occ_string = occ_txt.read()
        self.occ_datas = occ_string.split('\n')

        for id in range(1,6):
            self.occlusions_frame = []
            num = 0
            for i, line in enumerate(self.occ_datas):
                msgs = line.split(';')
                frame1 = int(msgs[1].split(',')[0])
                frame2 = msgs[1].split(',')[1]
                frame2 = int(frame2.replace("\n", ""))
                id1 = int(msgs[0].split(',')[0])
                id2 = int(msgs[0].split(',')[1])
                # OL
                ##add num[] to mean the occ_length
                if id == id1 or id == id2:
                    for num_frame in range(frame1, frame2+1):
                        num += 1
                        self.occlusions_frame.append(num_frame)
            self.occlusions_frame = np.unique(self.occlusions_frame)
            # self.occlusions_length.append(len(self.occlusions_frame)/ num )
            self.occlusions_length.append(len(self.occlusions_frame))
            self.occlusions_between.append(self.video_length - len(self.occlusions_frame))

                # if i != len(self.occ_datas) :
                #     frame_nxt = int(msgs[i+1].split(',')[0])
                # else:
                #     frame_nxt = len(self.string)

                #OL
                # self.occlusions_length.append(frame2 - frame1 + 1)


                #FBO

            # self.occlusions_between.append()


if __name__ == '__main__':
    fun = occlusion(occ_txt,root,output_txt)
    fun.execute()
    fun.eval_full()
    fun.eval_IBO()
    print('OL',np.mean(fun.occlusions_length))
    print('OC',fun.occlusions_count)
    print('FBO', np.mean(fun.occlusions_between))
    # print('FBO',np.mean(fun.occlusions_between))
