#coding: utf-8
import time
import urllib,urllib2
import sys
from refresh_config import host_list


random_segment =  '%d' % time.time()




if __name__ == '__main__':
    for ip in host_list :
        url_plist = '%s%s%s' % ('https://',ip,'/purge/douyutvalllive.plist')
        url_ipa =  '%s%s%s' % ('https://',ip,'/purge/douyutvalllive.ipa')
        request_plist = urllib2.Request(url_plist,headers={"Host" : "ssl.douyutv.com"})
        request_ipa = urllib2.Request(url_ipa,headers={"Host" : "ssl.douyutv.com"})
        try:
            urllib2.urlopen(request_plist)
            urllib2.urlopen(request_ipa)
            print  'host:%s clear caches success !' % ip
        except:
            print 'host:%s caches was cleared ,passed !' % ip
