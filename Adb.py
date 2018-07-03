# conding=utf-8
import os
import subprocess


class MyclassAdb():
    def __init__(self):
        self.__path = os.getcwd() + r'\adb'

    def adb(self, cmd):
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            #一定要加stderr,stdin的通道，不然打不带控制台的exe用不了
            log = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   stdin=subprocess.PIPE, cwd=self.__path, universal_newlines=True, startupinfo=si)
            #print('adb版本号：',log)
            print(log.pid)
            return log.stdout.read()
        except FileNotFoundError as e:
            # print('没有配置adb环境',e)
            return '没有配置adb环境', e
        except Exception as e:
            # print('其他错误：',e)
            return '其他错误：', e
