import json
import threading
import time

import requests

from reload.filter_ip import manage_ip
from reload.url_load import load_url
from sql_server import MySql


class func_res:#request 的返回值
    videoneed = ["created","length","is_union_video","typeid"]
    need = ["mid", "name", "sex", "sign", "level", "birthday", "coins", "following", "follower", "black"]
    def __init__(self):
        self.proxy = ""
        self.ip_pool=[]#用来放ip的


    # def starts(self,url):
    #     self.ip_manager = manage_ip()
    #     self.url = url
    #     if self.ip_manager.ip_pool != []:
    #         self.proxy =self.ip_manager.ip_pool.pop()
    def manager(self,name):
        self.load_url(name)#载入未成功的url
        for mid,url in self.urls:
            self.starts(url,3,mid,name)

    def manager_video(self,name):
        self.load_url(name)
        for av,url in self.urls:
            self.starts(url,3,av,name)

    def load_url(self,name):
        loads = load_url()
        self.urls = loads.load_manager(name)


    def starts(self,url,times,mid,name):
        print("dd")
        time2 = 0
        while True:
            self.response = self.init_head(url,times)
            if self.response ==None or self.response.status_code !=200:
                if self.ip_pool != []:
                    '''
                    用过的ip改变valid
                    '''
                    self.proxy=self.ip_pool.pop()
                    if len(self.ip_pool)<5:
                        '''
                        将ip加入
                        '''
                        pass
                else:
                    time2+=1
                    time.sleep(10)
            else:
                res = self.response.content.decode()
                res = json.loads(res)
                self.manager_deal_url(name,res,mid,url)
                break
            if time2>10:
                assert "数据库里没可用ip了，结束运行"
            print("等待下一次进入")
    def manager_deal_url(self,name,res,mid,url):
        if name== "load_url_1":
            self.deal_url_1_res(res,mid)
        elif name == "load_url_2":
            self.deal_url_2_res(res,mid)
        elif name == "load_url_3":
            self.deal_url_3_res(res,mid,url)
        elif name =="load_url_4":
            av = mid
            self.deal_url_4_res(res,av,url)
        elif name =="load_url_5":
            av = mid
            self.deal_url_5_res(res,av,url)
        else:
            assert "manager_deal_url name 错了"
    def deal_url_1_res(self,res,mid):
        info = {}
        for i, j in res["data"].items():
            if i in self.need:
                if j =="":
                    j = " "
                info[i] = j
        sql2 = f'''insert into upbasic values({info["mid"]},"{info["name"]}","{info["sex"]}","null",{info["level"]},"{info["birthday"]}",{info["coins"]},null,null,null)'''
        sql1 = f'''select mid from upbasic where mid = {mid}'''
        sql3 = f'''update baida_up set url_1_valid = 0 where mid = {mid}'''
        db = MySql()
        call = db.fetch_one(sql1)
        print(call)
        if call ==None:
            print(sql2)
            db.execute(sql2)
            db.execute(sql3)
        print("ok")

    def deal_url_2_res(self,res,mid):
        info = {}
        print("res",res)
        for i, j in res["data"].items():
            if i in self.need:
                if j =="":
                    j = " "
                info[i] = j
        sql2 = f'''update upbasic set following={info["following"]},black={info["black"]},follower={info["follower"]} where mid = {mid}'''
        sql3 = f'''update baida_up set url_2_valid = 0 where mid = {mid}'''
        db = MySql()
        print(sql2)
        db.execute(sql2)
        db.execute(sql3)
        print("ok")

    def deal_url_3_res(self,dict_json,mid,url):
        videolist=[]
        moreinfo = {}
        for i in dict_json["data"]["list"]["vlist"]:
            videolist.append(str(i["aid"]))
            moreinfo[str(i["aid"])] = {}
            for keyj, valuej in i.items():
                if keyj in self.videoneed:
                    moreinfo[str(i["aid"])][keyj] = valuej
        db = MySql()
        for i in videolist:
            sql_check = f'''select mid from bvlist where av = "{i}" '''
            res=db.execute(sql_check)
            print("res",res)
            if res == 0:
                sql = f'''Insert into bvlist values({mid},null,"{i}",1,{moreinfo[i]["typeid"]},{moreinfo[i]["created"]},"{moreinfo[i]["length"]}",{moreinfo[i]["is_union_video"]})'''#将信息插入bvlist
                print(sql)
                db.execute(sql)
        sql2 = f'''update getbvlist set valid=0 where url="{url}"'''
        db.execute(sql2)
        print("videolist",videolist)
        print("moreinfo",moreinfo)
    def deal_url_4_res(self,dict_json,av,url):
        print(av)
        if av ==0 or av==1299:
            return
        db = MySql()
        i = dict_json["data"]
        view = i["view"]
        if  isinstance(view,str):#用来处理视频不见了的状况
            view= -1
        danmaku = i["danmaku"]
        reply = i["reply"]
        favorite = i["favorite"]
        coin = i["coin"]
        share = i["share"]
        his_rank = i["his_rank"]
        like = i["like"]
        sql = f'''Update bvlist set view={view},danmaku={danmaku},reply={reply},favorite={favorite},coin={coin},share={share},his_rank={his_rank},likes={like} where av={av}'''
        print(sql)
        db.execute(sql)
        sql2 = f'''Update video_url set valid_1=0 where av={av}'''
        db.execute(sql2)

    def deal_url_5_res(self,dict_json,av,url):
        db = MySql()
        for i in dict_json["data"]:
            title = i[title]
            sql = f'''Update bvlist set title="{title} where av = {av}"'''
            db.execute(sql)
            sql2 = f'''Update video_url valid_2=0 where av={av}'''
            db.execute(sql2)



    def init_head(self,url,time):
        if self.proxy != "":
            proxies = {
                'http': 'http://' + self.proxy,
                'https': 'https://' + self.proxy,
            }
            response = None
            try:
                response = requests.get(url,proxies=proxies,timeout=time)
            except Exception as e:
                print(e)
            return response

        else:
            return requests.get(url,timeout=time)


if __name__ == '__main__':
    p =func_res()
    p.manager_video("load_url_4")
## http://x.fanqieip.com/index.php?s=/Api/IpManager/adminFetchFreeIpRegionInfoList&uid=12522&ukey=caa11eef0b28fa88056de334a5c0c2e3&limit=10&format=0&page=1