import pandas as pd
import random
from datetime import datetime, timedelta
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(DateTimeEncoder, self).default(obj)


# 读取Excel文件
excel_file = 'files/20231025/互动留言导入数据.xlsx'  # 请替换为您的Excel文件路径
df = pd.read_excel(excel_file)

# MongoDB集合名称
collection_name = 'leaveMessage'

# 生成插入数据的JavaScript脚本
insert_scripts = []

for _, row in df.iterrows():
    data = {
        "regionId": 19,
        "reply": [],
        "mark": 0,
        "del": 0,
        "publish": 1,
        "type": 1,
        "newReply": 0,
        "_class": "com.goodsogood.ows.model.mongo.LeaveMessage"
    }

    # data["leaveMessageId"] = None
    data["orgId"] = 3  # int(row["org_id"]) if not pd.isna(row["org_id"]) else None  # 检查是否为NaN
    data["orgName"] = '中共重庆市烟草公司机关委员会系统管理员'  # row["组织"]
    data["unitOrgId"] = int(row["unit_org_id"]) if not pd.isna(row["unit_org_id"]) else None  # 检查是否为NaN
    data["unitOrgName"] = row["单位"]  # 从单位列获取unitOrgName
    data["unitShortName"] = row["单位简称"]
    data["userId"] = int(row["user_id"]) if not pd.isna(row["user_id"]) else None  # 检查是否为NaN
    data["userName"] = row["姓名"]
    data["content"] = row["留言内容"]
    data["actionId"] = None
    data["actionTitle"] = None
    data["approvalStatus"] = None
    data["approvalUserId"] = None
    data["approvalReason"] = None

    # 转换Timestamp对象为字符串，然后解析日期字符串并添加时分秒
    leave_time = row["留言时间"]
    if not pd.isna(leave_time):
        leave_time_str = leave_time.strftime('%Y-%m-%d')
        leave_time = datetime.strptime(leave_time_str, '%Y-%m-%d')
        leave_time = leave_time.replace(hour=0, minute=0, second=0)  # 设置时分秒为0
        data["createTime"] = f"ISODate('{leave_time.isoformat()}')"  # 包含ISODate函数
        data["updateTime"] = f"ISODate('{leave_time.isoformat()}')"  # 包含ISODate函数

    # 使用自定义的JSON编码器将数据转换为MongoDB插入脚本
    insert_script = f"db.{collection_name}.insert({json.dumps(data, cls=DateTimeEncoder, ensure_ascii=False)});"
    # 去掉ISODate外层的双引号
    insert_script = insert_script.replace('"ISODate(', 'ISODate(').replace(')"', ')')
    insert_scripts.append(insert_script)

# 输出JavaScript脚本
for script in insert_scripts:
    print(script)
