#conding=utf-8
import threading
import os
import re
from Adb import MyclassAdb
class android_data():
    def __init__(self):
        self.path = os.getcwd() + r'\adb'

    def android_ram(self,cdm):
        get_ram=MyclassAdb()
        ram_log=get_ram.adb('adb shell dumpsys meminfo com.jiguang.h5Test98')
        lines=str(ram_log)
        if lines.strip('b\'\\r\\n')=='error: device not found':
            print('把手机连上')
        else:
            for i in range(0,len(lines)):
                if lines[i]=='TOTAL:':
                    print(lines[i+1])


i=android_data()
th=threading.Thread(i.android_ram())
th.setDaemon(True)
th.start()
th.join()
