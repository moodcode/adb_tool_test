from Adb import MyclassAdb
import subprocess

adb=MyclassAdb()
adb.adb('adb logcat -c')

# y=subprocess.Popen('adb -d  logcat >tettt.txt',shell=True,cwd=r'E:\python\adb_tool\adb')
# print(1)
# subprocess.Popen("taskkill /F /T /PID " + str(y.pid),shell=True,cwd=r'E:\python\adb_tool\adb')
# print(2)