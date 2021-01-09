import pymysql
import logging
from sshtunnel import SSHTunnelForwarder
def getconn():
    # try:
    #     conn = pymysql.connect(db='bilibili', user='root', passwd='123456', host='localhost', port=int(3306),
    #                             charset="utf8")
    #     cursor = conn.cursor()
    #     return conn
    # except Exception as e:
    #     print(e)
    #     logging.error('数据库连接失败:%s' % e)

    # 通过SSH连接云服务器
    server = SSHTunnelForwarder(
        ssh_address_or_host=("8.131.82.204", 22),  # 云服务器地址IP和端口port
        ssh_username="root",  # 云服务器登录账号admin
        ssh_password="aqwsdeR1",  # 云服务器登录密码password
        remote_bind_address=('localhost', 3306)  # 数据库服务地址ip,一般为localhost和端口port，一般为3306
    )
    # 云服务器开启
    server.start()
    # 云服务器上mysql数据库连接
    con = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                          port=server.local_bind_port,
                          user="root",  # mysql的登录账号admin
                          password="123456",  # mysql的登录密码pwd
                          db="bilibili",  # mysql中要访问的数据表
                          charset='utf8')  # 表的字符集
    return con;