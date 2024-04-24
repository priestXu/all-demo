import pandas as pd
import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 连接到 MySQL 数据库
conn = mysql.connector.connect(
    # host="218.201.94.166",
    # user="root",
    # password="1234567890",
    # database="gs_ows_cps_test"
    host="218.201.94.151",
    user="gs_ows_cps",
    password="ZEn7YdNezZNqrf@c",
    database="gs_ows_cps_online"
)
cursor = conn.cursor()

# 读取 Excel 文件
df = pd.read_csv("files/20240407/数字赋能人员信息收集(0407).csv", na_filter=[''])


# 处理身份证号，计算年龄和生日
def calculate_age_and_birthday(identity):
    birth_year = int(identity[6:10])
    birth_month = int(identity[10:12])
    birth_day = int(identity[12:14])
    today = datetime.now()
    birth_date = datetime(birth_year, birth_month, birth_day)
    age = relativedelta(today, birth_date).years
    return age, birth_date.strftime("%Y-%m-%d")


# 遍历 Excel 中的每一行数据
for index, row in df.iterrows():
    name = row['姓名']
    gender = row['性别']
    gender_value = row['性别']
    gender = 1 if gender_value == '男' else 2  # 根据数字判断性别
    identity = row['身份证号']
    age, birthday = calculate_age_and_birthday(identity)
    phone = row['手机号']
    branch_depart = row['所在支部']

    # 插入到 t_user 表中
    cursor.execute(
        "INSERT INTO t_user (name, gender, identity, age, birthday, phone, branch_depart) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, gender, identity, age, birthday, phone, branch_depart))
    user_id = cursor.lastrowid  # 获取插入的用户ID

    # 插入到 t_common_addresses 表中
    consignee = row['姓名']
    phone = row['手机号']
    address1 = row['常用地址1（默认地址）']
    address2 = row['常用地址2']
    address3 = row['常用地址3']
    addresses = [address1, address2, address3]
    for idx, addr in enumerate(addresses, start=1):
        if pd.notna(addr) and addr.strip():
            if idx == 1:  # 第一个地址设为默认地址
                has_default = 1
            else:
                has_default = 0
            # 添加调试信息
            print(f"Inserting address for user {user_id}: {consignee}, {phone}, {addr}, {has_default}")
            cursor.execute(
                "INSERT INTO t_common_addresses (user_id, consignee, phone, address, has_default) VALUES (%s, %s, %s, %s, %s)",
                (user_id, consignee, phone, addr, has_default))

# 提交事务并关闭连接
conn.commit()
cursor.close()
conn.close()
