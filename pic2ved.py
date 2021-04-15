import cv2
import glob
import os

img_path = '092'
video_path = 'video'

if not os.path.exists(video_path):
    os.mkdir(video_path)


class conv:
    def __init__(self,img_path,video_path ):
        super().__init__()
        self.h =0
        self.w = 0
        self.img_path = img_path
        self.txt_path = img_path
        self.video_path = video_path
        self.gt_path = video_path
    def img2video(self):
        i = 0

        for imgs in glob.glob(self.img_path + "/*.jpg"):
            frame = cv2.imread(imgs)
            if i == 0:
                self.h, self.w, _ = frame.shape  # 获取一帧图像的宽高信息
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(self.video_path + '/' + self.img_path + '.avi', fourcc, 25.0, (self.w, self.h), True)
                i = 1
            out.write(frame)  # 对视频文件写入一帧
        # out.release()  # 释放视频流


    def txt2gt(self):
        filenames = glob.glob(self.txt_path + "/*.txt")
        f = open(self.gt_path + '/' + self.txt_path + '.txt', 'w')
        for filename in filenames:
            filepath = filename
            r =open(filepath)
            line = r.readline()
            while(line):
                line = r.readline()
                if line == '':
                    break
                line = line.split(' ')
                print(line)
                line[0] = int(line[0]) + 1
                line[1] = float(line[1])*self.w
                line[3] = float(line[3])*self.w
                line[2] = float(line[2])*self.h
                line[4] = float(line[4].replace('\n', '')) * self.h
                frame =int(os.path.basename(filename).split('.')[0])
                str = '{},{},{:.0f},{:.0f},{:.0f},{:.0f},-1,-1,-1-1\n'.format(
                    frame, line[0], line[1], line[2], line[3], line[4]
                )
                f.writelines(str)
        f.close()

if __name__ == '__main__':
    c = conv(img_path, video_path)
    c.img2video()
    c.txt2gt()
