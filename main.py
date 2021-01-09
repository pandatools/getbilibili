from Up import Person
from getconn import getconn
from video import video
import logging
from Up import up
import re
import time
uplist=list(map(str,[39180492,382666849]))
conn = getconn()
# 爬取up基本信息
time1 = 0
for uid in uplist:

    per = Person(uid)
    basic = per.getbasic()
    print(time1,basic["name"] )
    keys = ','.join(basic.keys())
    values = list(basic.values())
    try:
        cursor = conn.cursor()
        # sql="insert into upbasic({keys})values({a1},{a2},{a3},{a4},{a5},{a6},{a7},{a8},{a9},{a10})".format(keys=keys,a1=values[0],a2=values[1],a3=values[2],a4=5,a5=values[4],a6=values[5],a7=values[6],a8=values[7],a9=values[8],a10=values[9])
        sql = "insert into upbasic(mid,name,sex,sign,level,birthday,coins,following,black,follower)values('%d','%s','%s','%s','%d','%s','%d','%d','%d','%d')" % (
            values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9])
        cursor.execute(sql)
        conn.commit()
        print("up基本信息爬取成功！！！！")
    except Exception as e:
        print(e)

    # 爬取up视频列表


    u = up(uid)
    videos = list(set(u.getvideos()))
    videos = ';'.join(videos)
    try:
        cursor = conn.cursor()
        sql = "insert into bvlist(UID,BVlist)values('%s','%s')" % (uid, videos)
        cursor.execute(sql)
        conn.commit()
        print('up视频列表爬取成功！！！！')
    except Exception as e:
        print(e)
    listvideo=list(set(u.getvideos()))

    # 爬取视频基本信息
    for av in listvideo:
        av1=video(av)
        bv = av1.putbv()
        videos = video(bv)
        # print(video.getbasic())
        basic = videos.getbasic()
        # print(basic.keys())
        # print(basic.values())
        # for i in basic.values():
        #     print(type(i))
        videolist = u.moreinfo
        last = videolist[int(av)]
        typeid_union = list(last.values())#获取除video以外的视频信息
        values = list(basic.values())
        print(values)
        values.extend(typeid_union)
        try:
            cursor = conn.cursor()
            sql = "insert into videobasic(aid,`view`,danmaku,reply,favorite,coin,`share`,now_rank,his_rank,`like`,dislike,no_reprint,copyright,videos,tid,tname,title,`desc`,typeid,created,length,is_union_video)" \
                  "values('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%s','%s','%s','%d','%d','%s','%d')" \
                  % (
                      values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8],
                      values[9],
                      values[10], values[11], values[12], values[13], values[14], values[15], values[16], values[17],
                      values[18],
                      values[19], values[20], values[21])
            sql = sql.replace('\n', '')
            cursor.execute(sql)
            conn.commit()
            print(bv + "视频基本信息爬取成功")
        except Exception as e:
            print(e)

        #爬取视频评论
        try:
            reply=';'.join(videos.getreply(100))
            res=re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^;]")
            reply=res.sub('',reply)
        except Exception as e:
            print(e)
        try:
            cursor=conn.cursor()
            sql="insert into comments(BV,comment)values('%s','%s')"%(bv,reply)
            cursor.execute(sql)
            conn.commit()
            print(bv+"视频评论爬取成功！！！！")
        except Exception as e:
            print(e)