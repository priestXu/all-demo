import re
import time

import mysql.connector
from pymongo import MongoClient

# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkmoderation.v2.region.moderation_region import ModerationRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkmoderation.v2 import *

words = [
    '熙来书记', '孙政才书记', '邓恢林', '五个重庆', '五大功能区', '低调务实', '少说多干', '三进三统', '民生十二条', '共富二十条',
    '说差共富', '走对路', '重庆模式', '民族分裂', '两岸关系', '当代中国', '反社会', '帝国主义', '完整', '马克思主义', '汪洋',
    '伊斯兰教', '全能神', '恐怖主义', '习书记', '总理', '晓波', '石泰峰', '看守所', '海南自由', '委员长', '中央政府',
    '三中全会', '恐怖袭击', '拉票贿选', '89年春夏之交', '党和国家', '习近年', '习XX', '近平', '令计划', '余杰', '薄熙来',
    '李总理', '遗留问题', '傅政华', '反党', '克强', '毛主席', '解决台湾', '总动员', '国家领袖', '反对党', '宪章', '六四',
    '俞正声', '张升民', '动乱', '锦涛总书记', '上访', '人民大会堂', '泽民', '台独', '中南海', '屠杀', '红色政权',
    '政令', '独立', '集会游行', '政治体制改革', '李小鹏', '改革开放', '王丹', '退党', '周恩来', '中共中央', '腐败中国',
    '知情者', '陈刚', '信息中心', '亡党', '郭伯雄', '志洪李', '林彪', '国家体育场', '习主席', '张军', '王小洪', '杨洁篪',
    '煽动颠覆国家政权', '七中全会', '政治局委员', '执政党', '破局', '官僚主义', '暴动', '一国两制', '3退', '天安门',
    '朱镕基', '文化大革命', '近习平', '整风运动', '抓捕', '集会', '民主化', '赖昌星', '地缘政治', '李长春', '中央对新疆',
    '刘奇葆', '保平安', '中国民主', '年改革', '政委', '胡锦涛', '民族冲突', '三个代表', '中国', '致中国', '功学',
    '温家宝', '镇压', '军事委员会', '同志习', '易纲', '洗净平', '习中央', '丽媛', '习近乎', '人民法院', '策反',
    '全国代表大会', '中国国家主席', '共产觉', '李干杰', '中央委员会', '周', '永康', '调查中共', '财政部', '人权', '中功',
    '中公', '全党', '反迫害', '沪宁', '中央人民政府', '江择民', '不信党', '全委会', '小平', '恶势力', '解放军',
    '国务委员', '腐败', '延安整风', '四个伟大', '朱德', '国办发', '全国政协', '朝鲜', '人大常委', '中国梦', '卖国',
    '文革', '中央候补委员', '中共国', '平反', '则民', '跑官要官', '粉碎四人帮', '贪污', '万里', '学联', '右派',
    '主席', '自焚', '门徒会', '人民广场', '香港', '法论功', '民联', '习斤平', '何立峰', '北京天安门', '农民起义',
    '进京', '国家领导人', '1989', '吴官正', '共和国主席', '锦涛', '十九届', '剿共', '徐才厚', '中朝', '王立军',
    '张德江', '习语', '民运', '天朝', '公民权利', '买官卖官', '不能定于一尊', '评中国共产党', '刘云山', '暴行',
    '董必武', '毛泽', '上中央', '李鹏', '庆红', '彭丽媛', '党组书记', '示威', '常委', '香港国安法', '中共', '共和党',
    '王毅', '反对日本', '邓小平', '打砸抢', '宪政', '国民党', '毛泽东思想', '反华势力', '反共', '共党', '9学',
    '三反五反', '政府', '江泽明', '国保大队', '丁薛祥', '天安门广场', '万钢', '一九八九年', '张高丽', '我的奋斗',
    '民族矛盾', '无政府主义者', '颠覆国家政权', '李克强', '颜色革命', '陈敏尔', '看中国', '殖民主义', '八九', '亡党亡国',
    '一寸山河一寸血', '国保', '大老虎', '国家主席', '赵紫阳', '习平', '胡春华', '九一八', '九二共识', '习仲勋',
    '泽东', '总司令', '杨晓渡', '中纪委', '维权', '选国家主席', '改革历程', '酷刑', '反革命', '毛泽东', '江青',
    '永康', '统一', '郭声琨', '汉奸', '帝王', '政治史', '国家安全', '共产', '叙利亚', '习总书记', '制度反腐',
    '联盟党'
]

tables = {
    # 't_news': ['content'],
    # 't_cm_activity': ['content'],
    't_meeting': ['name'],
    't_meeting_topic': ['topic_name'],
    't_topic_content': ['name'],
    't_topic_log': ['ans_cnt']
}

collections = {
    'messages-fd': ['content']
}

huawei_ak = "YJN3XNB95EAMUFC4EPR9"
huawei_sk = "5JznYzEPlSfFVkypYLf3lH9f7yIHHcG1r7a13rnM"
huawei_region = "cn-north-4"


