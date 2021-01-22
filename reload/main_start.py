import random
import threading
from queue import Queue

import requests

from reload.func_request import func_res
from sql_server import MySql


class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, idQueue):
        # 继承父类的方法
        super(ThreadCrawl, self).__init__()
        self.idQueue =idQueue
        self.threadName = threadName          # 线程名字
    def run(self):
        print('启动' + self.threadName)
        while not self.idQueue.empty():
            try:
                id = self.idQueue.get(False)  # False 如果队列为空，抛出异常
                print("~~~~run~~~")
                self.get_con(id,self.threadName)

            except Exception as e:
                print('队列为空。。。。。', e)
                pass

    def get_con(self,id,name):  #自己封装的请求自定义
        print("request ",id,name)

class main_manager:
    url_item=[]
    def __init__(self):
        self.get_res()#获得请求对象
        self.load_url_1()

    def get_res(self):
        self.res =func_res()

    def load_url_1(self):
        db = MySql()
        sql = "select url_1 from baida_up where url_1_valid=1"
        res = db.fetch_all(sql)
        for i in res:
            self.url_item.append(i[0])

def get_id(m, n):

    data = [[random.randint(0,100)] for _ in range(6)]
    res = requests.get("http://www.baidu.com")
    print(res.status_code)
    return data
def main():
    n = 0
    while True:
        m = 1
        # m是固定值，一次去20条， n是第几条开始
        print('开始采集n的值为', n)
        if n > 300:
            break

        # id的队列
        idQueue = Queue(20)
        if idQueue.empty():
            data = get_id(m, n)
            for i in data:
                idQueue.put(i[0])

        #　采集线程的数量
        crawlList = []
        for id in range(1, 2):
            name = '采集线程{}'.format(id)
            crawlList.append(name)

        # 存储采集线程的列表集合
        threadcrawl = []
        for threadName in crawlList:
            thread = ThreadCrawl(threadName, idQueue)
            thread.start()
            threadcrawl.append(thread)

        for thread in threadcrawl:#阻塞调用线程，知道所有全部被处理掉
            thread.join()
        n = n + m
    print("主线程退出..............")
if __name__ == '__main__':
    mains = main_manager()
    print(mains.url_item)
