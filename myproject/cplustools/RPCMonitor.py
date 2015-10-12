import subprocess
import time
import os
os.chdir('/home/room/server/ServerMonitorTool')
s = subprocess.Popen('./ServerMonitorTool client', shell=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
s.stdin.write('all')
s.stdin.write('exit')
s.stdout.read()

