import requests
import json
import csv
import time
import random
import execjs

f = open(r"sign.js", 'r', encoding='UTF-8')
line = f.readline()
htmlstr = ''
while line:
    htmlstr = htmlstr + line
    line = f.readline()
ctx = execjs.compile(htmlstr)

def saveContent(data,fileName):
    for d in data:
        title = d["title"]
        comment_count = d["comments_count"]
        create_time = d["behot_time"]
        play_effective_count = str(d["detail_play_effective_count"])
        source_url = "https://www.toutiao.com"+str(d["source_url"])
        file = open(fileName+".csv", "a", encoding="utf-8", newline='')
        writer = csv.writer(file)
        writer.writerow([title, play_effective_count, comment_count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(create_time)), source_url])
        file.close()

def getHeader(uid,cookie,path):
    header = {
        "accept": "application/json, text/javascript",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": cookie,
        "referer": "https://www.toutiao.com/c/user/%s/" %(uid),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "x-requested-with": "XMLHttpRequest",
    }
    return header

def getUrl(uid, max_behot_time):
    Honey = json.loads(ctx.call('get_as_cp_signature', uid, max_behot_time))
    a = Honey['as']
    c = Honey['cp']
    signature = Honey['_signature']
    url = "https://www.toutiao.com/c/user/article/?page_type=0&user_id=%s&max_behot_time=%s&count=20&as=%s&cp=%s&_signature=%s" %(uid,max_behot_time,a,c,signature)
    return url


def mainProcess(name, uid ,mid):
    print("开始爬取：", name)
    file = open(name+".csv", "w", encoding="utf-8",newline='')
    writer = csv.writer(file)
    writer.writerow(["标题", "播放量", "评论数", "发布时间", "播放地址"])
    file.close()
    max_behot_time = 0
    cookie = ""
    old_max_behot_time = 0
    while(True):
        url = getUrl(uid, max_behot_time)
        path = url[23:]
        response = requests.get(url, headers=getHeader(uid, cookie, path))
        content = response.text
        try:
            cookie = response.headers["set-cookie"]
            cookie = str(cookie).split(";")[0]
        except:
            cookie = cookie
        result = json.loads(content)
        time.sleep(random.randint(0,3))
        try:
            nextValue = result["next"]
            max_behot_time = nextValue["max_behot_time"]
            if old_max_behot_time == max_behot_time:
                break
            data = result["data"]
            saveContent(data, name)
            old_max_behot_time = max_behot_time
        except:
            continue
    return 0


idFile = open("id.txt", "r", encoding="utf-8")

for id in idFile.readlines():
    finish = open("finish.txt", "r", encoding="utf-8")
    s = set()
    for line in finish.readlines():
        if line.isspace() or len(line) == 0:
            continue
        line = line[:len(line)-1]
        line = line.split(" ")
        s.add(line[1])
    finish.close()
    finish = open("finish.txt", "a", encoding="utf-8")
    id.replace("\n","")
    ids = id.split(" ")
    if ids[1] not in s:
        result = mainProcess(ids[0], ids[1],ids[2].replace("\n",""))
        if result==0:
            finish.write(id+"\n")
    finish.close()
print("success")