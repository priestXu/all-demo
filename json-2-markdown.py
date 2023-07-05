import json
import os
import re

# 指定包含JSON文件的目录路径
json_dir = '/Users/xuliduo/Downloads/data'

# 定义包含type值的数组
allowed_types = [
    # 'CqjgdjCINews',  # szf 走进工委-> 工委资讯
    # 'CqjgdjCSNews',  # szf 党建要问 -> 中央精神
    # 'CqjgdjPCRNews',  # szf 党建要问 -> 市委要求
    # 'CqjgdjDDNews',  # szf 工作动态 -> 部门动态
    # 'CqjgdjGWNews',  # szf 工作动态 -> 群团工作
    # 'CqjgdjPSCNews',  # szf 党风廉政
    # 'CqjgdjDCFNews',  # szf 工作动态 -> 区县传真
    # 'CpcImportant',  # tobacco 党建要闻
    # 'CpcLibrary',  # tobacco 人民网书库
    # 'Twenty',  # tobacco 二十大
    'LpSpeech',  # 三峡 习近平重要讲话
    # 'LpActivity',  # 三峡 习近平重要活动
    # 'CpcExclusive',  # 三峡 要闻->独家稿件
    # 'CpcNews',  # 三峡 要闻->新闻发布
    # 'CpcPartyBuilding',  # 三峡 党建要闻
    # 'CpcDiscuss',  # 三峡 重要论述
    # 'TodayInHistory',  # 三峡 历史上的今天
    # 'CpcMeeting',  # 三峡 重要会议
    # 'CpcEvents',  # 三峡 重要事件
    # 'CpcCharacter',  # 三峡 人物长廊
    # 'NormativeDoc',  # 三峡 规范性文件
]

# 正则表达式模式，用于匹配HTML标签和JavaScript代码
html_pattern = r'<[^>]+>'
js_pattern = r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>'

# 每个文件的最大字符数
max_chars_per_file = 20000

# 遍历目录中的每个JSON文件
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        json_file = os.path.join(json_dir, filename)

        # 读取JSON数据
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = file.read()

        # 解析JSON数据
        data = json.loads(json_data)

        # 创建Markdown文件名前缀（使用JSON文件名，将扩展名改为.md）
        markdown_file_prefix = os.path.splitext(json_file)[0]

        # 遍历每个JSON对象并生成Markdown文件
        for i, record in enumerate(data['RECORDS']):
            # 检查type字段是否在allowed_types数组中
            if record['type'] in allowed_types:
                # 移除HTML标签和JavaScript代码
                content = re.sub(html_pattern, '', record['content'])
                content = re.sub(js_pattern, '', content)

                # 分割内容为多个部分
                parts = [content[j:j + max_chars_per_file] for j in range(0, len(content), max_chars_per_file)]

                # 生成Markdown文件名（以type作为前缀，加上序号）
                markdown_filename = f"{record['type']}_{i + 1}.md"

                # 生成Markdown文件路径
                markdown_file = os.path.join(json_dir, markdown_filename)

                # 生成Markdown文件
                with open(markdown_file, 'w', encoding='utf-8') as file:
                    for part in parts:
                        # 构建Markdown内容
                        markdown_content = f"# {record['title']}\n\n{part}\n\n---\n"

                        # 写入Markdown文件
                        file.write(markdown_content)
