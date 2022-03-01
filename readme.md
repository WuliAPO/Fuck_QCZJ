# 青春浙江-青年大学习打卡以及自动学习

## 快速使用

1、编辑mian.py 
```bash
nid = "" #在这里输入你的团组织编号，形如N003************，请使用抓包软件获取
cardNo = ""# 在这里输入你打卡时用的昵称，可能是学号，可能是姓名
openid = "" #靠自己抓包
nickname = "" #一般是微信账户名
```
将以上内容填进mian.py中

2、运行main.py
```bash
python3 main.py
```
其中python解释器的路径需根据自身情况设置

## 服务器端运行（推荐）
1、编辑mian.py

2、添加crontab，并保存运行结果
```bash
25 6 * * * [python interpreter path] [source root path] >> [log location] 2>&1
# eg： 25 6 * * * usr/local/bin/python3 ~/programs/QCZJ-Auotstudy-master/main.py >> ~/programs/QCZJ-Auotstudy-master/log.txt 2>&1
```
将以上内容填进crontab中即可。

## To Do
- [ ] 完善日志
- [ ] 重构代码
- [ ] 增加推送功能
- [ ] 针对网络问题优化
