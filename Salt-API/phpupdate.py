# -*- coding: utf-8 -*-
import salt
import sys
import os
import re
import datetime
from SimpleXMLRPCServer import SimpleXMLRPCServer

# hostlist = eval(sys.argv[1])  #字符串格式为['DY-WH01-ROOM-03','DY-WH01-ROOM-16']
# zipfile = 'file.zip' #3
# localpath = 'php_update/20150407rc1/' #2
# localfile = '%s%s%s' % ('salt://',localpath,zipfile)
# remotepath = '/tmp/' #4
# remotebackpath = '/data/backup/'#5
# remotefile = remotebackpath + zipfile


class PhpUpdate(object):
    def __init__(self):
        self.client = salt.client.LocalClient('/etc/salt/master')


#文件上传
    def file_upload(self,hostlist,localfile,remotefile):
        #ret = self.client.cmd(['DY-WH01-ROOM-03','DY-WH01-ROOM-16'],'cmd.run',['ls -l '],expr_form='list')
        ret = self.client.cmd(hostlist,
                              'cp.get_file',
                              [
                                  localfile,
                                  remotefile,
                                 # 'gzip=5 '
                              ],
                              expr_form='list'
                              )
        return ret

#目录备份
    #defaults to /var/cache/salt/master/minions/minion-id/files
    #salt '*' archive.zip template=jinja /tmp/zipfile.zip /tmp/sourcefile1,/tmp/{{grains.id}}.txt
    def file_backup(self,hostlist,remotepath,remotebackpath):
        dt = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        backfile = remotebackpath + dt + '.zip'
        ret = self.client.cmd(hostlist,
                              'archive.zip',
                              [
                                  backfile,
                                  remotepath,
                              ],
                              expr_form='list'
                              )
        if ret:
            return 'backup complete !'
#        return ret


#列出备份目录
    def list_backdir(self,hostlist,remotebackpath):
        ret = self.client.cmd(hostlist,
                              'cmd.run',
                              [
                                  'ls',
                                  remotebackpath,
                              ],
                              expr_form='list'
                              )
        return ret




#解压更新
#salt ’*’ archive.unzip template=jinja /tmp/zipfile.zip /tmp/{{grains.id}}/ excludes=file_1,file_2
    def update(self,hostlist,remotebackpath,remotepath,zipfile):
        if zipfile != 'file.zip':
            unzip_path = '/'
        else:
            unzip_path = os.path.dirname(remotepath)
        remotefile = os.path.join(remotebackpath, zipfile)
        ret = self.client.cmd(hostlist,
                              'archive.unzip',
                              [
                                  remotefile,
                                  unzip_path,
                              ],
                              expr_form='list'
                              )
        return ret

#修改upstream
#salt ’*’ state.sls myslsfile pillar="{foo: ’Foo!’, bar: ’Bar!’}"

    def update_upstream(self,hostlist,action,target):
        upstream_sls = '/srv/pillar/nginx/upstream/upstream.sls'
        nginx_hosts = ['salt-11','salt-12']  #nginx主机的salt-id
        php_groups = ('192.168.5.11:9000', '192.168.5.12:9000')
        string = 'web_php_group:  |\n'
        for x in php_groups:
            string +=  "  server %s     weight=10 max_fails=2 fail_timeout=30s;\n" % x

        if action == 'drop':
            if target :
                seg = '.*%s.*' % target.replace('.','\.')
                line = re.search(seg , string).group(0)
                replace_line = re.sub('^\s\s','  #',line)
                string = re.sub(line,replace_line,string)

        if action ==  'accept':
            if target :
                seg = '.*%s.*' % target.replace('.','\.')
                line = re.search(seg , string).group(0)
                string = re.sub(line,line.replace('#',''),string)

        with open(upstream_sls,'w') as f:
            f.write(string)

        ret = self.client.cmd(nginx_hosts,
                              'state.sls',
                              [
                                  upstream_sls,
                              ],
                              expr_form='list'
                              )
        return ret


if __name__ == '__main__':
    hosts = PhpUpdate()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000))#确定URL和端口
    print "Listening on port 8000..."
    server.register_instance(hosts,'PhpUpdate')
    server.serve_forever()



