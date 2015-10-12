# coding: utf-8
import MySQLdb
import time
import json

class CheckDB(object):
    def initdbconfig(self,dbhost,dbport,dbuser,dbpasswd):
        self.conn=MySQLdb.connect(user=dbuser, passwd=dbpasswd, host=dbhost , port=dbport)
        self.cursor = self.conn.cursor()

    def check_component_stats(self,delay_seconds):
        delay_unix_time = int(time.time()) - delay_seconds
        sql = self.cursor.execute("use stt_online")
        self.cursor.execute('SELECT * FROM stt_online.web_online_server where avtive_time < %d and server_id <> 8123 and server_id <> 28002' % delay_unix_time )
        self.result = self.cursor.fetchall()


    def data2json(self):
        if self.result:
            d = {}
            for each in self.result:
                server_name = each[3]
                server_id = int(each[0])
                server_ip = each[4]
                server_active_time = int(each[7])
                strftime = self.timestamp_datetime(server_active_time)
                d[server_name] = [server_ip,server_id,strftime]
            jsondata = json.dumps(d)
            return jsondata
        else:
            return

    def timestamp_datetime(self,value):
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt

if __name__ == '__main__':
    ckeckdb = CheckDB()
    ckeckdb.initdbconfig('192.168.4.81',11306,'vod_web','HVAGKKgRTT3SbpDmVzF5')
    ckeckdb.check_component_stats(90)
    result = ckeckdb.data2json()
    if result:
        print result
    else:
        print 1
