# -*- coding: utf-8 -*-
import salt
salt_host_list = []
class SaltControl(object):
    def __init__(self):
        self.base_dir = '/home/room/server'
        self.client = salt.client.LocalClient('/etc/salt/master')

    def getMsgconfig(self,host):
        self.host = host
        ret = self.client.cmd(self.host,
                              'file.find',
                              [
                              self.base_dir,
                              name = 'config.json',
                              type = 'f',
                              grep = 'MsgServer',
                              print = 'path'
                              ]
        )

        return ret
print SaltControl().getMsgconfig()