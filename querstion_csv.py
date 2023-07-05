import re

import pandas as pd

# 读取CSV文件
df = pd.read_csv('1.1.csv')

# 生成表2的数据
data = []
for _, row in df.iterrows():
    question = row['q']
    options = re.split(r'[A-Z][、.]', row['a'])
    options = [option.strip() for option in options if option.strip()]
    # options = row['a'].replace('\n','').strip().split('、')
    question_type = row['t']
    correct_answer = row['ta']
    ranking = '&'.join([chr(ord('A') + i) for i in range(len(options))])
    value = '&'.join(options)
    correct = '&'.join(list(correct_answer))

    data.append([question, ranking, value, question_type, correct])

# 创建表2的DataFrame
df2 = pd.DataFrame(data, columns=['question', 'ranking', 'value', 'questiontype', 'correct'])

# 保存为CSV文件
df2.to_csv('表2.1.csv', index=False)