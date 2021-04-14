import cv2
import tqdm
import os
import pandas as pd

video_path = './原视频和结果/112.mp4'
result_path = './原视频和结果/112.txt'
img_path = './img'
label_img = './label'

if not os.path.exists(img_path):
    os.mkdir(img_path)

cap = cv2.VideoCapture(video_path)

def tlwh2xywh(t,l,w,h):#转成中心点
    return t+w/2, l+h/2, w, h



def txt_to_df(txt_path):
    f = open(txt_path)
    nearby_list = []
    for row in f.readlines():
        nearby_list.append(row)

    df_nearby = pd.DataFrame()
    id_list = []
    x_list = []
    y_list = []
    w_list = []
    h_list = []
    score_list = []
    defect_list = []
    time_list = []
    for ele_nearby in nearby_list:
        ele_nearby = ele_nearby.split(',')
        time_list.append(int(ele_nearby[0]))
        id_list.append(int(ele_nearby[1]))
        x_list.append(round(float(ele_nearby[2])))
        y_list.append(round(float(ele_nearby[3])))
        w_list.append(round(float(ele_nearby[4])))
        h_list.append(round(float(ele_nearby[5])))

    df_nearby['frame'] = time_list
    df_nearby['id'] = id_list
    df_nearby['x'] = x_list
    df_nearby['y'] = y_list
    df_nearby['w'] = w_list
    df_nearby['h'] = h_list


    return df_nearby

index = -1
num = 0
i =0
while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        index += 1
        df = txt_to_df(result_path)
        #print(df['frame'][num])
        cv2.imwrite("./img/%08d.jpg" % index, frame, [100])

        if i == 0:
            a = cv2.imread('./img/00000000.jpg')
            video_h, video_w, _ = a.shape  # 获取一帧图像的宽高信息
            print('get')
            i = 1

        txt_name = os.path.join(img_path, '%08d.txt' % index)

        f = open(txt_name,'w')
        while(df['frame'][num] == index):
            t = int(df['x'][num])
            l = int(df['y'][num])
            w = int(df['w'][num])
            h = int(df['h'][num])
            x,y,w,h = tlwh2xywh(t,l,w,h)
            id = int(df['id'][num])
            f.write(('%g ' * 4 + '%g' + '\n') % (id, x/video_w, y/video_h,
                                                        w/video_w, h/video_h))  # label
            num += 1
    else:
        cap.release()
        cv2.destroyAllWindows()
        break




