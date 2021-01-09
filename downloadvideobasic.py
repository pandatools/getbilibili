import json
import requests
import headers
import urllib.request
import random
from urllib.request import ProxyHandler,build_opener
import redistest

def getdict(url):
    header=headers.get_user_agent_pc()
    headers1 = {
        'User-Agent': header
    }
    # ips=redistest.getips()
    # ip1='http://'+random.choice(ips)
    # ip={'http':ip1}
    # request = urllib.request.Request(url, headers=headers1, method='GET')
    # proxy_handler = ProxyHandler(ip)
    # opener = build_opener(proxy_handler)
    # response = opener.open(request)
    # res_p=response.read().decode('utf-8')
    # return json.loads(res_p)
    # print(ip)
    p = requests.get(url,headers=headers1)
    res_p = p.content.decode()
    return json.loads(res_p)

def gettime(timeStamp,style="%Y--%m--%d %H:%M:%S"):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime(style, timeArray)
    return otherStyleTime