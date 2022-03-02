# Copyright 2022.1 by WuliAPO
# Copyright © cjlu.online . All rights reserved.

# modified by @Dimlitter 2022/3/1 
# personal profile: https://github.com/Dimlitter

import json
import random
import time
import requests
import datetime

class QCZJ_Youth_Learning:
    def __init__(self,nid,cardNo,openid,nickname):
        self.nid = nid
        self.cardNo = cardNo
        self.openid = openid
        self.nickname = nickname

        self.sleep_time = random.randint(5,10)

        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3185 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/4365 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    #获取AccessToken
    def getAccessToken(self,session,openid,nickname):
        time_stamp = str(int(time.time()))#获取时间戳
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid="+openid+"&nickname="+ nickname +"&headimg=&time="+time_stamp+"&source=common&sign=&t="+time_stamp
        res = session.get(url)
        access_token = res.text[45:81]#比较懒，直接截取字符串了     
        print("获取到AccessToken:",access_token)
        return access_token

    #获取当前最新的课程代号
    def getCurrentCourse(self,session,access_token):
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current?accessToken="+access_token
        res = session.get(url)
        res_json = json.loads(res.text)
        if(res_json["status"]==200):#验证正常
            print("获取到最新课程代号:", res_json["result"]["id"])
            return res_json["result"]["id"]
        else:
            print("获取最新课程失败！退出程序")
            print(res.text)
            exit(0)

    #签到 并获取签到记录
    def getJoin(self,session,access_token,current_course,nid,cardNo):
        data = {
                "course": current_course,# 大学习期次的代码，如C0046，本脚本已经帮你获取啦
                "subOrg": None,
                "nid": nid, # 团组织编号，形如N003************
                "cardNo": cardNo # 打卡昵称
            }
        url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join?accessToken="+access_token
        res = session.post(url,json=data) #特别注意，此处应选择json格式发送data数据
        print("签到结果:",res.text)
        res_json = json.loads(res.text)
        if(res_json["status"]==200):#验证正常
            print("似乎签到成功了")
            return True
        else:
            print("签到失败！")
            exit(0)

    def check(self,session,access_token):
        url = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/sign-in?accessToken='+access_token
        data = {
            #'accessToken': access_token,
        }
        try:
            res = session.post(url,json = data)
        except :
            print("网络错误，请检查网络")
            print("尝试重新签到，等待15s")
            time.sleep(15)
            try:
                res = session.post(url,json = data)
            except :
                print("签到失败！")
                return False
        res = json.loads(res.text)
        if res["status"]==200:
            print("访问成功")
            if res['result'] == False:
                print("今天已经签到过了")
            else:
                print("今天签到成功！")
        else:
            print("访问失败")

        url2 = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/sign-in/records?accessToken=' + access_token + '&date=' + datetime.datetime.now().strftime('%Y-%m')
        res2 = session.get(url2)
        if res2.status_code == 200:
            print("签到记录存在！")
            print(res2.text)
        else:
            print("签到记录失败")

    def read(self,session,access_token):
        session.headers.update({
            'Referer': 'https://qczj.h5yunban.com/qczj-youth-learning/learn.php',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=UTF-8',
            'Content-Length': '2',
            'Origin': 'https://qczj.h5yunban.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        numbers = [random.randint(470017, 470026) for i in range(4)]
        for number in numbers:
            number = str(number)
            url = 'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/study?accessToken='+access_token+'&id='+ 'C00'+ number
            time.sleep(8)
            #传的data居然是空的
            data = {
                #'accessToken': access_token,
                #'id': 'C00'+ number,
            }
            try:
                res = session.post(url,json = data).json()
                if res['status'] == 200:
                    print("文章"+'C00'+ number +"学习成功")
                    print(res)
                else:
                    print("文章"+'C00'+ number +"学习失败")
                    print(res)
            except:
                print("网络错误，尝试重新学习，等待15s")
                time.sleep(15)
                try:
                    res = session.post(url,json = data).json()
                    if res['status'] == 200:
                        print("文章"+'C00'+ number +"重新学习成功")
                except:
                    print("重新学习失败，退出")
                    break

    def main(self):
        session = requests.session()
        session.headers = self.headers
        time.sleep(self.sleep_time)
        access_token = self.getAccessToken(session,self.openid,self.nickname)

        time.sleep(self.sleep_time)
        current_course = self.getCurrentCourse(session, access_token)

        #添加随机执行
        sequence = [1,2,3]
        random.shuffle(sequence)
        order = {1:'看视频',2:'签到',3:'阅读文章'}
        result = ''
        for i in sequence:
            result = result + order[i] + '------>'
        print("本次学习的顺序为：",result,"完成")

        for i in sequence:
            if i == 1:  #看视频
                time.sleep(self.sleep_time)
                if datetime.datetime.now().weekday == '1':
                    time.sleep(self.sleep_time)
                    self.getJoin(session,access_token,current_course,nid,cardNo)
                else:
                    print("今天不是周一，不看视频")
            if i == 2:    #签到
                time.sleep(self.sleep_time)
                self.check(session,access_token)
            if i == 3:   #阅读
                time.sleep(self.sleep_time)
                self.read(session,access_token)

if __name__ == '__main__':

    nid = "" # 在这里输入你的团组织编号，形如N003************，请使用抓包软件获取
    cardNo = ""# 在这里输入你打卡时用的昵称，可能是学号，可能是姓名
    openid = "" #靠自己抓包
    nickname = "" #一般是微信账户名

    qndxx = QCZJ_Youth_Learning(nid,cardNo,openid,nickname)
    qndxx.main()

