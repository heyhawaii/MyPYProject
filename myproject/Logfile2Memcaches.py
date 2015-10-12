#coding: utf-8
import memcache
import os

class Log2Memached(object):
    def __init__(self):
        self.rooms_path = '/home/room/server'

    def logfilename(self):
        file_names = []
        for base_dir,chird_dir,files in os.walk(self.rooms_path):
            for file in files:
                if '.log' in file:
                    file_names.append(os.path.join(base_dir,file))
        return file_names

    def last1klog(self,file):




A = Log2Memached()
print A.logfilename()