def get_conn():
    return mysql.connector.connect(
        host='218.201.94.166',
        user='root',
        password='1234567890',
        # database='gs_ows_fd_test'
        database='gs_ows_szf_test'
    )


# 不关闭conn
def get_paged_data(table_name, fields, page_number, page_size, conn):
    # 创建游标对象
    cursor = conn.cursor()

    # 执行分页查询
    offset = (page_number - 1) * page_size
    query = "SELECT " + fields + " FROM " + table_name + " LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))

    # 获取查询结果
    results = cursor.fetchall()

    # 判断是否到达最后一页
    is_last_page = len(results) < page_size

    # 关闭游标和数据库连接
    cursor.close()

    return results, is_last_page


def get_mysql_data():
    datas = []
    # mysql
    conn = get_conn()
    count = 0
    # 遍历字典中的键值对
    for table, field in tables.items():
        # print(table, field[0])
        is_last_page = False
        page_number = 0
        while (is_last_page != True):
            content = ""
            page_number = page_number + 1
            paged_data, is_last_page = get_paged_data(table, field[0], page_number, 100, conn)
            for row in paged_data:
                field_value = re.sub(r"\s+", "", row[0])
                # # 处理字段值，例如打印输出
                # print(f"table: {table}, {field[0]}: {field_value}")
                content = content + "||" + field_value
            count = count + 1
            datas.append(content)
            # print(f"table: {table}, {field[0]}: {content}")
    conn.close()
    print(f"mysql:count: {count}")
    return datas


def get_mongodb_client(db_name):
    # 创建 MongoDB 连接
    client = MongoClient('mongodb://gs_ows_szf:1234567890@218.201.94.166:3717/' + db_name)
    return client


def get_mongodb_data():
    datas = []
    count = 0
    # mongodb
    for collection_name, field in collections.items():
        # 分页查询
        page_size = 50  # 每页的数据量
        page_number = 0  # 页码，从1开始
        db_name = "gs_ows_szf_test"
        client = get_mongodb_client(db_name)
        # 选择数据库和集合
        db = client[db_name]
        collection = db[collection_name]

        is_last_page = False
        while (is_last_page != True):
            content = ""
            page_number = page_number + 1
            # 计算跳过的文档数量
            skip_count = (page_number - 1) * page_size
            # 执行分页查询
            results = collection.find({}, {field[0]: 1}).skip(skip_count).limit(page_size)
            # 获取每页的 content
            for doc in results:
                # print(doc[field])
                content = content + re.sub(r"\s+", "", doc[field[0]])
            count = count + 1
            datas.append(content)

            # 获取集合中的文档数量
            total_documents = collection.count_documents({})
            # 判断是否为最后一页
            is_last_page = skip_count + page_size >= total_documents

            results.close()
        client.close()
        print(f"mongo:count: {count}")
        return datas


if __name__ == '__main__':
    datas = get_mysql_data()
    datas = datas + get_mongodb_data()
    print(len(datas))

    # 处理不超过5000个字符
    new_datas = []  # 新的列表，用于存储处理后的字符串
    for string in datas:
        if len(string) > 5000:
            # 如果字符串长度超过5000，将其拆分成多个小字符串
            chunks = [string[i:i + 5000] for i in range(0, len(string), 5000)]
            new_datas.extend(chunks)
        else:
            new_datas.append(string)

    print(len(new_datas))

    ak = huawei_ak
    sk = huawei_sk
    output_file = "output.txt"
    keys = set()

    credentials = BasicCredentials(ak, sk)

    client = ModerationClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(ModerationRegion.value_of(huawei_region)) \
        .build()
    for index, data in enumerate(new_datas):
        print(f"当前index--------------->[[[{index}]]]")
        if index != 0 and index % 1000 == 0:
            print("休眠...")
            # 等待30秒
            time.sleep(120)
        try:
            request = RunTextModerationRequest()
            listItemsbody = [
                TextDetectionItemsReq(
                    data
                )
            ]
            listWhiteGlossariesbody = [
                "ows"
            ]
            listCategoriesbody = [
                "politics"
            ]
            request.body = TextDetectionReq(
                items = listItemsbody,
                white_glossaries = listWhiteGlossariesbody,
                categories = listCategoriesbody
            )
            response = client.run_text_moderation(request)
            # print(response)
            if response.result.suggestion == 'block' and 'politics' in response.result.detail:
                print(f"detail:{response.result.detail}")
                keys.update(response.result.detail["politics"])
                print("=" * 100)
                print(data)
                print("*" * 100)
                print(','.join(response.result.detail["politics"]))
                with open(output_file, 'a') as file:
                    file.write("=" * 100 + "\n")
                    file.write(str(data) + "\n")
                    file.write("*" * 100 + "\n")
                    file.write(','.join(response.result.detail["politics"]) + "\n")
                    file.close()
        except exceptions.ClientRequestException as e:
            print("=" * 100)
            for key in keys:
                print(key)
            print("=" * 100)

            print(e.status_code)
            print(e.request_id)
            print(e.error_code)
            print(e.error_msg)

    print("=" * 100)
    for key in keys:
        print(key)
    print("=" * 100)
