# coding: utf-8
import os
import hashlib
import memcache
import json

from socket import socket, SOCK_DGRAM, AF_INET
bash_path = '/home/www/server/www.douyutv.com'
clude_path = [ os.path.join(bash_path,'app'),
               os.path.join(bash_path,'sys'),
]
exclude_path = [os.path.join(bash_path,'root'),
                os.path.join(bash_path,'app/cache'),
                os.path.join(bash_path,'app/logs')
                ]

class WalkPath(object):
    def __init__(self,path):
        self.path = path
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('192.168.4.1', 0))
        self.local_ip = s.getsockname()[0]

    #type为file时返回所有文件，type为dir时返回所有子目录
    def getfilesordir(self,type,*exclude_path):
        def compare_path(source_path,dst_path):
            mark = True
            for path in source_path:
                if path in dst_path:
                    mark = False
            if mark:
                return True

        self.result = []
        for clude_dir in self.path:
            for base_dir,chird_dir,files in os.walk(clude_dir):
                if exclude_path:
                    if type == 'dir':
                        self.result.append(base_dir)
                    elif type == 'file':
                        for file in files:
                            if compare_path(exclude_path[0],base_dir):
                                self.result.append(os.path.join(base_dir,file))
                #单独加入root下的index.php
        self.result.append('/home/www/server/www.douyutv.com/root/index.php')
        return self.result



    def filemd5(self,*files):
        file_md5 = {}
        if not files:
            files = self.result
        for file in files:
            md5 = hashlib.md5(open(file,'rb').read()).hexdigest()
            file_md5[file] = md5
        return file_md5

    def writememcache(self,memcachedaddr,jsondata):
        mc = memcache.Client([memcachedaddr],debug=0)
        mc.set(self.local_ip,jsondata)


if __name__ == '__main__':
    phpfile2json = WalkPath(clude_path)
    phpfile2json.getfilesordir('file',exclude_path)
    data = phpfile2json.filemd5()
    jsondata = json.dumps(data)
    phpfile2json.writememcache('192.168.4.92:33211',jsondata)
