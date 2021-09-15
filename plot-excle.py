import xlrd
import xlwt
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter as xls

path_input = 'output/track-915.xlsx'
result_path = 'output'
index = ['A','B','C','D','E','F']

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
    'avg_v',
    'a',
    'var',
    'turn'
]

class Fun(object):
    def __init__(self, data_path, result_path):
        super().__init__()
        self.data_path = data_path
        self.result_path = result_path

        self.twohours = 5400 # 1.5*3600
        self.twentyfour = 20*3600  #20h

        self.sample_time = 10
        self.exp_vs = []
        self.exp_vh = []
        self.exp_rest = []
        self.exp_a = []
        self.exp_var = []
        self.exp_swr = []
        self.xlsbook = xlrd.open_workbook(self.data_path)
        self.xlsoutput = xls.Workbook("track-test.xlsx")


    def execute(self):
        # print(self.xlsbook.nsheets)
        # print(self.xlsbook.sheet_names())
        for x in range(0,8):
            table_z = self.xlsbook.sheets()[x+8*2]
            table_x = self.xlsbook.sheets()[x]
            table_j = self.xlsbook.sheets()[x+8]
            exp_sheet = self.xlsoutput.add_worksheet('{}'.format(x+1))

            exp_sheet.write_row('A1', heading)  # 需要判断哪个单元开始
            for y in range(0,6):
                # print(heading[y])

                # self.exp_vs.append(table_z.col_values(y,1,self.twohours))
                # self.exp_vs.append(table_x.col_values(y,1,self.twentyfour))
                # self.exp_vs.append(table_j.col_values(y,1,self.twentyfour))
                # 填充0  统一时间
                self.exp_vs.append(table_z.col_values(y,1,self.twohours-1)
                                   + table_x.col_values(y,1,self.twentyfour-1)
                                   +table_j.col_values(y,1,self.twentyfour-1)
                                   )
                temp = []

                temp = [b for a,b in enumerate(self.exp_vs[0]) if a%self.sample_time==0]
                if y == 2:
                    self.exp_vh.append(
                        table_z.col_values(y, 1, 4) +
                        + table_x.col_values(y, 1, 40)+
                        + table_j.col_values(y, 1, 40)
                    )
                    self.plot_bar(self, y, x, heading)
                    self.exp_vh =[]

                self.plot_vis(temp, y, x, heading)
                exp_sheet.write_column('{}2'.format(index[y]), temp)
                self.exp_vs = []
        self.xlsoutput.close()

    def plot_bar(self,y,x,heading):
        n = len(self.exp_vh)
        fig = plt.figure(dpi=300)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_title('{}-{}'.format(exp_ind[x], heading[y]))
        ax1.set_xlabel('hours')
        x_zhou = np.linspace(-1.5, 40, n).tolist()
        plt.plot(x_zhou, self.exp_vh, 'bo-', linewidth=1)
        plt.xlim(-1.5, 40)
        plt.savefig(result_path + '/{}-{}.png'.format(exp_ind[x], heading[y]))


    def plot_vis(self,temp,y,x,heading):
        n = len(temp)
        fig = plt.figure(dpi=300) # figsize=
        # 将画图窗口分成1行1列，选择第一块区域作子图
        ax1 = fig.add_subplot(1, 1, 1)
        # 设置标题
        ax1.set_title('{}-{}'.format(exp_ind[x],heading[y]))
        # 设置横坐标名称
        ax1.set_xlabel('hours')
        # 设置纵坐标名称
        # ax1.set_ylabel('{}'.format(heading[y]))
        # x_zhou = np.random.uniform(-2, 40, n).tolist()
        x_zhou = np.linspace(-1.5,40,n).tolist()
        ax1.scatter(x_zhou, temp, s=0.5, c='r', marker='.')
        y2 = np.random.uniform(0, 5, n)
        x2 = np.array([self.twentyfour] * n)
        x1 = np.array([0] * n)
        # ax1.plot(x1, y2, c='b', ls='--')
        # ax1.plot(x2, y2, c='b', ls='--')
        plt.xlim(-1.5,40)
        plt.savefig(result_path+'/{}-{}.png'.format(exp_ind[x],heading[y]))

if __name__ == '__main__':
    fun = Fun(path_input,result_path)
    fun.execute()