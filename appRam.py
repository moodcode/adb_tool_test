#conding=utf-8
import re
import csv
import time
import os
from Adb import MyclassAdb
LIST_RAM=[]
class MyclassGetRAM():
    def __init__(self):
        self.__ram_log=''
        self.ram_num1=0
        self.path=os.getcwd()
    def clean_ram(self):
        global LIST_RAM
        LIST_RAM=[]

    def get_ram(self,packName,range_ram,checkbox_ram):
        global LIST_RAM
        get_ram=MyclassAdb()
        ram_log=get_ram.adb('adb shell dumpsys meminfo '+ packName)
        lines=str(ram_log)
        list_lines=lines.split()
        if lines.strip('b\'\\r\\n')=='error: device not found':
            return ('把手机连上')
        elif re.findall('TOTAL',lines):
            for i in range(100,len(list_lines)):
                print (list_lines[i])
                if list_lines[i]=='TOTAL:' or list_lines[i]=="TOTAL" :
                    ram_num=int(int(list_lines[i+1])/1024)
                    if ram_num-self.ram_num1>=range_ram and self.ram_num1!=0 and checkbox_ram==True:
                        get_ram.adb("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
                        Newtime=time.strftime('%Y-%m-%d%H%M%S',time.localtime(time.time()))
                        # print("adb pull /sdcard/screenshot.png "+self.path.replace('\\','/')+'/截图/'+Newtime+ '当时内存'+str(ram_num)+'.png')
                        get_ram.adb("adb pull /sdcard/screenshot.png "+self.path.replace('\\','/')+'/截图/'+Newtime+ '当时内存'+str(ram_num)+'.png')
                        self.ram_num1=ram_num
                        LIST_RAM.append(ram_num)
                        return str('截图，当时内存是：'+str(ram_num))

                    else:
                        print('第四步')
                        self.ram_num1=ram_num
                        print('第5步')
                        LIST_RAM.append(ram_num)
                        print('第6步')
                        return str(ram_num)
                    # self.__list_ram.append(lines[i+1])
        else:
            return lines.strip('\'\\r\\n')

    def ram_cav(self,fileName):
        global LIST_RAM
        with open(fileName,"w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(LIST_RAM)


# x=MyclassGetRAM()
# while True:
#     time.sleep(1)
#     y=x.get_ram('com.jiguang.h5Test98',50)
#     print('输出的Y',y)








