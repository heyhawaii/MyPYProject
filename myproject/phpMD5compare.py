#conding: utf-8
import memcache
mc = memcache.Client(['192.168.4.92:33211'],debug=0)
standard_data = eval(mc.get('192.168.4.92'))
for nu in xrange(1,24):
    ipaddr = '192.168.4.' + str(nu)
    each_mc_data = eval(mc.get(ipaddr))
    if each_mc_data != standard_data:
        for x in each_mc_data:
            if each_mc_data[x] != standard_data.get(x):
                if not standard_data.get(x):
                    print 'warning: %s is not in standard files' % each_mc_data[x]
                else:
                    print x
                    print '%s:%s\t%s:%s' % (ipaddr,each_mc_data[x],'source', standard_data[x])

