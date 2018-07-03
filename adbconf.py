# coding=utf-8
import re
import os
import time
import subprocess
from Adb import MyclassAdb


class Myclassconf():
    def __init__(self):
        self.myadb=MyclassAdb()
        self.path=os.getcwd()

    # 打开adb进程
    def start_adb(self):
        log = self.myadb.adb('adb start-server')
        if re.findall('successfully', str(log)):
            # print('启动成功')
            return '启动成功'
        else:
            # print('不知道什么原因失败了')
            return '不知道什么原因失败了'+str(log)

    # 关闭adb进程
    def close_adb(self):
        self.myadb.adb('adb kill-server')
        return '应该是关闭成功了，启动试试'

    # 查看是否有adb环境，并且获得adb版本
    def get_adb(self):
        log = self.myadb.adb('adb')
        str_log = str(log.split()[4]).strip('b').strip('\'')
        if re.match('[0-9]\.[0-9]\.[0-9][0-9]', str_log):
            # print('adb版本号：', str_log)
            return 'adb版本号：' + str_log
        else:
            return str(log)
            # print(log)

    # 判断手机是否正确链接电脑
    def get_phone(self):
        log = self.myadb.adb('adb devices')
        print(log.split())
        if log.strip() == b'List of devices attached':
            # print('确认手机已经连接电脑，并且开启了开发者模式和USB调试模式')
            return '确认手机已经连接电脑，并且开启了开发者模式和USB调试模式'
        elif str(log) == 'list index out of range':
            return '把手机连接上电脑 '
            # print('把手机连接上电脑 ')
        elif len(log.split()) >= 6 and log.split()[5] == 'device':
            # print('手机已经连接成功，你可以为所欲为了' )
            return '手机已经连接成功，你可以为所欲为了'
        else:
            # print('没连上应该有其他原因')
            return '没连上，确认手机开启开发者模式和USB调试，并且授权'

    # 获取安卓版本
    def get_android_version(self):
        version = self.myadb.adb('adb shell getprop ro.build.version.release')
        if re.findall('device not found', str(version)):
            return '确认手机已经连接电脑，并且开启了开发者模式和USB调试模式'
        else:
            return str(version).strip('b\\r\\n\'')

    # 获取当前界面的包名
    def get_FocusedActivity(self):
        activity = self.myadb.adb('adb shell "dumpsys activity activities|grep mFocusedActivity"')
        print(str(activity))
        if activity=='error: device not found\n':
            return '手机没有连接'

        #三星note8升级后原有获得当前的包名返回为空，换一个命令重新获取
        elif activity=="":
            activity = self.myadb.adb('adb shell "dumpsys activity activities"')
            activity=str(activity).split(' ')
            for num in range(0,len(activity)):
                if re.findall("affinity=",activity[num]):
                    str_pack=activity[num].split("=")[1]
                    return str_pack
        else:
            print (activity)
            str_pack = str(activity).split(' ')[5].split('/')[0]
            return str_pack

    # 清楚指定包名的缓存和数据
    def clean_pack_data(self, packName):
        clean_log = self.myadb.adb('adb shell pm clear ' + packName)
        return str(clean_log).strip('b\\r\\n\'')

    # 安装APK包
    def install_apk(self, apk_Path):
        install_log = self.myadb.adb('adb install -r ' + apk_Path)
        return str(install_log)

    # 删除APK包
    def uninstall_apk(self, packName):
        uninstall_log = self.myadb.adb('adb uninstall ' + packName)
        if str(uninstall_log).strip('b\\r\\n\'')=='Failure [DELETE_FAILED_INTERNAL_ERROR]':
            return '要删除的apk包不存在'
        else:
            return str(uninstall_log).strip('b\\r\\n\'')

    def jietu(self):
        Newtime = time.strftime('%Y-%m-%d%H%M%S', time.localtime(time.time()))
        self.myadb.adb('adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        log=self.myadb.adb("adb pull /sdcard/screenshot.png "+self.path.replace('\\','/')+'/'+Newtime+'.png')


    def get_log(self,path):
        adb_log=subprocess.Popen('adb logcat >'+path,shell=True,cwd=self.path+r'\adb')
        time.sleep(5)
        subprocess.Popen("taskkill /F /T /PID " + str(adb_log.pid), shell=True, cwd=self.path+r'\adb')

    def clear_log(self):
        self.myadb.adb('adb logcat -c')


    def video(self,video_time):
        myadb=subprocess.Popen('adb shell screenrecord --time-limit '+str(video_time)+' /sdcard/demo.mp4',shell=True,cwd=self.path+r'\adb')
        # print('adb shell screenrecord --time-limit '+str(video_time)+' /sdcard/demo.mp4')
        # print('录制结束')
        return myadb.pid


    def stop_video(self,video_pid):
        subprocess.Popen("taskkill /F /T /PID " + str(video_pid), shell=True, cwd=self.path + r'\adb')

    def pull_video(self,bendi_path):
        subprocess.Popen('adb pull /sdcard/demo.mp4 '+bendi_path, shell=True, cwd=self.path + r'\adb')



# lg=Myclassconf()
# # y=lg.install_apk(r'C:\Users\quan\Desktop\2018_3_7_11_24_15_1002721.apk')
# # # F:\python\adb_tool\2018_4_10_16_58_46_1002721.apk
# y=lg.get_FocusedActivity()
# print(y)
