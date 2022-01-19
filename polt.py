import math

import xlrd
import xlwt
import xlsxwriter as xls
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

sns.set()

name_list = ["lianyu", "heiyu", "liyu", "caoyu"]
day_list =["day1first","day1second","day2first","day2second"]

def avg2excle():
    xlsinput = xlrd.open_workbook("eval_vmat.xls")
    xlsouput = xls.Workbook("CE.xls")
    datamatrix_c, datamatrix_e = np.zeros((40, 19)), np.zeros((40, 19))  # 生成一个nrows行ncols列，且元素均为0的初始矩阵

    for start in range(0,4):
        v_c, v_e = [], []
        for idc in range(start,24,8):
            print(xlsinput.sheet_names()[idc])
            table_c = xlsinput.sheet_by_index(idc)
            v_c = np.sum([v_c, table_c.col_values(1,start_rowx=0, end_rowx=4)], axis=0)
            temp = np.zeros((40, 19))
            for x in range(40):
                rows_c = np.matrix(table_c.row_values(x,start_colx=3))  # 把list转换为矩阵进行矩阵操作
                temp[x:] = rows_c  # 按列把数据存进矩阵中
            datamatrix_c += temp
        for ide in range(start+1,24,8):
            print(xlsinput.sheet_names()[ide])
            table_e = xlsinput.sheet_by_index(ide)
            v_e = np.sum([v_e, table_e.col_values(1,start_rowx=0, end_rowx=4)], axis=0)
            temp = np.zeros((40, 19))
            for x in range(40):
                rows_e = np.matrix(table_e.row_values(x,start_colx=3))  # 把list转换为矩阵进行矩阵操作
                temp[x:] = rows_e  # 按列把数据存进矩阵中
            datamatrix_e += temp
        print('d')
        ###记录数据在新excle
        v_c = v_c/3
        v_e = v_e/3
        worksheet = xlsouput.add_worksheet("{}".format(day_list[start]))
        worksheet.write_column("A1", name_list+["C"])
        worksheet.write_column("B1", v_c.tolist())
        worksheet.write_column("C1", name_list+["E"])
        worksheet.write_column("D1", v_e.tolist())
        for x_label in range(0, 4):
            worksheet.write('E{}'.format(x_label * 10 + 1), name_list[x_label] + "matC")
            worksheet.write('E{}'.format(x_label * 10 + 41), name_list[x_label] + "matE")
        for row in range(40):
            worksheet.write_row("F{}".format(row+1), datamatrix_c[row])
            worksheet.write_row("F{}".format(row + 41), datamatrix_e[row])

    xlsouput.close()

def polt_ce():
    x_c = [0, 2, 4, 6]
    x_e = [0.5, 2.5, 4.5, 6.5]
    x_name = [0.25,2.25,4.25,6.25]
    label = ["silver carp", "hybrid snakehead", "carp", "grass carp"]
    xlsinput = xlrd.open_workbook("CE.xls")
    for _index in range(4):
        table = xlsinput.sheet_by_index(_index)
        vc = table.col_values(1,start_rowx=0, end_rowx=4)
        ve = table.col_values(3,start_rowx=0, end_rowx=4)
        plt_v = plt.figure()
        plt.ylabel("V/(px/s)")
        plt.xlabel("Name")
        plt.xticks(x_name, label)
        plt.ylim(0,0.4)
        plt.bar(x_c, vc, width=0.5, color='r')
        plt.bar(x_e, ve, width=0.5, color='b')
        plt_v.savefig("pic/avg_V_{}.jpg".format(day_list[_index]))

        for  fish in range(0,80,10):
            plt_heatmap = plt.figure()
            temp = np.zeros((10, 19))
            for x in range(10):
                rows = np.matrix(table.row_values(fish+x ,start_colx=5))
                temp[x:] = rows
            sns_plot = sns.heatmap(temp, cmap="RdBu_r", linewidths=.5)
            _name = fish/10
            print(_name)
            if  _name <=3 :
                plt_heatmap.savefig("pic/heatmap{}_{}C.jpg".format(day_list[_index],name_list[math.floor(_name)]))
            else:
                plt_heatmap.savefig("pic/heatmap{}_{}E.jpg".format(day_list[_index], name_list[math.floor(_name-4)]))

if __name__ == '__main__':
    avg2excle()
