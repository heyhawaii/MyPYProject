import socket
from component_controler import *
import time
'''
'{components_name:[gate1,gate2],' \
'action:"start/stop/sendcommand"'
'''
class SocketServer(object):

    def getmyipaddr(self,type):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if type == 'wan':
            s.connect(('114.114.114.114', 0))
        if type == 'lan':
            s.connect(('192.168.4.1', 0))
        myip = s.getsockname()[0]
        return myip

    def socketbase(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        myip = self.getmyipaddr('lan')
        self.sock.bind((myip,19166))
        self.sock.listen(5)
        while True:
            self.connection,address = self.sock.accept()
            try:
                self.connection.settimeout(5)
                self.data = self.connection.recv(1024)
                self.getcmd = self.getcommand()
                if not self.getcmd:
                    self.result = 'not enough segments '
                else:
                    self.execute_command()
                self.returndata()
            except Exception,e:
                print e
                pass

    def getcommand(self):
        self.data = eval(self.data)
        if self.data.get('components_name') and self.data.get('action'):
            self.components_name = self.data['components_name']
            self.action = self.data['action']
            return True
        else:
            return False


    def execute_command(self):
         for component_name in self.components_name:
            component = Action(component_name)
            if self.action == 'restart':
                self.result = component.stop()
                time.sleep(1)
                self.result += '\n'+ component.start()
            elif self.action == 'stop':s
                self.result = component.stop()
            elif self.action == 'start':
                self.result = component.start()
            else:
                self.result = component.sendcmd(self.action)

    def returndata(self):
        self.connection.send(self.result)
        self.connection.close()


if __name__ == '__main__':
    sockserver = SocketServer()
    sockserver.socketbase()