__author__ = 'Jlink'
import os
import time
import logging
import logging.config
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

google_searcher = input("是否为MTK的GMS版本，是否主界面有Google搜索微件？两者都是为1，其他情况都为0：")
total = int(input("请输入所有应用程序界面的总应用数：             "))
row = int(input("请输入所有应用程序界面第一屏满屏应用的总行数： "))
col = int(input("请输入所有应用程序界面第一屏满屏应用的总列数： "))

get_version = 'adb shell getprop ro.build.version.release'
version = os.popen(get_version).read()
get_SN = 'adb shell getprop ro.boot.serialno'
deviceName = os.popen(get_SN).read()
lanucher_package = 'com.android.launcher3'
lanucher_activity = '.Launcher'

if google_searcher == '1':
    lanucher_activity = 'com.android.searchlauncher.SearchLauncher'

desired_caps = {
        'platformName':'Android',
        'platformVersion':version,
        'deviceName':deviceName,
        'appPackage':lanucher_package,
        'appActivity':lanucher_activity,
        'autoGrantPermissions':'true'
    }

driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)

#系统应用的包名
system_apppackage = ['com.android.launcher3','com.android.browser','com.android.calculator2','com.android.calendar',
                     'com.mediatek.camera','com.android.deskclock','com.android.contacts','com.android.email',
                     'com.mediatek.filemanager','com.android.fmradio','com.android.gallery3d','com.android.mms',
                     'com.android.music','com.android.dialer','com.android.quicksearchbox','com.android.settings',
                     'com.android.soundrecorder','com.android.inputmethod.latin','com.android.chrome',
                     'com.android.cellbroadcastreceiver','com.android.vending','com.google.android.apps.maps',
                     'com.google.android.calendar','com.google.android.contacts','com.google.android.apps.photos',
                     'com.google.android.apps.messaging','com.google.android.gms','com.google.android.apps.tachyon',
                     'com.google.android.gm','com.google.android.googlequicksearchbox','com.google.android.music',
                     'com.google.android.youtube','com.google.android.apps.youtube.music','com.google.android.videos',
                     'com.google.android.apps.docs','com.google.android.apps.nbu.files','com.sprd.sprdnote',
                     'com.sprd.screencapture','com.android.messaging','com.android.documentsui','com.android.camera2'
                     ]
system_apppackage = set(system_apppackage)
sums = row*col
total = total + 1
path = r'E:\Picture\Click_APP_Shot'
#清空log文件
def delete_log():
    try:
        #获取当前文件的路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        #log文件删除
        for root,dir,files in os.walk(current_dir):
            for name in files:
                #匹配log文件规则
                if name.endswith(".log"):
                    os.remove(os.path.join(root,name))
    except Exception as e:
        logging.error(e)
#删除log文件
delete_log()
#加载日志配置文件
CON_LOG = 'log.conf'  #注意是log.conf所在的路径
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()

#计算屏数
def screen_total(total,sums):
        if (total)%sums == 0:
                screen_total = int((total)/sums)
        else:
                screen_total = int((total)/sums) + 1
        return screen_total

#计算剩余的行数
def row_total(total,sums,col):
        if (total-sums*screen_total(total,sums))%col == 0:
                row_total = int((total-sums*(screen_total(total,sums)-1))/col)
        else:
                row_total = int((total-sums*(screen_total(total,sums)-1))/col) + 1
        return row_total

#创建文件夹
def create_file():
    try:
        #若该文件夹不存在，直接创建
        os.makedirs(path)
    except Exception as e:
        logging.warning(e)
        #将该文件夹下的.png图片全部删除
        for root,dirs,files in os.walk(path):
            for name in files:
                #匹配图片规则
                if name.endswith(".png"):
                    os.remove(os.path.join(root,name))
                    #print("Delete File:" + os.path.join(root,name))

#点击应用
def click(n,s):
    try:
        #滑屏进入所有应用程序界面
        swipeAll()
        #滑屏的次数
        swipeUp(s)
        driver.find_elements_by_class_name('android.widget.TextView')[n].click()
        time.sleep(3)
        #允许权限
        isPermission()
        #判断应用是否闪退
        isFlashBack(n)
        #判断应用是否停止运行
        isError()
        #旋转界面
        rotation()
        #判断应用是否闪退
        isFlashBack(n)
        #截图
        screen_shot()
        #关闭应用后台运行
        close()
        #回到主界面
        home()
        time.sleep(1)
        print("================================================================")
    except Exception as e:
            logging.error(e)
            logging.error("第"+str(n+1)+"个应用未检查")
            #回到主界面
            home()
