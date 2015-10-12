import MySQLdb
import sys
import time as t
import calendar
conn1 = MySQLdb.connect (host = "127.0.0.1",
                        user = "",
                        passwd = "",
                        db = "")

conn = MySQLdb.connect (host = "",
                        user = "",
                        passwd = "",
                        db = "")
conn1.autocommit(1)


cursor = conn.cursor()
cursor1 = conn1.cursor()
#month = '05'
starttime = 01
#endtime = 22
year = 2014

for month in xrange(12,13):
    endtime = calendar.monthrange(year,month)[1]
    for each in xrange(starttime,endtime+1):
        eachtime = ('%.2d' % month) + ('%.2d' % each)
        startpoint =  str(year) + eachtime + '000000'
        endpoint = str(year) + eachtime + '235959'
        select_sql = "select room_id,user_count,msg_in_minute,item_in_minute,cashgift_in_minute,time,video_bandwidth from web_room_stat_old where time >= unix_timestamp(" + startpoint + ") and time <= unix_timestamp(" + endpoint + ')'
        cursor.execute (select_sql)
        values = []
        n = 0
        count_lines = cursor.rowcount
        while 1:
            try:
                room_id,user_count,msg_in_minute,item_in_minute,cashgift_in_minute,time,video_bandwidth = cursor.fetchone()
                #single_value = '(%s,%s,%s,%s,%s,%s,%s)' % (room_id,user_count,msg_in_minute,item_in_minute,cashgift_in_minute,time,video_bandwidth)
                #values += single_value + ','
                values.append([room_id,user_count,msg_in_minute,item_in_minute,cashgift_in_minute,time,video_bandwidth])
                n += 1
                sql = 'insert into web_room_stat values(%s,%s,%s,%s,%s,%s,%s)'
                if count_lines < 1000:
                    cursor1.executemany(sql,values)
                    count_lines -= 1
                    print 'inerted=',n,' count_lines=',count_lines, ' starttime=',startpoint ,' enditme=',endpoint
                    t.sleep(0.01)
                if not n % 1000:
                    cursor1.executemany(sql,values)
                    count_lines = count_lines - 1000
                    print 'inserted=',n,' count_lines=',count_lines, ' starttime=',startpoint ,' enditme=',endpoint
                    values = []
                    t.sleep(0.01)
                if count_lines == 0:
                    break
            except Exception,e:
                print e
                continue

cursor.close()
cursor1.close()

