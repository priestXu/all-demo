import pandas as pd
import uuid

# 读取Excel文件，假设需要处理的列名为"uuid_column"
df = pd.read_excel("/Users/xuliduo/python_workspaces/all-demo/20230724/1.xlsx")

# 使用groupby和transform函数找到重复记录的索引
duplicate_mask = df.duplicated(subset="token", keep=False)

# 为重复记录生成新的UUID并更新原始数据框
def generate_uuid():
    return str(uuid.uuid4()).replace("-", "")

df.loc[duplicate_mask, "token"] = [generate_uuid() for _ in range(duplicate_mask.sum())]

# 保存更新后的数据框回Excel文件
df.to_excel("/Users/xuliduo/python_workspaces/all-demo/20230724/2.xlsx", index=False)
