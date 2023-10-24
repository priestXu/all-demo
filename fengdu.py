import csv
from pypinyin import lazy_pinyin

# 读取CSV文件
csv_file = '/Users/xuliduo/python_workspaces/all-demo/20230721/mingshanjiedao.csv'
output_file = '/Users/xuliduo/python_workspaces/all-demo/20230721/sql/mingshangjiedao.sql'  # 指定输出文件路径

with open(csv_file, newline='', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as output:
    reader = csv.reader(f)
    # 跳过前两行表头
    next(reader)
    next(reader)

    # 用于跟踪已生成的姓名及对应的数字后缀
    name_suffixes = {}

    for row in reader:
        # 从CSV文件中获取相应数据
        name = row[1]
        position = row[2]
        participants = row[3].split('、')

        # 生成SQL插入语句
        sql_template = "INSERT INTO pms.t_user (name, password, status, create_time, update_time, account) VALUES ('{name}', 'e10adc3949ba59abbe56e057f20f883e', 1, NOW(), NOW(), '{account}');"

        # 输出生成的SQL语句到文件
        for participant in participants:
            # 获取姓名的拼音，并转换为小写作为account
            name_pinyin = ''.join(lazy_pinyin(participant)).lower()

            # 检查是否有重名，如果有则添加数字后缀
            if name_pinyin in name_suffixes:
                name_suffixes[name_pinyin] += 1
                account = f"{name_pinyin}{name_suffixes[name_pinyin]}"
            else:
                name_suffixes[name_pinyin] = 1
                account = name_pinyin

            sql = sql_template.format(name=participant, account=account)
            output.write(sql + '\n')  # 将生成的SQL插入语句写入文件
