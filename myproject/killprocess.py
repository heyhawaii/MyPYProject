__author__ = 'Administrator'
import psutil
import time
while True:
    all_processes = list(psutil.process_iter())
    for proc in all_processes:
        try:
            if proc.cpu_percent(interval=0) > 100.0:
                proc.kill()
                print 'process name:',proc.name(), ' pid:',proc.pid,' is be killed'
        except:
            pass


    time.sleep(0.5)