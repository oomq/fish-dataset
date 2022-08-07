import pandas as pd
import os

input_folder = r'output-test'
output_pathname = r'test-test.xlsx'
ls = []
for dirpath, dirname, files in os.walk(input_folder):
    for file in files:
        if "09" in file:
            continue
        if file.endswith('xlsx'):
            # 为防止文件与代码不在同一个路径时出错，组合绝对路径
            ls.append(dirpath + '\\' + file)

# pd.ExcelWriter 函数可以追加写入
sheetname_list = []
with pd.ExcelWriter(output_pathname, mode='w+') as xlsx:
    for file in ls:
        df = pd.read_excel(file, sheet_name=None)
        # 获取excel 的表名称
        sheet_names = df.keys()
        # 循环获取每个表的内容，并写入文件中
        for sheet_name in sheet_names:
            # if sheet_name in sheetNamelist:
            #     pass
            #     name = sheet_name + '_1'
            # else:
            #     name = sheet_name
            name = sheet_name
            sheetname_list.append(name)
            df1 = pd.read_excel(file, sheet_name=sheet_name)
            df1.to_excel(xlsx, sheet_name=name, index=False)
