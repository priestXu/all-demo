#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
#接口地址
url ="http://ltpapi.xfyun.cn/v1/ke"
#开放平台应用ID
x_appid = "6017d908"
#开放平台应用接口秘钥
api_key = "7b6a8bcbfdf58adc43b263d29ca01145"
#语言文本
TEXT=""" 让校园更加突显文化？
无
家庭教育关系
师生成长
家庭教育
无
如何有效进行谈会
学习平台，成长空间
如何与孩子沟通交流
家庭教育指导
共同学习，分享成长。
师生成长
暂无
读党史
无
暂无
师生成长困惑
暂时无
无
优课资源网址、资源搜索等
可以定期组织师生共读活动
了解更多的便民服务
从专业成长走向生命成长
更好融入学生校园生活
教师培训与学习
师生共成长
便民服务
徒步活动，强身健体
校园生活新方式
保障服务
校园安全
无

无
期待能够学习一些教师自我成长的干货！
无
无
无
教师职业成长
愉快工作  共同成长
无
家庭教育
家校合作，共助成长
教具学具提供
无
 语文教师如何快速成长
怎么让孩子更坚强，不哭鼻子
宣传我党相关知识。
请问学校后门什么时候可以开放呢？
让孩子跟着党走，了解中国共产党的历史。
怎样让孩子建立优秀的习惯，树立学习信心
孩子自觉性养成
专注力
无意义的活动甚多。还是要结合中国大中小考特色，结合小学生能吸收的程度安排每项活动。
家长自我成长，身教，激励孩子开启内驱力
如何教育孩子，处理孩子情绪，正确陪伴孩子学习成长
如何给老师沟通孩子学习情况，和老师一起纠正孩子学习习惯
学生徐海涛性格内向，缺少了同龄孩子的自信和活跃，尤其在同伴中间，融入度不够，家长很焦虑。请学校在这方面温暖关怀，多观察并正向鼓励孩子。我们家长也在通过家庭教育方面投入精力帮助他健康成长。谢谢。
孩子是鲁能巴蜀小学4年级11班的李映熹，专注力不足，上课走神。孩子智力和逻辑思维都很好。书写困难写字慢，家庭作业要一直守到做，也要做到晚上10点多，阅读困难认字认得少，对阅读识字有抵触，学过的字有时也不认识，读题就很困难，语文考试只能做两三道大题。去专注力训练培训了，收效甚微。不知道怎么办？
孩子成绩中等，家长如何调整心态
家校共同促进孩子学习
党建工作培训提升
党建工作提升培训"""


def main():
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print(result.decode('utf-8'))
    return


if __name__ == '__main__':
    main()
