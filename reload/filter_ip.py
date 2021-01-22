import json
import re
import threading
import time
import datetime
from reload.res_test import func_res_test
from sql_server import MySql


class manage_ip:
    ip_pool = []
    def __init__(self):
        self.find_store_ip = self.input_ip()#将ip载入
        self.starts()

    def starts(self):
        self.add_ip()
        t1 = threading.Thread(target= self.check)
        t1.start()

    def input_ip(self):
       return  find_store_ip()


    def check(self):#检查ip池的数据，如果小于5，那么立刻添加进入ip_pool，如果没有新的ip进来，就一直处于监听转台
        '''
        这里面需要完成如果ip池小于10，那么，不断补充新的ip，如果没有有效的ip，那么程序一直处于监听状态
        '''
        while(1):
            time.sleep(60)
            if len(self.ip_pool)<5:
                self.add_ip()




    def add_ip(self):#将ip添入ip_pool
        '''
        将代理ip添加入ip_pool
        :return:如果成功，返回true，否则，False
        '''
        print("正在添加~~~~~~")
        today = datetime.date.today()
        sql = f'''select ip from ip_pool where  valid=1  and date = "{today}"'''
        db = MySql()
        res = db.fetch_all(sql)
        print(type(res))
        if res != tuple():
            for i in res:
                self.ip_pool.append(i[0])
            print("添加成功")
            return True
        print("添加失败，数据库中没有合适的值")
        return False

    def update_valid(self,ip):#将valid变为0
        sql = f'''update  ip_pool set valid = 0   where ip="{ip}"'''
        db = MySql()
        res = db.execute(sql)
        print("delete ok")

    def delete_today(self):#将今天的数据全部删除
        sql = "Delete from ip_pool where 1=1"
        db = MySql()
        res = db.execute(sql)
        print("delete all ok")

            # self.ip_pool.extend(新的ip)
class find_store_ip:
    def __init__(self):
        self.res = func_res_test()
        self.starts()

    def starts(self):

        self.to_mange()
        t1= threading.Thread(target=self.listen_write)
        t1.start()
        print(">>")

    def ip_check(self, ip):
        '''
        :param :ip是测试ip
        :return: True为可用ip，False为不可用ip
        '''
        test_url = "https://api.bilibili.com/x/space/arc/search?mid=451618887&;pn=1&ps=100&jsonp=jsonp"
        response = self.res.init_head(test_url, time=3, ip=ip)
        if response == None:
            return False
        if response.status_code != 200:
            return False
        else:
            return True
    def listen_write(self):
        while(1):
            time.sleep(100)
            url = input("请输入获得ip的地址，如若想退出，请按quit")
            self.to_mange2(url)
            if url == "quit":
                break

    def to_mange(self):#控制各个小功能块
        url = input("请输入获得ip的地址")
        ip_item = self.get_ip(url)
        if ip_item!=None and ip_item !=[]  :
            for i in ip_item:
                if  self.ip_check(i):
                    self.ip_store(i)
            return False
        return True

    def to_mange2(self,url):#控制各个小功能块
        ip_item = self.get_ip(url)
        if ip_item!=None and ip_item !=[]  :
            for i in ip_item:
                if  self.ip_check(i):
                    self.ip_store(i)

    def get_ip(self,url):
        '''
        :param url: 获取代理api
        :return: 代理ip列表,如果无法连接，返回None，连接初见错误，返回[]，如果正常连接，返回response
        '''

        response = None
        try:
            response = self.res.init_head(url, time=4)
            if response.status_code != 200:
                print("url错误！！！")
                return []
            else:
                return self.get_ip_rules(response)
        except Exception as e:
            print(e)
            return response

    def get_ip_rules(self,response):#获得返回后，提取ip的规则
        '''
        :param response:
        :return:  list
        '''
        js = response.text
        print(re.findall(r'\d+.\d+.\d+.\d+:\d+', js))
        return re.findall(r'\d+.\d+.\d+.\d+:\d+', js)



    def ip_store(self,ip):
        db = MySql()
        sql = f'''insert into ip_pool values(null,'{ip}',NOW()，1)'''
        print(sql)
        db.execute(sql)



if __name__ == '__main__':
    # p = find_store_ip()
    p = manage_ip()
    # p.delete_today()
# http://x.fanqieip.com/index.php?s=/Api/IpManager/adminFetchFreeIpRegionInfoList&uid=12522&ukey=caa11eef0b28fa88056de334a5c0c2e3&limit=10&format=0&page=1