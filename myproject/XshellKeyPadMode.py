# -*- coding:cp936 -*-
import fileinput
import os
import time
from config import *


def get_sessions_file(base_dir):
    files =[]
    for base_path,dir_path,filenames in os.walk(base_dir):
        for filename in filenames:
            if '.xsh' in filename:
                file = os.path.join(base_path,filename)
                files.append(file)
    return files

def chline(filename):
    for line in fileinput.input(filename,backup='_bak',inplace=1):
        if 'InitKeypadMode' in line:
            print 'InitKeypadMode=2\n',
            continue
        print line,
    fileinput.close()

if __name__ == '__main__':
    files = get_sessions_file(base_dir)
    for file in files:
        chline(file)
        print file,'chanced success!'

time.sleep(2)