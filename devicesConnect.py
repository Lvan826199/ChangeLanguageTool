import time
import datetime
import uiautomator2 as u2
from ChangeLanguageScript.changeLanguage_Test4.readSerialNumber import adbDevices
from ChangeLanguageScript.changeLanguage_Test4.readExcelFile import RWExcel
from ChangeLanguageScript.changeLanguage_Test4.writeExcel import Write_excel


class readWarningTest():
    def __init__(self):
        # 连接手机
        print("正在获取设备的SN号")
        SN = adbDevices().readSN()  # 获取涉笔的SN号
        print("获取成功，设备的SN号为：" + SN)
        time.sleep(5)
        print("正在连接设备")
        self.d = u2.connect(SN)  # HA12FYBL\HA12G0GW\HA169RPZ填入设备的SN号即可
        self.sizeTuple = self.d.window_size()

        print("设备连接成功，先回到主页面")

    def readWarning(self,Changelanguage):
        """

        :param Changelanguage: 需要切换的语言
        :return: 返回切换语言之后的warningtext
        """

        self.d.press('home')
        print("回到主页面成功，正在把屏幕调到自然方向")
        time.sleep(3)
        self.d.set_orientation("n")  # or "natural"

        print("屏幕调整完成，正在启动应用")
        time.sleep(3)
        self.d.implicitly_wait(20)
        #启动应用
        self.d.app_start("com.android.settings")
        print("应用启动成功")
        #创建session连接对象，建议与设置应用的绑定连接
        s = self.d.session('com.android.settings',attach=True)
        time.sleep(3)
        #获取设备的尺寸
        print(self.d.window_size())

        x = self.sizeTuple[0]
        y = self.sizeTuple[1]
        print("屏幕的宽为："+str(x) +",屏幕的高为："+str(y)) #获取屏幕的宽高
        #1.进入设置之后，划动屏幕找到System
        time.sleep(3)
        print("---------------------开始滑屏---------------")
        self.d.swipe(x/5 * 4,y/5 * 4,x/5*4,y/5*1,1,50)
        self.d.swipe(x/5 * 4,y/5 * 4,x/5*4,y/5*1,1,50)
        self.d.implicitly_wait(5)
        #2.通过class和下标点击系统（开发者模式）
        self.d(className = 'android.widget.LinearLayout',index = '18').click()
        time.sleep(1)
        #3.点击语言和输入法
        self.d(className = 'android.widget.LinearLayout',index = '1').click()
        time.sleep(2)
        #4.点击语言
        self.d(className = 'android.widget.RelativeLayout',index = '1').click()
        time.sleep(2)
        #5.点击添加语言（此时页面仅可存在一个语言，其他语言需提前删除）（需判断目前显示的语言是否和要搜索的一致）
        self.d(resourceId = 'com.android.settings:id/add_language').click()

        #6.点击搜索
        self.d(resourceId = 'android:id/locale_search_menu').click()

        #7.输入需要更换的语言(此时要注意一个语言下面还有分支的情况)
        # Changelanguage = 'Čeština'  #Suomi Akan
        time.sleep(3)
        #7.1 单语言切换
        if "/" not in Changelanguage:
            self.d(resourceId = 'android:id/search_src_text').send_keys(Changelanguage)
            self.d.implicitly_wait(5)
            #8.1选择更换的语言,text要是选择的语言，有的语言会有推荐语言列表
            self.d(resourceId = 'android:id/locale',text = Changelanguage).click()

        time.sleep(1)

        #7.2 多语言切换（英语有很多页，需要滑动的,分开操作）
        if "/" in Changelanguage:
            print("含有/符号的value：{}".format(Changelanguage))  # 把含有/的value打印出来
            multilingual = Changelanguage.split("/")  # 分割好的语言放在这个里面
            print("--------------------------------")
            print("分割的", multilingual)
            hostLanguage = multilingual[0]   #获取多语言的主语言
            secondLanguage = multilingual[1]  #获取多语言的子语言
            time.sleep(3)

            if multilingual[0] == "English":
                self.d(resourceId='android:id/search_src_text').send_keys(hostLanguage)
                self.d.implicitly_wait(5)
                # 8.1点击主语言进入次语言的选择界面
                self.d(resourceId='android:id/locale',text = hostLanguage ).click()
                time.sleep(2)

                #寻找子语言，如果子语言不存在，则滚动屏幕，直到找到子语言，找到子语言则跳出循环，进行后面的操作
                flag = True
                while flag:
                    # 判断元素是否存在
                    time.sleep(5)
                    judgeElement = self.d(resourceId='android:id/locale', text=secondLanguage).exists
                    if judgeElement:
                        print("---------------次语言查找成功----------------")
                        self.d(resourceId='android:id/locale', text=secondLanguage).click()
                        flag = False
                    else:
                        x = self.sizeTuple[0]   #获取屏幕的宽
                        y = self.sizeTuple[1]   #获取屏幕的高
                        print("--------------滑屏寻找元素--------------")
                        # 1.进入设置之后，划动屏幕找到System
                        self.d.swipe(x / 5 * 4, y / 5 * 4, x / 5 * 4, y / 5 * 3, 1, 50)
                        self.d.swipe(x / 5 * 4, y / 5 * 4, x / 5 * 4, y / 5 * 3, 1, 50)



                #d(resourceId = 'android:id/locale',text = secondLanguage).click()

            else:   #不是英语的其他多语言
                self.d(resourceId='android:id/search_src_text').send_keys(hostLanguage)
                self.d.implicitly_wait(5)
                # 8.1点击主语言进入次语言的选择界面
                self.d(resourceId='android:id/locale', text = hostLanguage).click()
                time.sleep(2)
                self.d(resourceId='android:id/locale', text=secondLanguage).click()



        time.sleep(2)
        print("准备点击小点")
        #9.选择右上角的三个小点，remove
        self.d(className = 'android.widget.ImageButton',index='1').click()
        print("点好了")

        #10.点击移除（把选择之前的语言移除掉）
        self.d(resourceId = 'android:id/content').click()
        time.sleep(3)
        #11.勾选之前的语言（也就是第一个），这样把第一个删除之后，现在的语言就是需要更换的语言
        self.d(className = 'android.widget.RelativeLayout',index = '0').click() #点击第一个语言
        self.d(className = 'android.widget.TextView',index = '0').click() #点击删除
        #12.由于点击第一个删除会触发系统提示弹窗，则勾选ok就好
        self.d(resourceId = 'android:id/button1',index = '1').click()
        time.sleep(1)
        self.d.press("back") #返回到语言和输入法界面
        time.sleep(1)
        self.d.press("back") #返回到系统界面（开始进入系统更新对比）
        print("-------------------------开始进入系统更新对比------------------")

        #13.进入系统更新界面
        self.d(className = 'android.widget.LinearLayout',index = '8').click()

        #14.获取提示信息
        WaringText = self.d(resourceId = 'com.lenovo.ota:id/text_new_version_content').get_text(timeout=5)
        # print(WaringText)

        #14.获取到信息之后截屏，截图该屏幕并保存到同目录的screen文件中，图片名称为时间+语言
        nowTime = datetime.datetime.now().strftime('%m-%d-%H-%M-%S')
        self.d.screenshot("./screenshort/{}_{}.jpg".format(Changelanguage,nowTime))
        return WaringText

    # 15.把获取到的信息写入到表格中,使用获取到的信息和表格里面的信息进行对比
    def judgeResult(self):
        #获取select为1的行数和语言的键值对  eg.{3: 'Latviešu', 4: '日本語'}
        languageList = RWExcel().list_dic()
        print(languageList)
        for key, value in languageList.items():
            print("index:{},value:{}".format(key, value))
            # key作为第几行直接输入
            print("---------------------开始切换语言-------------")
            print("所切换的语言为：{}".format(value))
            msg = Run.readWarning(value)
            print(msg)
            print("-------------------开始把warning信息写入到对应表格中-------------------")
            write = Write_excel("Test.xlsx", key, msg)
            #把获取到的warning信息写入进入表格
            write.write()
            print("-------------------Warning信息写入成功--------------------------")
            print("----------------------开始对比系统提示与标准描述模板是否一致----------------")
            print("-------------------开始把测试结果写入到对应表格中-------------------")
            #把对比之后的测试结果写入到表格
            write.write_result()
            print("-------------------测试结果写入成功--------------------------")






if __name__ == '__main__':
    Run = readWarningTest()
    # language = "Dansk"
    #Run.readWarning("English/Tuvalu")
    Run.judgeResult()



