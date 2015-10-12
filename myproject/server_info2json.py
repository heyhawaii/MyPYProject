import MySQLdb
import re
import json

# {
#    "ServerInfos" : [
#       {
#          "ServerID" : 4,
#          "ServerIP" : "192.168.5.14",
#          "ServerName" : "MsgServer",
#          "ServerPort" : 11004
#       },
#       {
#          "ServerID" : 3,
#          "ServerIP" : "192.168.5.14",
#          "ServerName" : "MsgServer",
#          "ServerPort" : 11003
#       }
#    ]
# }



conn = MySQLdb.connect (host = "",
                        user = "",
                        passwd = "",
                        db = "")


select_sql = "select server_id,server_type,server_name,server_region,ip,port,ipv6 from web_server_info"
cursor = conn.cursor()
cursor.execute (select_sql)
result = cursor.fetchall()
d= {}
d['ServerInfos'] = []
for x in result :
    server_id,server_type,server_name,server_region,ip,port,ipv6 = x
    d1 = {}
    d1['ServerID'] = server_id
    d1['ServerIP'] = ip
    d1['ServerName'] = server_name
    d1['ServerPort'] = port
    d['ServerInfos'].append(d1)
