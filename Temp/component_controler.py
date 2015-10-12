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


def get_screens(component_name):
    screens = []
    for screen in list_screens():
        #print screen
        if component_name.lower() in screen.name.lower():
            screens.append(screen)
    return screens   #['chatroom31','chatroom32']

def getpwd(rooms_path,screen_name):
    allroom = os.listdir(rooms_path)
    for room in allroom:
        if room.lower() == screen_name.lower():
            room_path = os.path.join(rooms_path,room)
            return  room_path   #'/home/room/server/ChatRoom31'
    return

def isalived(component_name):
    ps = psutil.process_iter()
    for psinfo in ps:
        try:
            if component_name.lower() == psinfo.name().lower():
                return psinfo
        except:
            continue
    return

def NewScreen(component_name):
    screen = Screen(component_name,True)
    return screen

def start(rooms_path,component_name,screen):
    if not isalived(screen.name):
        path = getpwd(rooms_path,screen.name)
        screen.send_commands('cd '+  path)
        screen.send_commands('./'+component_name)
        return  '%s started success!' % component_name

def stop(component_name,screen):
     if isalived(screen.name):
         component_process = isalived(screen.name)
         component_process.kill()
         return  '%s stopped success' % component_name

if __name__ == '__main__':
    rooms_path = '/home/room/server'
    components_name = sys.argv[1]
    segment = sys.argv[2]
    if len(sys.argv) < 3:
        print 'segment error! '
        sys.exit(1)
    if len(sys.argv) > 3:
        range_type = sys.argv[3]
        components_list = get_components_list(components_name,range_type)
    else:
        components_list = get_components_list(components_name)

    for component_name in components_list:
        if component_name not in list_screens():
            NewScreen(component_name)
        for screen in get_screens(component_name):

            if segment == 'start':
                # if not isalived(screen.name):
                #     path = getpwd(rooms_path,screen.name)
                #     screen.send_commands('cd '+  path)
                #     screen.send_commands('./'+component_name)
                #     print '%s started success!' % component_name
                print start(rooms_path,component_name,screen)
            elif segment == 'stop':
                 # if isalived(screen.name):
                 #     component_process = isalived(screen.name)
                 #     component_process.kill()
                 #     print '%s stopped success' % component_name
                print stop(component_name,screen)

            elif  segment == 'restart':
                 print stop(component_name,screen)
                 print start(rooms_path,component_name,screen)

            elif segment == 'checkhideroom':
                if isalived(screen.name):
                    path = getpwd(rooms_path,screen.name)
                    cmdlist = ['cd ' + path + ' && ' + 'rm -f dumproom_*.log',
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



            else :
                if isalived(screen.name):
                    path = getpwd(rooms_path,screen.name)
                    screen.send_commands(segment)
                    print 'send command to %s success!' % component_name

