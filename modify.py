import cv2
import numpy as np
import pandas as pd

root = './原视频和结果/112.mp4'
txt = './原视频和结果/112.txt'

cap = cv2.VideoCapture(root)
gt = open(txt)
#data = np.loadtxt(txt)


y =[]
x = []
time = []

#
# for i in range(0, int((data.shape[0]))):
#     id = data[i, 1]
#     time.append(data[i, 0])
#     x.append(data[i, 2])
#     y.append(data[i, 3])

def txt_to_df(txt_path):
    f =open(txt_path)
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
while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        index += 1
        df = txt_to_df(txt)
        print(df['frame'][num])

        while(df['frame'][num] == index):
            pt1 = (int(df['x'][num]) ,df['y'][num])
            pt2 = (df['x'][num] + int(df['w'][num]), df['y'][num] + int(df['h'][num]))
            #pt1 = (int(df['x'][num]) - int(df['w'][num]/2), int(df['y'][num]) - int(df['h'][num]/2))
            cv2.rectangle(frame, pt1, pt2, (0,255,255), thickness=8)
            cv2.putText(frame, str(df['id'][num]), pt1, cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)
            cv2.putText(frame, str(df['frame'][num]), (20,20), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)
            #cv2.putText(img, label, (x1, y1 + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)
            num += 1

        cv2.imshow('image', frame)
        k = cv2.waitKey(20)
        # q键退出
        if (k & 0xff == ord('q')):
            break

    else:
        cap.release()
        cv2.destroyAllWindows()
        break