import uiautomator2 as u2
from uiautomator2 import SessionBrokenError, UiObjectNotFoundError
import time


#设置apk点检
def settingstest_byname():
    try:
        d.set_orientation('n')
        setting=d.session("com.android.settings")
        time.sleep(1)
        if setting(text="Network & internet").exists:
            now_touch="Network & internet"
            next_touch=setting(text="Network & internet").down(resourceId="android:id/title").info["text"]
        elif setting(text="网络和互联网").exists:
            now_touch ="网络和互联网"
            next_touch=setting(text="网络和互联网").down(resourceId="android:id/title").info["text"]
        else:
            print("未找到设置相关元素")
            return
        #next_touch ='System'#setting(resourceId="android:id/title")[14].info["text"]
        needseip=0
        while 1:
            try:
                print("————",now_touch)
                setting(text=now_touch).click()
                if(now_touch=="Google"):
                    time.sleep(1)
                depth(setting)
                setting.press("back")
                time.sleep(0.3)
                if version=="10":
                    time.sleep(1)#系统卡顿则把等待时间延长
                now_touch=next_touch
                if needseip==1:
                    d.swipe_ext("up")
                next_touch = setting(text=now_touch).down(resourceId="android:id/title").info["text"]
            except AttributeError as e:
                if version=="9"and now_touch in ["System","系统"] or version=="10"and now_touch in ["关于手机","About phone","关于平板电脑","About table"]:
                    print("————", now_touch)
                    setting(text=now_touch).click()
                    depth(setting)
                    setting.press("back")
                    print("设置点击完毕")
                    return
                elif needseip==0:
                    needseip=1
                    d.swipe_ext("up")
                    next_touch = setting(text=now_touch).down(resourceId="android:id/title").info["text"]
                else:
                    print(str(e))
            except UiObjectNotFoundError as e:
                d.screenshot("home.jpg")
                image = d.screenshot()
                image.save("home.jpg")
    except SessionBrokenError as e:
        print(now_touch +str(e))


#第二层目录检查
def depth(session):
    try:
        title=session(className='android.view.ViewGroup').child(className='android.widget.TextView')
        title1=title.info["text"]
        try_time=0
        #等待页面进入
        while  1:
            if title.exists:
                #print(session(resourceId="android:id/title")[1].exists,session(resourceId='com.google.android.apps.wellbeing:id/title')[1].exists)
                if session(resourceId="android:id/title")[0].exists :
                    resource_Id="android:id/title"
                    break
                elif session(resourceId='com.google.android.apps.wellbeing:id/title')[0].exists:
                    resource_Id = 'com.google.android.apps.wellbeing:id/title'
                    break
                elif session(resourceId='com.google.android.gms:id/title')[0].exists:
                    resource_Id = 'com.google.android.gms:id/title'
                    break
            try_time = try_time + 1
            if try_time==10:
                print('Error:该页面未找到元素')
                return

        count2 = session(className='android.widget.LinearLayout').child(resourceId=resource_Id).count
        #print(count2)
        last1=session(resourceId=resource_Id)[count2 - 1]
        t1 = last1.info["text"] in ["高级", "Advanced"]
        if t1 or session(resourceId=resource_Id)[count2 - 2].info["text"] in ["高级", "Advanced"]:
            if t1:
                last1.click()
            else:
                session(resourceId=resource_Id)[count2 - 2].click()
            time.sleep(0.5)
            count2 = session(className='android.widget.LinearLayout').child(resourceId=resource_Id).count
            last1 = session(resourceId=resource_Id)[count2 - 1]
        lasttext=last1.info["text"]
        swipe=0
        i=count2-1
        fisttext = session(resourceId=resource_Id)[0].info["text"]
        while i>=0:
            current = session(resourceId=resource_Id)[i]
            next = current.info["text"]
            #print(next)
            if swipe==1 and next==lasttext:
                return
            current.click()
            if "Google"in next:
                time.sleep(0.5)
            print(next)
            is_gone = current.wait_gone(timeout=0.5)
            if is_gone!=True and fisttext==session(resourceId=resource_Id)[0].info["text"]:
                pass
            else:
                session.press("back")
                if session(resourceId='android:id/button2').exists:
                    session(resourceId='android:id/button2').click()
                elif fisttext!=session(resourceId=resource_Id)[0].info["text"]:
                    session.press("back")
            if i==0:

                d.swipe_ext("up")
                if  fisttext!=session(resourceId=resource_Id)[0].info["text"]:
                    swipe=1
                    i = session(className='android.widget.LinearLayout').child(resourceId=resource_Id).count
                    fisttext=session(resourceId=resource_Id)[0].info["text"]
            i = i - 1

    except SessionBrokenError as e:
        print(next +str(e))


if __name__ == '__main__':
    d = u2.connect() # connect to device
    d.settings['operation_delay_methods'] =['click', 'swipe','info']
    device=d.device_info
    version=device["version"]
    display=device["display"]
    #depth(d)
    settingstest_byname()