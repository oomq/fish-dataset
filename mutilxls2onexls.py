import pandas as pd
import os

ls = []
for dirpath, dirname, files in os.walk(r'output'):
    for file in files:
        if file.endswith('xlsx'):
            # 为防止文件与代码不在同一个路径时出错，组合绝对路径
            ls.append(dirpath + '\\' + file)

# pd.ExcelWriter 函数可以追加写入
sheetname_list = []
with pd.ExcelWriter(r'test.xlsx', mode='w+') as xlsx:
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
