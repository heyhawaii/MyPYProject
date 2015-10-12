
import re
import json
import sys

old_config = 'config.txt'
new_config_json = 'config.json'
d = {}
with open(old_config,'r') as o:
    n = 0
    for line in o:
        n += 1
        reseg = re.compile('(\w+.*?)@=(\w+.*?)/')
        reseg.findall(line)
        if n == 1 :
            for x in reseg.findall(line):
                try:
                    d[x[0]] = int(x[1])
                except:
                    d[x[0]] = x[1]
        else:
            d1 = {}
            for y in reseg.findall(line):
                try:
                    d1[y[0]] = int(y[1])
                except:
                    d1[y[0]] = y[1]
            print d1
            if d.get('server_list') == None :
                d['server_list'] = []
            else:
                d['server_list'].append(d1)
if len(sys.argv) > 1 and sys.argv[1] == 'white_ip':
    d['white_ip'] = [
                     "192.168.0.*",
                     "27.17.8.110",
                     "221.234.42.170",
                     "221.234.42.157",
                     "221.234.42.158",
                     "119.147.137.245",
                     "121.9.245.181",
                     "115.231.98.26",
                     "171.91.159.200",
                     "221.229.163.130",
                     "180.97.182.50",
                     "180.97.182.51",
                     "182.18.47.5",
                     "124.95.173.46",
                     "220.194.199.222",
                     "218.199.110.35",
                     "111.4.115.105",
                     "218.205.74.82",
                     "162.211.183.239"
                     ]
json.dump(d,open('config.json','w'),indent=4)
print 'Finished'
