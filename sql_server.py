import pymysql

from getconn import getconn


class MySql:
    def __init__(self):
        self.conn = getconn()
        self.rows = 0  # 修改行数
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql: str, args=None):
        self.rows = self.cursor.execute(sql, args)
        self.conn.commit()
        return self.rows

    def executemany(self, sql: str, data: list):
        self.rows = self.cursor.executemany(sql, data)
        self.conn.commit()
        return self.rows

    def fetch_one(self, sql: str, args=None):
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def fetch_all(self, sql: str, args=None):
        try:
            self.cursor.execute(sql, args)
        except:
            self.conn.rollback()
        return self.cursor.fetchall()

    def insert_ip(self,str_ip):
        sql = f'''insert into ip_pool values(null,"{str_ip}",NOW())'''
        self.execute(sql)
if __name__ == '__main__':
    sql1 = f'''select av from bvlist limit 0,10'''
    db = MySql()
    db.execute(sql1)
    res = db.fetch_all(sql1)
    # (('100027799',), ('10005970',), ('10007899',), ('10009228',), ('100104284',), ('10011216',), ('10011671',), ('100135713',), ('10014474',), ('100146984',))
    #((0,), (1299,), (1612,), (1769,), (1799,), (6255,), (44067,), (51749,), (54430,), (55173,))
    print(res)