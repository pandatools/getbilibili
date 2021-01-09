from translate import translate
import getdata
import requests
import json
class video():
    sockip = ['112.192.179.75:4258', '175.154.44.87:4258', '124.161.43.184:4258', '119.5.176.249:4258',
            '175.155.50.78:4258', '112.194.178.181:4258', '124.161.212.88:4258', '119.5.179.10:4258',
            '112.194.178.137:4258', '112.192.182.77:4258', '175.155.51.160:4258', '112.192.179.15:4258',
            '112.194.178.22:4258', '119.5.177.126:4258', '119.5.177.172:4258', '119.5.189.136:4258',
            '175.155.51.94:4258', '119.5.177.191:4258', '175.154.44.153:4258', '175.155.50.74:4258']

    av = ""                                                                                                                                                                                                                      ''
    bv = ""
    mid_reply = {}#每一句回复所对应的id
    def __init__(self,*args):
        for i in args:
            if i[0:2]=="BV":
                self.bv = i
            else:
                self.av = i
        if self.av!="" and self.bv =="":
                self.bv = translate().enc(self.av)

        if self.bv!="" and self.av =="":
                self.av = translate().dec(self.bv)


    def getav(self,av):
        self.av = av
        self.bv = translate().enc(self.av)

    def getbv(self,bv):
        self.bv = av
        self.av = translate().dec(self.bv)

    def putav(self):
        return self.av

    def putbv(self):
        return self.bv



    def check(self):
        if self.av =="":
            raise NameError("you should set av")
    def getbasic(self):
        self.check()
        answer = {}
        url = "http://api.bilibili.com/archive_stat/stat?aid="+self.av+"&type=jsonp"
        dict_json = getdata.getdict(url)
        print(dict_json)
        answer = dict_json["data"]
        if dict_json["code"] != 0:
            raise Exception("请求错误,请重新检查")
        url = "https://api.bilibili.com/x/web-interface/view?aid="+self.av# 关于视频类的,这段更重要,以后有需要,直接看这段就好
        dict_json = getdata.getdict(url)
        print("hhhhhhhhhhhhhhhhh")
        if dict_json["code"] != 0:
            # raise Exception("请求错误,请重新检查")
            print("youwentiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            answer["videos"] = []
            answer["tid"] = []
            answer["tname"] = []
            answer["copyright"] = []
            answer["title"] = []
            answer["desc"] = []  # 视频简介
        answer["videos"] = dict_json["data"]["videos"]
        answer["tid"] = dict_json["data"]["tid"]
        answer["tname"] = dict_json["data"]["tname"]
        answer["copyright"] = dict_json["data"]["copyright"]
        answer["title"] = dict_json["data"]["title"]
        answer["desc"] = dict_json["data"]["desc"] #视频简介
        return answer




    def getbasicinfo(self):
        params = {"aid":"av值","view":"播放量","danmaku":"弹幕量","reply":"回复数","favorite":"收藏数","coin":"硬币数","share":"分享数","like":"点赞数","copyright":"1自制2转载"}
        for key,value in params.items():
            print(key,"    ",value)

    def gettag(self):
        self.check()
        url = "http://api.bilibili.com/x/tag/archive/tags?aid="+self.av+"&jsonp=jsonp "
        dict_json = getdata.getdict(url)
        if dict_json["code"] != 0:
            raise Exception("请求错误,请重新检查")
        else:
            dictinfo = {}
            for i in dict_json["data"]:
                dictinfo[i["tag_name"]] = i["tag_id"]
            return dictinfo
    def gettaginfo(self):
        print("标签名称    标签id")

    def getdict(self,page,av,k):
        url = "http://api.bilibili.com/x/v2/reply?jsonp=jsonp&;pn="+page+"&type=1&oid="+av
        if k<0:
            p = requests.get(url)
            res_p = p.content.decode()
            return json.loads(res_p)
        elif k>=0 and k< self.sockip:
            proxies = {
                "http": self.sockip[k],
                "https": self.sockip[k],
            }
            p = requests.get(url)
            res_p = p.content.decode()
            return json.loads(res_p)
        else:
            raise Exception("超出list范围")

    def getreply(self,count):
        self.check()
        url ="http://api.bilibili.com/x/v2/reply?jsonp=jsonp&;pn=1"+"&type=1&oid="+self.av
        need = count
        times = 0
        num = 1
        flag = True
        answer = {}#{'来了来了': ['回复 @panda_face :df', '感谢老铁支持'], '想不出骚话': [], '百万后期，不得了': ['这么早就看了？？？']}
        id_answer = {}
        k = -1
        dict_json = self.getdict(str(num), self.av,k)
        while True:
            if dict_json["code"] != 0:
                k = k+1
                dict_json = self.getdict(str(num), self.av, k)
            else:
                break
        while  dict_json["data"]["replies"] != None and flag:
            for i in dict_json["data"]["replies"]:
                if i["content"]["message"] not in answer.keys():
                    answer[i["content"]["message"]] = []
                    id_answer[i["content"]["message"]] = []
                id_answer[i["content"]["message"]].append(i["mid"])
                if i["replies"] !=None:
                    for j  in i["replies"]:
                        answer[i["content"]["message"]].append(j["content"]["message"])
                times += 1
                if times == need:
                    flag =False
                    break
            # print("第"+str(num)+"页下载成功")
            num +=1
            dict_json = self.getdict(str(num), self.av,k)

        return answer

