
import xlrd
import xlwt
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter as xls

path_input = 'track-all.xlsx'
result_path = 'output'
index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

exp_ind = [
    '4.8-80',
    '4.8-8000',
    '19.2-8000',
    '19.2-80',
    '1.2-80',
    '1.2-8000',
    '0.3-8000',
    '0.3-80'
]

heading = [
    'v',
    'rest_time',
    'avg_v_30',
    'avg_v_20',
    'avg_v_10',
    'avg_v_5',
    'a',
    'var',
    'turn',
    'v_times'
]

exp_ind_change = [7, 4, 0, 3, 6, 5, 1, 2]

heading_unit = [
    'mm/s',
    's',
    'mm/0.5h',
    'mm/20mins',
    'mm/10mins',
    'mm/5mins',
    'mm/s^2',
    'mm^2',
    'times'
]

color = [
    'r', 'gold', 'b', 'k', 'g', 'c', 'm', 'y'
]

y_zhou = [
    5,
    1,
    3,
    3,
    3,
    3,
    3,
    20000,
    300,
]


class Fun(object):
    def __init__(self, data_path, result_path):
        super().__init__()
        self.data_path = data_path
        self.result_path = result_path
        # 10s采样 915
        # self.twohours = 5400 # 1.5*3600
        # self.twentyfour = 20*3600  #20h

        # 10s平均 916
        self.twohours = 540  # 1.5*3600
        self.twentyfour = 2 * 3600  # 20h

        self.sample_time = 1
        self.exp_vs = []
        self.exp_vh = []
        self.exp_rest = []
        self.exp_a = []
        self.exp_var = []
        self.exp_swr = []
        self.xlsbook = xlrd.open_workbook(self.data_path)
        self.xlsoutput = xls.Workbook("track-test.xlsx")
        self.exp_thres = 6 * 60 * 4
        self.big_thres = 2
        self.mid_thres = 1
        self.small_thres = 0.1
        self.big_v = []
        self.mid_v = []
        self.small_v = []
        self.exp_rest_graph = []

    def execute(self):
        # print(self.xlsbook.nsheets)
        # print(self.xlsbook.sheet_names())

        for x in range(0, 8):
            table_z = self.xlsbook.sheets()[x + 8 * 2]
            table_x = self.xlsbook.sheets()[x]
            table_j = self.xlsbook.sheets()[x + 8]
            exp_sheet = self.xlsoutput.add_worksheet('{}'.format(x + 1))

            exp_sheet.write_row('A1', heading)  # 需要判断哪个单元开始
            for y in range(0, 9):
                print(y)
                if y == 2:  # 30
                    self.exp_vh.append(
                        table_z.col_values(y, 1, 4)
                        + table_x.col_values(y, 1, 40)
                        + table_j.col_values(y, 1, 40)
                    )
                    self.plot_bar(y, x, heading)
                    self.exp_vh = []
                    continue
                elif y == 3:  # 20
                    self.exp_vh.append(
                        table_z.col_values(y, 1, 5)
                        + table_x.col_values(y, 1, 60)
                        + table_j.col_values(y, 1, 60)
                    )
                    self.plot_bar(y, x, heading)
                    self.exp_vh = []
                    continue
                elif y == 4:  # 10
                    self.exp_vh.append(
                        table_z.col_values(y, 1, 9)
                        + table_x.col_values(y, 1, 120)
                        + table_j.col_values(y, 1, 120)
                    )
                    self.plot_bar(y, x, heading)
                    self.exp_vh = []
                    continue
                elif y == 5:  # 5
                    self.exp_vh.append(
                        table_z.col_values(y, 1, 18)
                        + table_x.col_values(y, 1, 240)
                        + table_j.col_values(y, 1, 240)
                    )
                    self.plot_bar(y, x, heading)
                    self.exp_vh = []
                    continue

                # print(heading[y])
                # self.exp_vs.append(table_z.col_values(y,1,self.twohours))
                # self.exp_vs.append(table_x.col_values(y,1,self.twentyfour))
                # self.exp_vs.append(table_j.col_values(y,1,self.twentyfour))
                # 填充0  统一时间
                if y == 1:
                    self.exp_vs.append(table_z.col_values(y, 1, self.twohours - 1)
                                       + table_x.col_values(y, 1, self.twentyfour - 1)
                                       + table_j.col_values(y, 1, self.twentyfour - 1)
                                       )
                    temp = []
                    temp = [b for a, b in enumerate(self.exp_vs[0]) if a % self.sample_time == 0]
                else:
                    self.exp_vs.append(table_z.col_values(y, 1, self.twohours - 1)
                                       + table_x.col_values(y, 1, self.twentyfour - 1)
                                       + table_j.col_values(y, 1, self.twentyfour - 1)
                                       )
                    temp = []
                    temp = [b for a, b in enumerate(self.exp_vs[0]) if a % self.sample_time == 0]

                if y == 8:
                    self.exp_swr.append(self.exp_vs[0])

                self.plot_vis(temp, y, x, heading)
                exp_sheet.write_column('{}2'.format(index[y]), temp)
                self.exp_vs = []
        self.plot_eight(y, x, heading)
        self.xlsoutput.close()

    def plot_eight(self, y, x, heading):
        n = len(self.exp_swr[0])
        fig_turn = plt.figure(dpi=300)
        ax5 = fig_turn.add_subplot(1, 1, 1)
        ax5.set_title('{}-{}'.format(exp_ind[x], heading[y]))
        ax5.set_xlabel('hours')

        plt.xlim(-1.5, 40)
        # plt.ylim(0, y_zhou[5])
        x_zhou = np.linspace(-1.5, 40, n).tolist()
        for ind, data in enumerate(self.exp_swr):
            # print(color[ind])
            ax5.scatter(x_zhou, self.exp_swr[ind], s=0.5, c=color[ind], marker='.')
        plt.legend(loc='upper left', markerscale=15)
        plt.axvspan(xmin=-1.5, xmax=0.0, facecolor='m', alpha=0.3)
        plt.axvspan(xmin=0.0, xmax=20.0, facecolor='y', alpha=0.3)
        plt.axvspan(xmin=20.0, xmax=40.0, facecolor='b', alpha=0.3)
        plt.savefig(result_path + '/eight.png')

    def plot_bar(self, y, x, heading):
        n = len(self.exp_vh[0])
        fig = plt.figure(dpi=300)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_title('{}-{}'.format(exp_ind[x], heading[y]))
        ax1.set_xlabel('hours')
        x_zhou = np.linspace(-1.5, 40, n).tolist()
        plt.axvspan(xmin=-1.5, xmax=0.0, facecolor='m', alpha=0.3)
        plt.axvspan(xmin=0.0, xmax=20.0, facecolor='y', alpha=0.3)
        plt.axvspan(xmin=20.0, xmax=40.0, facecolor='b', alpha=0.3)

        plt.ylim(0, y_zhou[y])
        plt.plot(x_zhou, self.exp_vh[0], 'bo-', linewidth=1, markersize=2)
        plt.xlim(-1.5, 40)
        plt.savefig(result_path + '/{}-{}.png'.format(exp_ind[x], heading[y]))

    def plot_vis(self, temp, y, x, heading):
        n = len(temp)
        fig = plt.figure(dpi=300)  # figsize=
        # 将画图窗口分成1行1列，选择第一块区域作子图
        ax1 = fig.add_subplot(1, 1, 1)
        # 设置标题
        ax1.set_title('{}-{}'.format(exp_ind[x], heading[y]))
        # 设置横坐标名称
        ax1.set_xlabel('hours')
        # 设置纵坐标名称
        ax1.set_ylabel('{}'.format(heading_unit[y]))
        # x_zhou = np.random.uniform(-2, 40, n).tolist()
        x_zhou = np.linspace(-1.5, 40, n).tolist()
        if y == 3:
            plt.ylim(-y_zhou[3], y_zhou[3])
        elif y == 1:
            plt.ylim(-0.05, y_zhou[y])
        else:
            plt.ylim(-0.5, y_zhou[y])
        ax1.scatter(x_zhou, temp, s=0.5, c='r', marker='.')
        plt.axvspan(xmin=-1.5, xmax=0.0, facecolor='m', alpha=0.3)
        plt.axvspan(xmin=0.0, xmax=20.0, facecolor='y', alpha=0.3)
        plt.axvspan(xmin=20.0, xmax=40.0, facecolor='b', alpha=0.3)
        y2 = np.random.uniform(0, 5, n)
        x2 = np.array([self.twentyfour] * n)
        x1 = np.array([0] * n)
        # ax1.plot(x1, y2, c='b', ls='--')
        # ax1.plot(x2, y2, c='b', ls='--')
        plt.xlim(-1.5, 40)

        plt.savefig(result_path + '/{}-{}.png'.format(exp_ind[x], heading[y]))

    def plot_v(self):
        for x in range(0, 8):
            self.exp_vs = []
            self.big_v = []
            self.mid_v = []
            self.small_v = []
            table_z = self.xlsbook.sheets()[x + 8 * 2]
            table_x = self.xlsbook.sheets()[x]
            table_j = self.xlsbook.sheets()[x + 8]
            exp_sheet = self.xlsoutput.add_worksheet('{}'.format(x + 1))
            self.exp_vs.append(table_z.col_values(0, 1, 1)  # 只用算一次
                               + table_x.col_values(0, 1, 6 * 60 * 20 + 2)
                               + table_j.col_values(0, 1, 6 * 60 * 20 + 2)
                               )
            temp = []

            temp_big, temp_mid, temp_small = 0, 0, 0
            for a, v in enumerate(self.exp_vs[0]):
                if a % self.exp_thres != 0:
                    if v > self.big_thres:
                        temp_big += 1
                    elif v > self.mid_thres:
                        temp_mid += 1
                    elif v > self.small_thres:
                        temp_small += 1
                else:
                    self.big_v.append(temp_big * 10)
                    self.mid_v.append(temp_mid * 10)
                    self.small_v.append(temp_small * 10)
                    temp_big, temp_mid, temp_small = 0, 0, 0

            n = len(self.small_v)
            print(n)
            fig = plt.figure(dpi=300)  # figsize=
            # 将画图窗口分成1行1列，选择第一块区域作子图
            ax1 = fig.add_subplot(1, 1, 1)
            # 设置标题
            ax1.set_title('{}-{}'.format(exp_ind[x], heading[9]))
            # 设置横坐标名称
            ax1.set_xlabel('hours')
            # 设置纵坐标名称
            ax1.set_ylabel('{}'.format(heading_unit[8]))
            # x_zhou = np.random.uniform(-2, 40, n).tolist()
            total_width = 0.8
            width = total_width / 3
            x_zhoul = (np.linspace(-2, 40, n) - (total_width - width) / 2).tolist()
            x_zhou = (np.linspace(-2, 40, n) - (total_width - width) / 2 + width).tolist()
            x_zhour = (np.linspace(-2, 40, n) - (total_width - width) / 2 + 2 * width).tolist()
            plt.xlim(-2, 43)
            plt.ylim(0, 3600 * 4)
            plt.bar(x_zhoul, self.small_v, facecolor='lightskyblue',
                    edgecolor='white', label='low')
            plt.bar(x_zhou, self.mid_v, facecolor='yellow',
                    edgecolor='white', label='mid', )
            plt.bar(x_zhour, self.big_v, facecolor='green',
                    edgecolor='white', label='high', )
            plt.legend(loc='upper left')
            plt.savefig(result_path + '/{}-{}-{}.png'.format(exp_ind[x], heading[0], self.exp_thres))

    def bar_graph_rest(self):
        for x in range(0, 8):
            table_z = self.xlsbook.sheets()[x + 8 * 2]
            table_x = self.xlsbook.sheets()[x]
            table_j = self.xlsbook.sheets()[x + 8]
            exp_sheet = self.xlsoutput.add_worksheet('{}'.format(x + 1))
            hour = 1  # 需要换成2h 或 5h 改这个就行
            value = sum(table_z.col_values(1, 1, 3600 * hour))
            self.exp_rest_graph.append(value)
            for i in range(int(20 / hour)):
                value = sum(table_x.col_values(1, 1 + i * 3600 * hour, 3600 * hour + i * 3600 * hour))
                self.exp_rest_graph.append(value)
            for i in range(int(20 / hour)):
                value = sum(table_j.col_values(1, 1 + i * 3600 * hour, 3600 * hour + i * 3600 * hour))
                self.exp_rest_graph.append(value)
            n = len(self.exp_rest_graph)
            print(n)
            fig = plt.figure(dpi=300)
            ax1 = fig.add_subplot(1, 1, 1)
            ax1.set_title('{}-rest_{}h'.format(exp_ind[x], hour))
            x_zhou = np.linspace(-1, 40 / hour, n).tolist()
            ax1.set_xlabel('hours')
            ax1.set_ylabel('s')
            plt.bar(x_zhou, self.exp_rest_graph)
            plt.xlim(-1.5, 40 / hour)
            plt.ylim(0, 3600 * hour)
            plt.savefig(result_path + '/{}-rest_{}h.png'.format(exp_ind[x], hour))
            self.exp_rest_graph = []


if __name__ == '__main__':
    fun = Fun(path_input, result_path)
    fun.execute()
    # fun.plot_v()
