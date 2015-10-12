import MySQLdb

conn = MySQLdb.connect (host = "",
                        user = "",
                        passwd = "",
                        db = "")



cursor = conn.cursor()
cursor.execute ("select room_id,user_count,msg_in_minute,item_in_minute,time,video_bandwidth from web_room_stat where time > 3532275885")
n = 0
while n < 10:
    if cursor.fetchone() == None:
        break
    room_id,user_count,msg_in_minute,item_in_minute,time,video_bandwidth = cursor.fetchone()
    print room_id,user_count,msg_in_minute,item_in_minute,time,video_bandwidth
    #cursor.execute("insert into web_room_stat(%d,%d,%d,%d,%d,%d)" % (room_id,user_count,msg_in_minute,item_in_minute,time,video_bandwidth))
    n+=1