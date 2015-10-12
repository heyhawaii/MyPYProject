# coding: utf-8
import gzip
import sys
import os
import re
starttime= '00:10:30'
endtime = '00:15:50'
date = '15'
keywords = '/api/v1/live'
file_type = 'gz'   #gz或其他
log_type = 'fpm' #'fpm'或'nginx'
filename = 'www.access.log-20150320.gz'

if file_type == 'gz':
    logfile  = gzip.GzipFile(filename)
else:
    logfile  = open(filename,'r')

result_log = os.getcwd() + '/result.log'
def time_interval(starttime,endtime,line):
    if len(line) > 5:
        if log_type == 'fpm':
            line_group = re.search('\s(\d+)/\w{3}/\d{4}:(\d{2}:\d{2}:\d{2})\s\+0800\s(.*?)\s',line)
        if  log_type == 'nginx':
            line_group = re.search('\[(\d+)/\w{3}/\d{4}:(\d{2}:\d{2}:\d{2})',line)
        line_date = line_group.group(1)
        line_time = line_group.group(2)

        if line_date == date:
            if starttime <= line_time and line_time <=  endtime:
                if keywords:
                    if keywords in line:
                        return line
                    else:
                        return
                return line
            if line_time > endtime:
                sys.exit(0)
line = logfile.readline()
while line:
    result = time_interval(starttime,endtime,line)
    if result:
        with open(result_log,'a+') as f:
            f.write(line)
    line = logfile.readline()
logfile.close()
f.close()


