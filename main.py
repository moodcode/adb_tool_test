# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

from Ui_adb import Ui_MainWindow
from adbconf import Myclassconf
from appRam import MyclassGetRAM
from appCpu import MyclassgetCpu
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import pyqtSignal,QObject
import threading
import os

import time

class MainWindow(QMainWindow, Ui_MainWindow,QObject):
    send_text = pyqtSignal(str)
    send_text2 = pyqtSignal(str)
    def __init__(self, parent=None):
        self.fool_ram=0
        self.fool_cpu=0
        self.fool_video=0
        self.video_pid=0
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.adb_Butt.clicked.connect(self.adb_ver)
        self.adb_devices_Butt.clicked.connect(self.phone_state)
        self.start_adb_Butt.clicked.connect(self.start_adb)
        self.close_adb_Butt.clicked.connect(self.close_adb)
        self.get_version_Butt.clicked.connect(self.android_version)
        self.get_Activity_Butt.clicked.connect(self.thread_Activity)
        self.uninstall_Butt.clicked.connect(self.uninstall)
        self.path_Butt.clicked.connect(self.apk_path)
        self.install_Butt.clicked.connect(self.thread_install)
        self.get_RAM_Butt.clicked.connect(self.thread_ram)
        self.close_RAM_butt.clicked.connect(self.thread_stop_ram)
        self.ram_csv_Butt.clicked.connect(self.csv_writer_ram)
        self.clean_ram_Butt.clicked.connect(self.clean_ram_log)
        self.get_CPU_Butt.clicked.connect(self.thread_cpu)
        self.close_CPU_Butt.clicked.connect(self.thread_stop_cpu)
        self.cpu_csv_Butt.clicked.connect(self.csv_writer_cpu)
        self.clean_cpu_Butt.clicked.connect(self.clean_cpu_log)
        self.clear_Butt.clicked.connect(self.clean_data)
        self.get_log_Butt.clicked.connect(self.log)
        self.jietu_Butt.clicked.connect(self.jietu)
        self.video_start_butt.clicked.connect(self.start_video)
        self.video_stop_butt.clicked.connect(self.close_video)
        self.pushButton_2.clicked.connect(self.get_video)
        self.pushButton.clicked.connect(self.clean_log)

    # 这个是弹窗
    def waring(self, str_log):
        QMessageBox.warning(self,
                            "消息框",
                            str_log,
                            QMessageBox.Yes)
    def emit_send(self,log):
        self.packName_text.setText(log)

    def test(self):
        _logo_str = "我们的标志是：\n"
        _logo_str += "上帝的骑宠，上古时期世界的霸主。\n"
        _logo_str += "┏┛┻━━━┛┻┓\n"
        _logo_str += "┃｜｜｜｜｜｜｜┃\n"
        _logo_str += "┃　　　━　　　┃\n"
        _logo_str += "┃　┳┛ 　┗┳  ┃\n"
        _logo_str += "┃　　　　　　　┃\n"
        _logo_str += "┃　　　┻　　　┃\n"
        _logo_str += "┃　　　　　　　┃\n"
        _logo_str += "┗━┓　　　┏━┛\n"
        _logo_str += "    ┃　史　┃　　\n"
        _logo_str += "    ┃　诗　┃　　\n"
        _logo_str += "    ┃　之　┃　　\n"
        _logo_str += "    ┃　宠　┃\n"
        _logo_str += "    ┃　　　┗━━━┓\n"
        _logo_str += "    ┃经验与我同在  ┣┓\n"
        _logo_str += "    ┃攻楼专用宠物  ┃\n"
        _logo_str += "    ┗┓┓┏━┳┓┏┛\n"
        _logo_str += "      ┃┫┫　┃┫┫\n"
        _logo_str += "      ┗┻┛　┗┻┛\n"

        _intr_str = "我们的口号是：\n"
        _intr_str += "搬别人的砖让别人无砖可搬\n"
        _intr_str += "亲，你还想加入我们吗？"
        self.waring(_logo_str+_intr_str)

    # 返回adb的信息
    def adb_ver(self):
        adb = Myclassconf()
        ver = adb.get_adb()
        self.waring(ver)

    # 查看手机链接状态
    def phone_state(self):
        adb = Myclassconf()
        devices = adb.get_phone()
        self.waring(devices)

    # 启动adb进程
    def start_adb(self):
        adb = Myclassconf()
        server_log = adb.start_adb()
        self.waring(server_log)

    # 关闭adb进程
    def close_adb(self):
        adb = Myclassconf()
        close_adb_log = adb.close_adb()
        self.waring(close_adb_log)

    #获得安卓版本号
    def android_version(self):
        adb=Myclassconf()
        version_log=adb.get_android_version()
        self.waring(version_log)

    #获取当前界面APK的包名
    def FocusedActivity(self):
        adb=Myclassconf()
        activity_log=adb.get_FocusedActivity()
        self.send_text2.emit(activity_log)

    #包卸载
    def uninstall(self):
        adb=Myclassconf()
        packName=self.uninstall_packName_text.toPlainText()
        if packName!='':
            uninstall_log=adb.uninstall_apk(packName)
            self.waring(uninstall_log)
        else:
            self.waring('左边输入框填个包名')

    #获取安装包绝对路径
    def apk_path(self):
        pathName, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "C:/Users/quan/Desktop",
                                    "APK (*.apk)")   #设置文件扩展名过滤,注意用双分号间
        if pathName!='':
            self.packPath_text.setText(pathName.replace('/','\\'))
    #安装apk
    def install(self):
        adb=Myclassconf()
        apk_path=self.packPath_text.toPlainText()
        if apk_path!='':
            install_log=adb.install_apk(apk_path)
            self.send_text.emit(install_log)
        else:
            self.send_text.emit('左边加载下路径或者自己填个绝对路径')

    #清除apk数据和缓存
    def clean_data(self):
        adb=Myclassconf()
        packName=self.packName_text.toPlainText()
        if packName!='':
            data_log=adb.clean_pack_data(packName)
            self.waring(data_log)
        else:
            self.waring('填个包名')

    def jietu(self):
        adb=Myclassconf()
        adb.jietu()
        self.send_text.emit('截图完毕')

    # def log(self):
    #     adb=Myclassconf()
    #     adb.get_log()

    #循环读取并输出内存
    def ram(self):
        self.thread_Activity()
        time.sleep(1)
        adb_ram=MyclassGetRAM()
        cursor = self.RAM_log_text.textCursor()
        self.fool_ram=1
        while self.fool_ram==1:
            # time.sleep(0.5)
            if self.packName_text.toPlainText()=='':
                self.RAM_log_text.append('获取当前包名或者填入包名')
                self.fool_ram=0
            else:
                adb_log=adb_ram.get_ram(self.packName_text.toPlainText(),int(self.range_ram_text.text()),self.checkBox_jietu.isChecked())
                # print(adb_log)
                time.sleep(0.8)

                try:
                    print('第一步')
                    #self.RAM_log_text.append(adb_log)

                    cursor.insertText(adb_log+'\n')
                    print('第二步')
                except Exception as e:
                    print('第四步')
                    cursor.insertText(adb_log)
                    #self.RAM_log_text.append('报错，在打印日志:'+e)
                print('第三步')
                time.sleep(0.1)
                cursor.movePosition(QTextCursor.End)
                print('第3+2步')
                time.sleep(0.1)
                self.RAM_log_text.setTextCursor(cursor)
                #self.RAM_log_text.moveCursor(QTextCursor.End)
                print('第3+1步')

    #循环读取CPU并输出
    def cpu(self):
        self.thread_Activity()
        time.sleep(1)
        adb_cpu=MyclassgetCpu()
        self.fool_cpu=1
        cursor = self.CPU_log_text.textCursor()
        if self.packName_text.toPlainText()=='':
            self.fool_cpu=0
            self.CPU_log_text.append('获取当前包名或者填入包名')
        else:
            while self.fool_cpu==1:
                time.sleep(0.9)
                print('CPU第1步')
                cpu_log=adb_cpu.get_cpu(self.packName_text.toPlainText())
                print('CPU第2步')
                if cpu_log=='没有找到这个进程':
                    self.fool_cpu=0
                    print('CPU第3步')
                    cursor.insertText(cpu_log+'\n')
                else:
                    #self.CPU_log_text.append(cpu_log)
                    print('CPU第4步')
                    cursor.insertText(cpu_log+'\n')
                print('CPU第5步')
                cursor.movePosition(QTextCursor.End)
                print('CPU第7步')
                time.sleep(0.1)
                self.CPU_log_text.setTextCursor(cursor)


    def log(self):
        fileName, ok = QFileDialog.getSaveFileName(self,
                                                   "文件保存",
                                                   os.getcwd(),
                                                   "txt (*.txt)")
        if fileName!='':
            adb_log=Myclassconf()
            adb_log.get_log(fileName)

    def clean_log(self):
        adb=Myclassconf()
        adb.clear_log()

    def start_video(self):
        adb_log=Myclassconf()
        if self.fool_video==1:
            self.send_text.emit('不要重复开启录制')
        elif self.time_min_text.text()=='0' and self.time_sec_text.text()=='0':
            self.send_text.emit('填入录制时间')
        else:
            video_time=int(self.time_min_text.text())*60+int(self.time_sec_text.text())
            print(video_time)
            self.video_pid=adb_log.video(video_time)
            self.send_text.emit('正在录制视频，视频长短为%s秒' %str(video_time))

    def close_video(self):
        adb = Myclassconf()
        adb.stop_video(self.video_pid)
        self.send_text.emit('录像线程已关闭')

    def get_video(self):
        fileName, ok = QFileDialog.getSaveFileName(self,
                                                   "文件保存",
                                                   os.getcwd(),
                                                   "mp4 (*.mp4)")
        if fileName != '':
            adb = Myclassconf()
            adb.pull_video(fileName)
            self.send_text.emit('录像保存完毕%s'%fileName)


    def thread_video(self):
        th3 = threading.Thread(target=self.start_video)
        th3.setDaemon(True)
        th3.start()
    #安装app多线程
    def thread_install(self):
        th2=threading.Thread(target=self.install)
        th2.setDaemon(True)
        th2.start()

    #读取ram子线程
    def thread_ram(self):
        th=threading.Thread(target=self.ram)
        th.setDaemon(True)
        th.start()

    #读取cpu子线程
    def thread_cpu(self):
        th1=threading.Thread(target=self.cpu)
        th1.setDaemon(True)
        th1.start()

    def thread_Activity(self):
        th4=threading.Thread(target=self.FocusedActivity)
        th4.setDaemon(True)
        th4.start()

    def thread_stop_ram(self):
        if self.fool_ram==0:
            self.RAM_log_text.append('查看内存未开启')
            self.RAM_log_text.moveCursor(QTextCursor.End)
        elif self.fool_ram==1:
            self.fool_ram=0
            time.sleep(1)
            self.RAM_log_text.append('关闭成功')
            self.RAM_log_text.moveCursor(QTextCursor.End)

    def thread_stop_cpu(self):
        if self.fool_cpu==0:
            self.CPU_log_text.append('查看cpu未开启')
            self.CPU_log_text.moveCursor(QTextCursor.End)
        elif self.fool_cpu==1:
            self.fool_cpu=0
            time.sleep(1)
            self.CPU_log_text.append('关闭成功')
            self.CPU_log_text.moveCursor(QTextCursor.End)

    def clean_ram_log(self):
        self.RAM_log_text.clear()
        adb_log=MyclassGetRAM()
        adb_log.clean_ram()

    def clean_cpu_log(self):
        self.CPU_log_text.clear()
        cpu_log=MyclassgetCpu()
        cpu_log.clean_cpu()

    def csv_writer_ram(self):
        fileName, ok = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    os.getcwd(),
                                    "CSV (*.csv)")     #设置文件扩展名过滤,注意用双分号间
        if fileName!='':
            adb_ram=MyclassGetRAM()
            adb_ram.ram_cav(fileName)

    def csv_writer_cpu(self):
        fileName, ok = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    os.getcwd(),
                                    "CSV (*.csv)")     #设置文件扩展名过滤,注意用双分号间
        if fileName!='':
            adb_cpu=MyclassgetCpu()
            adb_cpu.cpu_csv(fileName)

    def closeEvent(self, *args, **kwargs):
        self.fool_ram=0
        self.fool_cpu=0
        if self.fool_video!=0:
            adb = Myclassconf()
            adb.stop_video(self.video_pid)






if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    QApplication.addLibraryPath("./plugins")
    mainWindow = MainWindow()
    mainWindow.send_text.connect(mainWindow.waring)
    mainWindow.send_text2.connect(mainWindow.emit_send)

    mainWindow.show()
    sys.exit(app.exec_())
