import requests
class ChatingError(Exception):
    pass
def chat(question):
    #反反爬的请求头
    headers={
        'Host': 'biz.turingos.cn',
        'Content-Length': '73',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://biz.turingos.cn',
        'Referer': 'http://biz.turingos.cn/chat',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'UM_distinctid=16cc3e0e4d378b-0c68c2ff491139-7373e61-100200-16cc3e0e4d462d; CNZZDATA1267359368=1777192915-1566654395-null%7C1581833892',
        'Connection': 'keep-alive'
    }
    #Cookie,UA,X-Requested-With,Origin,Referer,Host不能删，其他的随便删
    
    data={"deviceId":"00730073-0073-0073-0073-007300730073","question":question}
    #deviceId不要删，这是反爬判断之一
    
    url="http://biz.turingos.cn/apirobot/dialog/homepage/chat"
    r=requests.post(url,headers=headers,data=data)
    j=r.json()["data"]

    #请求错误
    if r.json()["code"]!=10000:
        raise ChatingError("Response Error:[%s]%s"%(r.json()["code"],r.json()["content"]))

    #带音乐
    if j["intent"]["code"] in [200101,200201,200301,200302,200303]:
        return {"text":j["results"][0]["values"]["text"],"music":j["results"][1]["values"]["voice"]}
    #纯文字
    elif j["intent"]["code"] in [201401,10002,200209,10005,200207,200212,100000,201711,200702,
                                 201204,201501,200205,200401,900101]:
        return {"text":j["results"][0]["values"]["text"]}
    #无法识别的类别
    else:
        return {"text":"Unknown return type","data":j}
