import xlrd
import xlwt
import xlsxwriter as xls

if __name__ == '__main__':
    xlsinput = xlrd.open_workbook("eval_vmat.xlsx")
    xlsouput = xls.Workbook("CE.xlsx")
    for start in range(0,4):
        for idx in range(start,24,8):
            print(xlsinput.sheet_names()[idx])
        print('d')