#回到主界面
def home():
    try:
        driver.start_activity(lanucher_package,lanucher_activity)
        time.sleep(1)
        #获取当前的应用的包名
        package = current_package()
        #若当前应用为lanucher3，则旋转为竖屏
        if package == lanucher_package:
            rotation()
    except Exception as e:
        logging.error(e)
        time.sleep(5)
        driver.start_activity(lanucher_package,lanucher_activity)
        time.sleep(1)
        rotation()
#获取当前应用的包名
def current_package():
    try:
        package = driver.current_package
    except Exception as e:
        logging.error(e)
        time.sleep(10)
        package = driver.current_package
    return package

#保存截图
def screen_shot():
        #获取当前应用的包名
        package = current_package()
        #获取当前的时间
        timestr = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime())
        #获取存储的路径path = 'E:\\Picture\\Click_APP_Shot'
        img_path = os.path.abspath(path)
        #保存的路径
        save_path = img_path + "\\"+package+"_"+timestr+".png"
        #截图
        driver.save_screenshot(save_path)

#关闭应用
def close():
        #获取当前应用的包名
        package = current_package()
        #当前应用为系统应用时，不关闭后台
        if package in system_apppackage:
                pass
        else:
                #关闭该应用
                try:
                        driver.terminate_app(package,timeout=5000)
                except Exception as e:
                        logging.error(package + "应用关闭超时")
#滑屏到所有应用程序界面
def swipeAll():
        try:
            x = driver.get_window_size()['width']
            y = driver.get_window_size()['height']
            driver.swipe(0.5*x,y-80,0.5*x,0)
            time.sleep(1)
        except Exception as e:
            logging.error(e)
            driver.start_activity(lanucher_package,lanucher_activity)
            time.sleep(5)
            rotation()
            x = driver.get_window_size()['width']
            y = driver.get_window_size()['height']
            driver.swipe(0.5*x,y-80,0.5*x,0)
            time.sleep(1)
#滑屏到下一屏
def swipeUp(n):
        if n == 1:
                pass
        else:
                for i in range(n-1):
                        x = driver.get_window_size()['width']
                        y = driver.get_window_size()['height']
                        driver.swipe(0.5 * x, y - 1, 0.5 * x, 100, 5000)
                        time.sleep(1)

#旋转
def rotation():
        package = current_package()
        if package in system_apppackage:
                if driver.orientation == 'LANDSCAPE':
                        try:
                                #旋转至竖屏
                                driver.orientation = 'PORTRAIT'
                                time.sleep(3)
                        except Exception as e:
                                logging.warning(package + "无法横竖屏旋转")

                elif driver.orientation == 'PORTRAIT':
                        try:
                                #旋转至横屏
                                driver.orientation = 'LANDSCAPE'
                                #旋转至竖屏
                                driver.orientation = 'PORTRAIT'
                                time.sleep(3)
                        except Exception as e:
                                logging.warning(package + "无法横竖屏旋转")

        else:
                print(package+"为第三方应用，不旋转")
#权限允许
def isPermission():
        # 获取当前应用的包名
        package = current_package()
        try:
                 while driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button"):
                        driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()
                        time.sleep(5)
        except NoSuchElementException:
                print(package+"权限全被允许")
        except Exception as e:
            logging.error(e)

#应用是否停止运行
def isError():
        #获取当前应用的包名
        package = current_package()
        try:
                if driver.find_element_by_id("android:id/alertTitle"):
                        print(driver.find_element_by_id("android:id/alertTitle").text)
        except NoSuchElementException:
                print(package+"应用未报错")
        except Exception as e:
            logging.error(e)

#应用是否闪退
def isFlashBack(n):
    #获取当前应用的包名
    package = current_package()
    try:
        if package == lanucher_package:
            logging.error("第"+str(n+1)+"个应用闪退")
        else:
            print(package+"应用未闪退")
    except Exception as e:
        logging.error(e)
#创建文件夹
create_file()
#点检
for s in range(1,screen_total(total,sums)+1):
    if s <= screen_total(total,sums):
            print("第"+str(s)+"屏")
            if s == 1:
                if total <= sums:
                    for n in range(0,total):
                        print("第"+str(n+1)+"个应用： ")
                        click(n,s)
                else:
                    for n in range(sums):
                        print("第"+str(n+1)+"个应用： ")
                        click(n,s)
            else:
                if s == screen_total(total,sums):
                    for n in range(sums-col*(row_total(total,sums,col)-1),sums-col*(row_total(total,sums,col)-1)+(total - sums * (screen_total(total, sums) - 1))):
                        print("第"+str(n+1)+"个应用： ")
                        click(n,s)
                else:
                    for n in range(col,sums+col):
                        print("第"+str(n+1)+"个应用： ")
                        click(n,s)



