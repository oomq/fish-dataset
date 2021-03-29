import os

import numpy as np
root = './reid/train'
testpath = './reid/test'

def moveFile(fileDir, targetDir, rate):
    '''
    fileDir是训练集文件夹
    targetDir是目标文件夹
    rate是移动比例
    '''
    import random, shutil, os

    # 首先我的目标是生成一个字典, key是类别文件夹路径, 对应的value是里面的图片名字;
    # directory_path_list = []
    # file_path_list = {}
    # picture_number_list = []
    # for i in os.listdir(fileDir):
    #     directory_path = os.path.join(fileDir, i)
    #     directory_path_list.append(directory_path)
    #     picture_number_list.append(len(os.listdir(directory_path)))

    directory_path_list = []
    file_path_list = {}
    picture_number_list = []
    for i in os.listdir(fileDir):
        directory_path = os.path.join(fileDir, i)
        directory_path_list.append(directory_path)
        picture_number_list.append(len(os.listdir(directory_path)))

    # print(directory_path_list)
    # print(picture_number_list)

    for i in directory_path_list:
        file_path_list[i] = os.listdir(i)
    # print(file_path_list)
    # 计算每个子文件夹需要移走的图片数量
    pick_number_list = (np.array(picture_number_list) * rate).astype(int)
    # print(pick_number_list)

    for num, (directory, filenames) in zip(pick_number_list, file_path_list.items()):
        # print(num, directory)
        file_list = [os.path.join(directory, i) for i in filenames]
        # print(file_list)
        sample = random.sample(file_list, num)
        for name in sample:
            if os.path.exists(targetDir):
                pass
            else:
                os.mkdir(targetDir)
            if os.path.exists(os.path.join(targetDir, (name.split('\\')[1]))):
                pass
            else:
                os.mkdir(os.path.join(targetDir, (name.split('\\')[1])))
            target = os.path.join(targetDir, name.split('\\')[1])
            shutil.move(name, target)



moveFile(root,testpath,0.3)
