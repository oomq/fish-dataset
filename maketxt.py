import os
import random

train_percent = 0.9
trainval_percent = 0.1
test_percent = 1
root = './'
print(os.getcwd())
trainfilepath = os.path.join(root, 'train')
testfilepath = os.path.join(root, 'test')

txtsavepath = os.path.join(root, 'ImageSets')
total_train = os.listdir(trainfilepath)
total_test = os.listdir(testfilepath)
# num = len(total_train)
# list = range(num)
# tr = int(num * train_percent)#训练集数量
# tv = int(num * trainval_percent)#验证集数量
#tt = int(len(total_test) * test_percent)#测试集数量
# train = random.sample(list, tr)
# #print(train)
# trainval = random.sample(train, tv)
#print(trainval)

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

ftrainval = open('ImageSets/val.txt', 'w')
ftest = open('ImageSets/test.txt', 'w')
ftrain = open('ImageSets/train.txt', 'w')

for train_dirs in total_train:
    h = os.listdir(os.path.join(trainfilepath, train_dirs))
    num = len(h)
    list = range(num)
    tr = int(num * train_percent)  # 训练集数量
    tv = int(num * trainval_percent)  # 验证集数量
    train = random.sample(list, tr)
    # print(train)
    trainval = random.sample(train, tv)
    for y in h :

        name = 'data/images/' + train_dirs +'/' + y.replace('txt', 'jpg') + '\n'
        y = int(y[5:8])
        if y in trainval:
            ftrainval.write(name)
        else:
            ftrain.write(name)

ftrainval.close()
ftrain.close()



# for i in list:
#     name = 'images/' + total_train[i] + '\n'
#     if i in train:
#         if i in trainval:
#             ftrainval.write(name)
#         else:
#             ftrain.write(name)
#     else:
#         ftrainval.write(name)
#
# ftrainval.close()
# ftrain.close()


for i in os.listdir(testfilepath):
    for y in os.listdir(os.path.join(testfilepath, i)):
        name = 'data/images/' + i + '/' + y.replace('txt', 'jpg') + '\n'
        ftest.write(name)
ftest.close()

#fval.close()
#ftest.close()/train.txt', 'w')
#fval = open('data/ImageSets/