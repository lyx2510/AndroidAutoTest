# _*_ coding:utf-8 _*_
import uiautomator2 as u2
from uiautomator2 import UiObjectNotFoundError
import logging
import logging.config
import os
import time


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


#重写click操作
def click(d,n):
    try:
        d[n].click()
    except UiObjectNotFoundError:
        title = d2.info['text']
        logging.info(title+"页面上第"+str(n)+"行无法点击")

#向上滑
def swipeUp():
    #获取长、宽
    x = d.window_size()[0]
    y = d.window_size()[1]
    d.swipe(0.5*x,y-80,0.5*x,0,1)

#获取元素text值
def get_text(d,n):
    try:
        time.sleep(1)
        text_info = d[n].info['text']
        return text_info
    except UiObjectNotFoundError:
        logging.info("找不到元素")

#计算当前列表的数量
def cal_count():
    try:
       time.sleep(1)
       count = d1.count
       #当有列表时
       if count != 0:
           #判断当前列表中是否有高级字符
            for i in range(count):
                list1 = get_text(d1,i)
                if list1 in advanced:
                    print("已展开Advanced项........")
                    click(d1,i)
                    time.sleep(2)
                    return d1.count
            else:
                return count
       else:
           return count
    except UiObjectNotFoundError:
        count = 0
        return count

#计算当前元素的位置
def current_position(text_value):
    #先获取当前的位置
    current_count = d1.count
    #遍历一遍当前列表
    for i in range(current_count):
        current_text = get_text(d1,i)
        if current_text == text_value:
            return i

def is_button1():
    try:
        while d(resourceId='android:id/button1').exist:
            d(resourceId='android:id/button1').click()
    except Exception as e:
        print("无弹窗")

# 第二层点击
def order_click():
    list_count = cal_count()
    #当前列表数值不为0
    if list_count != 0:
        first_title = d2.info['text']
        for i in range(list_count):
            second_click = get_text(d1,i)
            print("   第二层：第"+str(i+1)+"个："+second_click)
            click(d1,i)
            time.sleep(1)
            is_button1()
            second_back(first_title)
        last1 = get_text(d1,list_count-1)
        swipeUp()
        list2_count = d1.count
        last2 = get_text(d1,list2_count-1)
        if  last2 != last1:
            #获取last的位置
            j = current_position(last1)
            for i in range(j+1,list2_count):
                second_click = get_text(d1,i)
                print("   第二层：第"+str(i+1)+"个："+second_click)
                click(d1,i)
                time.sleep(1)
                is_button1()
                second_back(first_title)
    d.press("back")

#第2层进入后判断
def second_back(title):
    try:
        second_title = d2.info['text']
        # 跳转页面则返回
        if title != second_title:
            d.press("back")
            print("已跳转页面"+second_title)
    except Exception as e:
        d.press("back")
        print("未跳转页面"+title)

def first_click(m,n):
    for i in range(m,n):
        #记录当前的text值
        text = get_text(d1,i)
        print("第一层：第"+str(i+1)+"个："+text)
        click(d1,i)
        time.sleep(1)
        # 依次点击子列表
        order_click()
    #获取last的text值
    last1 = get_text(d1,n-1)
    time.sleep(2)
    swipeUp()
    time.sleep(1)
    j = d1.count
    time.sleep(1)
    last2 = get_text(d1,j-1)
    if last2 != last1:
        #获取last的位置
        x = current_position(last1)
        for i in range(x+1,j):
            #记录当前的text值
            text = get_text(d1,i)
            print("第一层：第"+str(i+1)+"个："+text)
            click(d1,i)
            time.sleep(1)
            # 依次点击子列表
            order_click()

if __name__ == '__main__':
    d = u2.connect() # connect to device
    d.app_start("com.android.settings")
    devices = d.info
    system = ['About phone','关于手机']
    system = set(system)
    advanced = ['Advanced','高级']
    advanced = set(advanced)
    #定位
    d1 = d(className='android.widget.LinearLayout').child(resourceId='android:id/title')
    d2 = d(resourceId='com.android.settings:id/action_bar').child(className='android.widget.TextView')
    #删除log文件
    delete_log()
    #加载日志配置文件
    CON_LOG = '../conf/log.conf'  #注意是log.conf所在的路径
    logging.config.fileConfig(CON_LOG)
    logging = logging.getLogger()
    time.sleep(1)
    count1 = d1.count
    first_click(0,count1)



