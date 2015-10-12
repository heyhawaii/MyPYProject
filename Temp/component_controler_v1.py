import sys
import getpass
import os
import time
import re
import  subprocess

try:
    from screenutils import list_screens, Screen
except ImportError:
    print 'please install screenutils module. for example :' \
          'pip install screenutils'
    sys.exit(1)

try:
    import psutil
except ImportError:
    print 'please install psutil module. for example :' \
          'pip install psutil'
    sys.exit(1)

if getpass.getuser() != 'room':
    print 'must run as "room", please change user to "room"!'
    sys.exit(1)

def get_components_list(components_name,*range_type):
    components_list = []
    if '-' in components_name:
        component_base_name,start_num,end_num = re.search('([a-zA-z]+)(\d+)-(\d+)',components_name).groups()
        # if 'range_type' in locals().keys():
        #     if range_type == 'odd':
        #         range_over = xrange(int(start_num),int(end_num) + 1)[]
        for num in xrange(int(start_num),int(end_num) + 1):
            if range_type:
                if range_type[0] == 'odd':
                    if num % 2 :
                        components_list.append(component_base_name + str(num))
                if range_type[0] == 'even':
                    if not num % 2 :
                        components_list.append(component_base_name + str(num))
            else:
                components_list.append(component_base_name + str(num))#['ChatRoom31']
    else:
        components_list.append(components_name)
    return components_list

def arg_parser():

    '''
    Usage:
    type 1: component_controler.py servername start
    type 2: component_controler.py servername start odd

    Note:
        1. servername can replaced servername1-23 same like servernameNUMA-NUMB

            NUMA and NUMB are numbers, like 1, 2, 3, 4, 5, 6 ...

        2. start can replaced start stop restart or other command, for example:

            component_controler.py ChatRoom34-49 hide1

        3.  odd is a Filter,
            odd can replaced odd or even, and

                odd is keep odd number, ignore even number
                even is keep even number, ignore odd number

                odd is num % 2 is 1, like 1, 3, 5, 7, 9 ...
                even is num % 2 is 0, like 2, 4, 6, 8, 10 ...
    '''

    components_name = sys.argv[1]
    segment = sys.argv[2]
    if len(sys.argv) < 3:
        print '''segment error!
        Usage:
        component_controler.py screenname[NUMA-NUMB] start|stop|restart|other_command [odd|even]

        for example:

        1. start ChatRoom23
            component_controler.py ChatRoom23 start

        2. stop ChatRoom23, ChatRoom24, ... ChatRoom39
            component_controler.py ChatRoom23-39 stop

        3. restart ChatRoom24, ChatRoom26, ChatRoom28, ... ChatRoom38
            component_controler.py ChatRoom23-39 restart even

        4. send command "hide 1" to ChatRoom23, ChatRoom25, ChatRoom27, ... ChatRoom39
            component_controler.py ChatRoom23-39 "hide 1" odd
        '''
        sys.exit(1)
    if len(sys.argv) > 3:
        range_type = sys.argv[3]
        components_list = get_components_list(components_name,range_type)
    else:
        components_list = get_components_list(components_name)

    return (segment, components_list)

class component_controler:
    __components_list = []
    __rooms_path = ""

    def __init__(self, components_list = [], rooms_path = ""):
        if components_list != []:
            self.__components_list = components_list

        if rooms_path != "":
            self.__rooms_path = rooms_path

    def __get_screens(self, component_name):
            screens = []
            for screen in list_screens():
                #print screen
                if component_name.lower() in screen.name.lower():
                    screens.append(screen)
            return screens   #['chatroom31','chatroom32']

    def __isalived(self, component_name):
        for psinfo in psutil.process_iter():
            try:
                if component_name.lower() == psinfo.name().lower():
                    return psinfo
            except:
                continue
        return

    def __getpwd(self, rooms_path, screen_name):
        for room in os.listdir(rooms_path):
            if room.lower() == screen_name.lower():
                return os.path.join(rooms_path, room)
        return

    def __keep_screen(self, component_name):
        if component_name not in list_screens():
            screen = Screen(component_name,True)
            return screen
        else:
            return component_name

    def set_components_list(self, components_list):
        self.__components_list = components_list

    def set_rooms_path(self, rooms_path):
        self.__rooms_path = rooms_path

    def start(self):
        self.run('start')

    def stop(self):
        self.run('stop')

    def restart(self):
        self.run('restart')

    def run(self, segment):
        for component_name in self.__components_list:
            self.__keep_screen(component_name)

            for screen in self.__get_screens(component_name):
                if segment == 'start':
                    if not self.__isalived(screen.name):
                        path = self.__getpwd(self.__rooms_path, screen.name)
                        screen.send_commands('cd %s' % path)
                        screen.send_commands('./%s' % component_name)
                        print '%s started success!' % component_name

                elif segment == 'stop':
                    component_process = self.__isalived(screen.name)
                    if component_process:
                        component_process.kill()
                        print '%s stoped success!' % component_name

                elif segment == 'restart':
                    component_process = self.__isalived(screen.name)
                    if component_process:
                        component_process.kill()

                        path = self.__getpwd(self.__rooms_path, screen.name)
                        screen.send_commands('cd %s' % path)
                        screen.send_commands('./%s' % component_name)
                        print '%s restarted success!' % component_name

                elif segment == 'checkhideroom':
                    if self.__isalived(screen.name):
                        path = self.__getpwd(self.__rooms_path, screen.name)
                        cmdlist = [
                                    'cd ' + path + ' && ' + 'rm -f dumproom_*.log',
                                    'cd ' + path + ' && ' + 'ls dumproom_*.log',
                                    'cd ' + path + ' && ' + 'cat dumproom_*.log|grep "is_hide:1"'
                                  ]
                        p = subprocess.Popen(cmdlist[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        screen.send_commands('dumproomlist')
                        time.sleep(2)
                        #dumproom_2105_06_01_13_27_51.log
                        p = subprocess.Popen(cmdlist[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        dumpfile =  p.stdout.read()
                        #at dumproom_2105_05_29_17_33_44.log|grep 'is_hide:1'
                        p = subprocess.Popen(cmdlist[2], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        print screen.name,'-->',p.stdout.read()

                else:
                    if self.__isalived(screen.name):
                        # path = self.__getpwd(self.__rooms_path, screen.name)
                        # screen.send_commands('cd %s' % path)
                        screen.send_commands(segment)
                        print 'send command[%s] to %s success!' % (segment, component_name)

if __name__ == '__main__':

    rooms_path = '/home/room/server'
    segment, components_list = arg_parser()

    # mycontroler = component_controler(components_list = components_list, rooms_path = rooms_path)
    # or
    mycontroler = component_controler()
    mycontroler.set_components_list(components_list)
    mycontroler.set_rooms_path(rooms_path)

    # mycontroler.run(segment)
    # or
    if segment == 'start':
        mycontroler.start()
    elif segment == 'stop':
        mycontroler.stop()
    elif segment == 'restat':
        mycontroler.restart()
    else:
        mycontroler.run(segment)
