import requests
'''
此文件用来解决循环引用的问题

'''

class func_res_test:#request 的返回值
    def __init__(self):
        pass
    def init_head(self,url,time,ip=""):
        if ip != "":
            proxies = {
                'http': 'http://' + ip,
                'https': 'https://' + ip,
            }
            response = None
            try:
                response = requests.get(url,proxies=proxies,timeout=time)
            except Exception as e:
                print(e)
            return response

        else:
            return requests.get(url,timeout=time)