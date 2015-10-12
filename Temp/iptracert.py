#coding: utf-8
import hashlib
import json
import urllib,urllib2
import time
import re
import sys
import xlrd

reload(sys)
sys.setdefaultencoding('utf8')

excel_file = r'C:\Users\Administrator\Desktop\OnLineTest.xls'

def getlocaltion(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php'
    values = { 'ip':ip
    #          'json':'',
    #          'level':'3'
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = response.read()
    json_data =  json.loads(result)
    localtion_info = json_data['data']['country'] + ' -- ' +  json_data['data']['region'] + ' -- ' +  json_data['data']['city']  + ' -- ' +  json_data['data']['county']  + ' -- ' +  json_data['data']['isp']
    print localtion_info
    return localtion_info



def tracertiplist(excel_file):

    excel_data =  xlrd.open_workbook(excel_file)
    table = excel_data.sheets()[0]
    d = {}
    for i in xrange(3, table.nrows):
        ip_path = table.row(i)[9].value.split('|')
        id = table.row(i)[0].value
        d[id] = ip_path

    return d


if __name__ == '__main__':
    f = open(r'C:\Users\Administrator\Desktop\mobileTest.txt','w')
    iplist = tracertiplist(excel_file)
    for id,ips in iplist.items():
        for ip in ips :
            try:
                f.write("%s  %s  %s" % (id,ip, getlocaltion(ip)))
                f.write('\r\n')
                time.sleep(0.3)
            except Exception,e:
                print e
        f.write('\r\n')
        f.write('-' * 30)
        f.write('\r\n')

    f.close
    print "Finish"