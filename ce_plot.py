import math

import xlrd
import xlwt
import xlsxwriter as xls
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

x_c = [0, 2, 4, 6]
x_e = [0.5, 2.5, 4.5, 6.5]
x_name = [0.25, 2.25, 4.25, 6.25]
label = ["silver carp", "hybrid snakehead", "carp", "grass carp"]
day_list = ["first", "second"]
name_list = ["lianyu", "heiyu", "liyu", "caoyu"]
xlsinput = xlrd.open_workbook("CE_2.xls")
for  _index in range(2):
    table = xlsinput.sheet_by_index(_index)
    vc = table.col_values(1, start_rowx=0, end_rowx=4)
    ve = table.col_values(3, start_rowx=0, end_rowx=4)
    plt_v = plt.figure()
    plt.ylabel("V/(px/s)")
    plt.xlabel("Name")
    plt.xticks(x_name, label)
    plt.ylim(0, 0.4)
    plt.bar(x_c, vc, width=0.5, color='r')
    plt.bar(x_e, ve, width=0.5, color='b')
    plt_v.savefig("pic/avg_V_{}.jpg".format(day_list[_index]))


table = xlsinput.sheet_by_index(2)
for fish in range(0, 80, 10):
    plt_heatmap = plt.figure()
    temp = np.zeros((10, 19))
    for x in range(10):
        rows = np.matrix(table.row_values(fish + x, start_colx=5))
        temp[x:] = rows
    sns_plot = sns.heatmap(temp, cmap="RdBu_r", linewidths=.5)
    _name = fish / 10
    print(_name)
    if _name <= 3:
        plt_heatmap.savefig("pic/heatmap{}C.jpg".format( name_list[math.floor(_name)]))
    else:
        plt_heatmap.savefig("pic/heatmap{}E.jpg".format(name_list[math.floor(_name - 4)]))



def xls4toxls2():
    xlsinput = xlrd.open_workbook("CE_4.xls")
    xlsouput = xls.Workbook("CE_2.xls")
    day_list = ["first", "second"]

    name_list = ["lianyu", "heiyu", "liyu", "caoyu"]
    for idx in range(2):
        v_c, v_e = [], []
        worksheet = xlsouput.add_worksheet("{}".format(day_list[idx]))
        for start in range(idx, 4,2):
            table_c = xlsinput.sheet_by_index(start)
            v_c =np.sum([v_c, table_c.col_values(1,start_rowx=0, end_rowx=4)], axis=0)
            v_e = np.sum([v_e, table_c.col_values(3,start_rowx=0, end_rowx=4)], axis=0)

        v_c=v_c/2
        v_e=v_e/2
        worksheet.write_column("A1", name_list + ["C"])
        worksheet.write_column("B1", v_c.tolist())
        worksheet.write_column("C1", name_list + ["E"])
        worksheet.write_column("D1", v_e.tolist())


    datamatrix_e = np.zeros((80, 19))
    for start in range(0,4):
        table = xlsinput.sheet_by_index(start)
        temp = np.zeros((80, 19))

        for x in range(80):
            rows_c = np.matrix(table.row_values(x, start_colx=5))
            temp[x:] = rows_c
        datamatrix_e+=temp
    worksheet = xlsouput.add_worksheet("heatmap")
    for x_label in range(0, 4):
        worksheet.write('E{}'.format(x_label * 10 + 1), name_list[x_label] + "matC")
        worksheet.write('E{}'.format(x_label * 10 + 41), name_list[x_label] + "matE")
    for row in range(80):
        worksheet.write_row("F{}".format(row + 1), datamatrix_e[row])

    xlsouput.close()
