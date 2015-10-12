# -*- coding: gb18030 -*-
import easygui as g
import subprocess
import os
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

basestript_file = 'securecrt_connect_ssh2.py'
path = r'D:\pyproject\myproject'
stript_file = 'crtstript.py'

def setstript(hosts):
    basestript = os.path.join(path,basestript_file)
    striptfile =  os.path.join(path,stript_file)
    replace_line = 'hosts = ' + str(hosts) + '\n'
    with open(basestript,'r') as f:
        with open(striptfile,'w') as f1:
            for line in f:
                if 'hosts = []' in line:
                    line = replace_line
                f1.write(line)
    return striptfile


def get_db_result(*host):
    conn = MySQLdb.Connect(host='192.168.5.21',user='douyupa',passwd='123456',db='douyupa',charset='utf8')
    cursor = conn.cursor()
    if host:
        cursor.execute('select * from douyupa where ip="%s"' % host)
        result =  cursor.fetchone()
    else:
        cursor.execute('select * from douyupa')
        result = cursor.fetchall()
    return result


while 1:
    msg = '请选择服务器'
    title = '服务器列表'
    result = get_db_result()
    choies = [x[1] for x in result]
    choies_box = g.multchoicebox(msg,title,choies)
    hosts = []
    for host in choies_box:
        db_result = get_db_result(host)
        hosts.append(db_result)
    striptfile = setstript(hosts)
    p = subprocess.Popen(["F:\软件安装\SecureCRT\SecureCRT" , "/SCRIPT", striptfile], shell=True)
    if g.ccbox(msg,title):
        pass
    else:
        sys.exit(0)

