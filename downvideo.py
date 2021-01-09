from Up import up
from getconn import getconn
import logging
conn=getconn()
uid='451618887'
u=up(uid)
videos=u.getvideos()
print(videos)
print(type(videos))

# videos=';'.join(videos)
# cursor=conn.cursor()
# sql="insert into BVlist(UID,BVlist)values('%s','%s')"%(uid,videos)
# cursor.execute(sql)
# conn.commit()
