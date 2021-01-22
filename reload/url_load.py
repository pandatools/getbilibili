import json

import requests

from sql_server import MySql


class load_url:
    def __init__(self):
        pass
    def setmid(self,mid):
        self.mid = mid

    def load_mid(self,limit):
        '''

        :param limit: limit是要查询的是哪个有效的url种类
        :return: 返回的是dict
        '''
        db = MySql()
        sql= f"select mid from baida_up where {limit} = 1"
        res = db.fetch_all(sql)
        return res
    def load_mid_without_limit(self):
        '''

        :param limit: limit是要查询的是哪个有效的url种类
        :return: 返回的是dict
        '''
        db = MySql()
        sql= f"select mid from baida_up"
        res = db.fetch_all(sql)
        return res
    def load_av(self):
        db = MySql()
        sql = f'''select av from bvlist'''
        res = db.fetch_all(sql)
        return res
    def load_manager(self,name):
        if name =="load_url_1":
            return self.load_url_1()
        elif name =="load_url_2":
            return self.load_url_2()
        elif name =="load_url_3":
            return self.load_url_3()
        elif name == "load_url_4":
            return self.load_url_4()
        elif name == "load_url_5":
            return self.load_url_5()
        else:
            assert "load_manager name is wrong"

    def load_url_1(self):
        '''

        :return: mid,url_1
        '''
        sql ="select mid,url_1 from baida_up where url_1_valid=1 "
        db =MySql()
        res = db.fetch_all(sql)
        info = []
        for i in res:
            pair = []
            pair.append(i[0])
            pair.append(i[1])
            info.append(pair)
        return  info
    def load_url_2(self):
        sql = "select mid,url_2 from baida_up where url_2_valid=1"
        db = MySql()
        res = db.fetch_all(sql)
        info = []
        for i in res:
            pair = []
            pair.append(i[0])
            pair.append(i[1])
            info.append(pair)
        print(info)
        return info

    def load_url_3(self):
        sql="select mid,url from getbvlist where valid=1"
        db = MySql()
        res = db.fetch_all(sql)
        info = []
        for i in res:
            pair = []
            pair.append(i[0])
            pair.append(i[1])
            info.append(pair)
        return info

    def input_url3(self):
        loads = self.load_mid_without_limit()
        db =MySql()
        for i in loads:
            pn=1
            mid =i[0]
            sql1 = f'''select sum from getbvlist where mid={mid}'''
            res=int(db.fetch_one(sql1)[0])
            while(res>0):
                res = res-100
                pn+=1
                url= self.format_url_3(mid,pn)
                sql=f'''Insert Into getbvlist values({mid},"{url}",1,{res})'''
                print(sql)
                db.execute(sql)
            print(mid)
    def load_url_4(self):
        sql = "select av,url_1 from video_url where valid_1 =1"
        db = MySql()
        res = db.fetch_all(sql)
        info = []
        for i in res:
            pair = []
            pair.append(i[0])
            pair.append(i[1])
            info.append(pair)
        return info

    def load_url_5(self):
        sql = "select av,url_2 from video_url where valid_2 =1"
        db = MySql()
        res = db.fetch_all(sql)
        info = []
        for i in res:
            pair = []
            pair.append(i[0])
            pair.append(i[1])
            info.append(pair)
        return info


    # def getsum_url3(self,mid):#这个用一次就没用了
    #     url = self.get_url3(1,mid)
    #     response = requests.get(url)
    #     res_p = response.content.decode()
    #     dict_json = json.loads(res_p)
    #     jsgood=json.dumps(dict_json["data"]["list"],indent=1,ensure_ascii=False)
    #     sumcount = 0
    #     videotype = dict_json["data"]["list"]["tlist"]
    #     for key,value in videotype.items():
    #         sumcount += value["count"]
    #     db = MySql()
    #     sql =f'''Insert Into getbvlist values({mid},"{url}",1,{sumcount})'''
    #     print(sql)
    #     db.execute(sql)
    # def get_url3(self,pn,mid):
    #     return "https://api.bilibili.com/x/space/arc/search?mid=" + str(mid) + "&;pn="+str(pn)+"&ps=100&jsonp=jsonp"

    def format_sql_url_1(self,mid):
        url ="https://api.bilibili.com/x/space/acc/info?mid="+str(mid)+"&jsonp=jsonp"
        sql= f'''Update baida_up set url_1 = "{url}" where mid={mid};'''
        return sql

    def format_sql_url_2(self,mid):
        url = "https://api.bilibili.com/x/relation/stat?vmid=" + str(mid) + "&jsonp=jsonp"  # 2
        sql = f'''Update baida_up set url_2 = "{url}" where mid={mid};'''
        return sql

    def format_url_3(self,mid,pn):
        url = "https://api.bilibili.com/x/space/arc/search?mid=" + str(mid) + "&;pn="+str(pn)+"&ps=100&jsonp=jsonp"
        return url
    def format_url4_and_url5(self,av):
        url1 =  "http://api.bilibili.com/archive_stat/stat?aid=" + str(av) + "&type=jsonp"
        url2 = "https://api.bilibili.com/x/web-interface/view?aid="+str(av)
        sql = f'''insert into video_url values({av},"{url1}",1,"{url2}",1)'''
        return sql

    def build_urls_1(self):
        '''

        :return: 还需要请求的url
        '''
        strs = []
        mid = self.load_mid("url_1_valid")
        for i in mid:
            strs.append(self.format_sql_url_1(str(i[0])))
        return strs

    def build_urls_2(self):
        strs=[]
        mid = self.load_mid("url_2_valid")
        for i in mid:
            strs.append(self.format_sql_url_2(str(i[0])))
        return strs
    def build_url4_and_url5(self):
        strs = []
        load = self.load_av()
        for i in load:
            strs.append(self.format_url4_and_url5(str(i[0])))
        return strs

    def execute_many(self,name):#将url初始化进入数据库
        db = MySql()
        sql = []
        if name=="build_urls_1":
            sql =self.build_urls_1()
        elif name =="build_urls_2":
            sql = self.build_urls_2()
        elif name =="build_url4_and_url5":
            sql = self.build_url4_and_url5()
        else:
            assert "excute_many name is wrong"
        for i in sql:
            print(i)
            db.execute(i)
        print("ok")


if __name__ == '__main__':
    p= load_url()
    p.execute_many("build_url4_and_url5")
    # print(len(res))

