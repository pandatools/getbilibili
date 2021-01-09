# import requests
import pymysql
class ip_pool():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="bilibili",
        charset="utf8")
    def __init__(self):
        db