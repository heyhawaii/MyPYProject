#coding: utf-8
import hashlib
import urllib,urllib2
import time
import sys
from msmsender_config import  *
reload(sys)
sys.setdefaultencoding('utf8')



sms_content = {
'phonenum' : '18086669830',
'smsid' : '14126' ,         #短信模版id
# 'smsv1': urllib.quote('for test'),               #短信内容
'smsv1': urllib.quote_plus('今天 天气 不错'),
'smsv2' : str('%d' % time.time())           #unix时间戳

}



def sortandhashed(dict):
    content = ''
    sortcontent = sorted(dict.iteritems(), key=lambda d:d[0])
    for each in sortcontent:
        content += '%s=%s&' % (each[0],each[1])
    content = content[:-1] + auth_key
    content_bashed = hashlib.md5(content).hexdigest()
    return content_bashed

def encodeurl(dict):
    data = ''
    for k,v in sms_content.items():
        data += '%s=%s%s' % (k,v,'&')
    return data

sms_content['auth'] = sortandhashed(sms_content)
data = encodeurl(sms_content)
starttime = time.time()
response = urllib2.urlopen('%s?%s' % (baseurl,data))
endtime = time.time()

print response.read()
print endtime - starttime

