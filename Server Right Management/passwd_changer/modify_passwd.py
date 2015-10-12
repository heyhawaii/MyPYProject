# conding: utf-8
#服务器端每5分钟更改密码，申请的时候管理服务器从服务器端获取token（time + something）
#服务器端主动上报token至集中管理服务器并记录，每台服务器记录一条，每次都修改上一次的记录，当服务器端更改密码的程序出故障时，使用数据库记录的最后一次token
#平台登录申请使用google authenticator加password认证
import  time
import logging
import socket
import MySQLdb


class PWDManager(object):
    def __init__(self):
        self.hostname = socket.gethostname()

    def tokengenerate(self):
        t = time.time()
        token_unix_time = int(t) / 300
        return token_unix_time


    def modifypwd(self):
        pass

    def reporter(self):
        pass

    def tokensockserver(self):
        pass

    def logwriter(self):
        pass



