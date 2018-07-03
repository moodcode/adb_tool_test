#coding=utf-8
import csv
LIST_CPU=[]
from Adb import MyclassAdb
class MyclassgetCpu():
    def __init__(self):
        pass

    def clean_cpu(self):
        global LIST_CPU
        LIST_CPU=[]

    def get_cpu(self,packName):
        cpulist=[]
        get_ram=MyclassAdb()
        ram_log=get_ram.adb("adb shell top -m 100 -n 1 -s cpu")
        print (ram_log)
        p=str(ram_log).split('\n')
        # print(p)
        for x in range(0,len(p)):
            # print(p[x].strip('\\r').split(" "))
            cuplist=p[x].strip('\\r').split(" ")
            # print(cuplist[-1])
            if cuplist[-1] == packName:
                while '' in cuplist:  # 将list中的空元素删除
                    cuplist.remove('')
                LIST_CPU.append(cuplist[4])
                return cuplist[4]
        return '没有找到这个进程'

    def cpu_csv(self,fileName):
        global LIST_CPU
        with open(fileName,"w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(LIST_CPU)

    # def xx(self):
    #     li = os.popen("adb shell top -m 100 -n 1 -s cpu").readlines()
    #     print(li)

# li = os.popen("adb shell top -m 100 -n 1 -s cpu").readlines()
#     name = "com.m37.dtszjwd.sy37.ka"
#     for line in li:
#         if re.findall(name, line):
#             cuplist = line.split(" ")
#     # print cuplist
#     if cuplist[-1].strip() == 'com.m37.dtszjwd.sy37.ka':
#         while '' in cuplist:  # 将list中的空元素删除
#             cuplist.remove('')
#         # print cuplist[4]
#         return float(cuplist[4].strip('%'))