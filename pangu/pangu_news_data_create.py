# 获取MongoDB中的新闻数据，生成盘古AI训练数据集
import jieba
import jieba.analyse
from pymongo import MongoClient
import openpyxl
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os
import datetime
import time


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def summarize(text, ratio=0.2):
    keywords = jieba.analyse.textrank(text, topK=int(len(text) * ratio), withWeight=False)
    summary = ''.join(keywords)
    return summary


time_delta = datetime.timedelta(hours=8)


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
            if content:
                summary = summarize(content, ratio=0.2)
            else:
                summary = ''
            release_time = news_doc.get('release_time', '') + time_delta  # 加8小时变成北京时间
            img_urls = news_doc.get('img', [])
            source = news_doc.get('source', '')
            data.append({
                'title': title,
                'content': content,
                'summary': summary,
                'release_time': release_time,
                'img_urls': img_urls,
                'source': source
            })
        return data

    def save_to_excel(self, filename):
        data = self.get_data
        today = datetime.datetime.now().strftime('%Y%m%d')
        directory = os.path.join(os.getcwd(), today)
        os.makedirs(directory, exist_ok=True)
        timestamp = str(int(time.time()))
        filepath = os.path.join(directory, f'{timestamp}.xlsx')
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "News Data"
        worksheet.append(['Title', 'Content', 'Summary', 'Release Time', 'Image URLs', 'Source'])
        for item in data:
            worksheet.append([
                item['title'],
                item['content'],
                item['summary'],
                item['release_time'],
                ', '.join(item['img_urls']),
                item['source']
            ])
        workbook.save(filepath)
        print(f"Excel file saved to: {filepath}")


# 使用示例
news_data = NewsData('ows_saas_online', 'OWS-SPIDER-NEWS-ZZB-SZF', 'ows_saas', 'ygYssBS5vL5oQnV&', '218.201.94.151')
news_data.save_to_excel('news_data.xlsx')
