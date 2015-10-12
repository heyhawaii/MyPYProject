# import sys
# import os
# import time
# import datetime
# base_dir = '/home/mysql/data'
# log_file = '/tmp/dbfile_size.txt'
# while 1:
#     with open(log_file,'a')as f:
#         f.write('-'*50+'\n')
#         for parent,dirnames,filenames in os.walk(base_dir):
#                 for dir in dirnames:
#                     dir = os.path.join(parent,dir)
#                     for parent1,dirnames1,filenames1 in os.walk(dir):
#                         for file in filenames1:
#                             file = os.path.join(parent1,file)
#                             print int(os.stat(file).st_size)
#                            # f.write(("%s: %d, %.2f%s") % (file, int(os.stat(file).st_size), float(os.stat(file).st_size)/1024/1024, 'M\n'))
#         time.sleep(600)


import re
result_file = r'C:\Users\Administrator\Desktop\dbfile_size.txt'
d = {}
with open(result_file,'r') as f:
    for line in f:
        if '--' not in line:
            # print line
            line_content = line.split(':')
            # print line_content
            # print line_content[0]
            # print re.search('(\d+\.\d+)M',line_content[1]).group(1)
            if not d.get(line_content[0]):
                d[line_content[0]] = [re.search('(\d+\.\d+)M',line_content[1]).group(1)]
            else:
                d[line_content[0]].append(re.search('(\d+\.\d+)M',line_content[1]).group(1))
for k,v in d.items():
    if v[0] !=  v[-1]:
        print k,'-->',v[0],' ',v[-1]