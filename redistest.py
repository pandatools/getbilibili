import redis
import random
# 连接redis
# r = redis.StrictRedis(host='localhost',  # 主机ip
#                       port=6379,  # 端口
#                       db=0,  # 数据库索引
#                       password="",  # 密码
#                       decode_responses=True)  # 设置解码，因为使用get()方法获取出来的值是一个字节类型，这个设置为get()方法获取的值是字符串类型

# 使用连接池连接redis
def getredisconn():
    r = redis.StrictRedis(connection_pool=pool)
    return r
def getips(r=getredisconn()):
    key='proxies:universal'
    x=random.randint(0,800)
    ips=r.zrange(key,x,x+20)
    return ips
