# 获取MongoDB中的新闻数据，生成milvus向量数据集
import jieba
import jieba.analyse
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os
import datetime as dt
from datetime import datetime


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def summarize(text, ratio=0.2):
    keywords = jieba.analyse.textrank(text, topK=int(len(text) * ratio), withWeight=False)
    summary = ''.join(keywords)
    return summary


time_delta = dt.timedelta(hours=8)


def parse_date(date_str):
    try:
        # 尝试解析日期时间
        date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        formatted_date = date_time.strftime('%Y年%-m月%-d日')  # %Y年 %#m月 %#d日
    except ValueError:
        try:
            # 尝试解析日期
            date = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = date.strftime('%Y年%-m月%-d日')
        except ValueError:
            # 解析失败，返回原始字符串
            formatted_date = date_str
    return formatted_date


class NewsData:
    def __init__(self, db_name, collection_name, username, password, ip, max_length=600):
        print('mongodb://{}:{}@{}:3717/{}'.format(username, password, ip, db_name))
        self.client = MongoClient('mongodb://{}:{}@{}:3717/{}'.format(username, password, ip, db_name))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.max_length = max_length

    @property
    def get_data(self):
        data = []
        news_docs = self.collection.find()
        for news_doc in tqdm(news_docs, desc='Processing news'):
            title = news_doc.get('title', '')
            content = clean_html(news_doc.get('content', ''))
            # if content:
            #     summary = summarize(content, ratio=0.2)
            # else:
            #     summary = ''
            release_time = news_doc.get('release_time', '') + time_delta  # 加8小时变成北京时间
            # img_urls = news_doc.get('img', [])
            # source = news_doc.get('source', '')
            data.append({
                '标题': title,
                '正文': content,
                # '摘要': summary,
                '发布时间': release_time,
                # '图片链接': img_urls,
                # '来源': source
            })
        return data

    def save_to_md(self):
        data = self.get_data
        today = dt.datetime.now().strftime('%Y%m%d')
        directory = os.path.join(os.getcwd(), "files", today)
        os.makedirs(directory, exist_ok=True)
        for item in data:
            # 提取发布日期
            release_date = item['发布时间'].date().isoformat()

            # 构建文件名
            filename = f"{item['标题']}_{release_date}"
            filename = ''.join(c for c in filename if c.isalnum() or c in ['-', '_', ' '])  # 去除非法字符
            filename = filename[:100]  # 限制文件名长度不超过100个字符

            filepath = os.path.join(directory, f'{filename}.md')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {parse_date(str(item['发布时间']))} - {item['标题']}\n\n")
                f.write(f"{item['正文']}\n\n")
                # f.write(f"## 摘要\n\n{item['摘要']}\n\n")
                f.write(f"## 发布时间：{item['发布时间']}\n\n")
                # f.write(f"## 图片链接\n\n")
                # for img_url in item['图片链接']:
                #     f.write(f"{img_url}\n")
                # f.write(f"\n## 来源\n\n{item['来源']}\n\n")
        print(f"Markdown files saved to: {directory}")


# 使用示例
news_data = NewsData('ows_saas_online', 'OWS-SPIDER-NEWS-ZZB-SZF', 'ows_saas', 'ygYssBS5vL5oQnV&', '218.201.94.151')
news_data.save_to_md()
