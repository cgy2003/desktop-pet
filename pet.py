import os
import sys
import time
import random

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from talk import Talk
from alarm import AlarmClock
import datetime
import sqlite3
class Config():
  # resource文件夹
  ROOT_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resources')

  PET_ACTIONS_MAP = dict()
  # 自定义宠物动作分布情况
  PET_ACTIONS_MAP = [
          [str(i) for i in range(1, 56)],
        [str(i) for i in range(56, 112)],
        
        [str(i) for i in range(112, 173)],
        [str(i) for i in range(173, 229)],
        

  ]
  PET_STATIC=[
      [str(i) for i in range(229,269)]
      ] 

class WindowPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(WindowPet, self).__init__(parent)
        #主体初始化
        self.init()
        self.init_tray()
        self.init_menu()
    def init(self):
        
        self.hide_open=0
        self.time=0 
        self.cfg=Config()
        #重新定义窗口性质
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 导入宠物
        self.pet_images,self.pet_move_images = self.LoadPetImage()
        self.is_move_action=False
        # 当前显示的图片
        self.image = QLabel(self)
        #初始化第一个动作
        self.action_pointer=0
        self.setImage(self.pet_images[0][self.action_pointer])
        #初始化变量
        self.is_running_action=False
        
        #定时做动作
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeAction)
        self.timer.start(50)
        
        
        #整点报时
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.checkTime)
    
        self.timer2.start(1000)

        self.bubble = QLabel(self.parent())
        self.bubble.setWindowFlags(Qt.SplashScreen)
        
        
        self.bubble.setStyleSheet("background-color: white; border-radius: 10px; padding: 5px;")
        self.bubble.hide()

        shadow_effect = QGraphicsDropShadowEffect(blurRadius=5, xOffset=2, yOffset=2)
        self.bubble.setGraphicsEffect(shadow_effect)
        # 将bubble的位置与image的位置绑定，使得image位置移动，bubble也移动
        self.updateBubblePosition()
        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.updateBubblePosition)
        self.timer3.start(50)

        #时间显示
        self.show_time_time = QLabel()
        self.time_open=1
        # 对话框样式设计
        self.show_time_time.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")

        #闹钟
        self.timer4 = QTimer()
        self.timer4.timeout.connect(self.check_alarm)
    
        self.timer4.start(1000)
        self.show()
    def init_tray(self):
        # 添加托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join(Config.ROOT_DIR, 'png', 'shime1.png')))
        
        # 创建托盘菜单
        self.tray_menu = QMenu()
        
        # 添加菜单项

        hide_action = self.tray_menu.addAction("隐藏")
        
        question_answer_action = self.tray_menu.addAction("聊天室")
        
        
        time_anhour_action = self.tray_menu.addAction("打开整点报时")
        
        alarm_action = self.tray_menu.addAction("设置闹钟")
        self.tray_menu.addSeparator()
        exit_action = self.tray_menu.addAction("退出")
        
        # 连接菜单项的触发信号到相应的槽函数
        
        hide_action.triggered.connect(self.hide_application)
        question_answer_action.triggered.connect(self.show_question_answer)
        exit_action.triggered.connect(self.exit_application)
        time_anhour_action.triggered.connect(self.time_reminder)
        alarm_action.triggered.connect(self.set_alarm)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
    def init_menu(self):
        # 定义菜单
        self.menu = QMenu(self)
        
        # 定义菜单项

        self.hide_action = self.menu.addAction("隐藏")
       
        self.question_answer_action = self.menu.addAction("聊天室")
        

        self.time_anhour_action = self.menu.addAction("打开整点报时")
        self.alarm_action = self.menu.addAction("设置闹钟")
        self.menu.addSeparator()
        self.exit_action = self.menu.addAction("退出")
    def contextMenuEvent(self, event):     
        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = self.menu.exec_(self.mapToGlobal(event.pos()))
        
        # 连接菜单项的触发信号到相应的槽函数
        if action == self.exit_action:
            self.exit_application()
        elif action == self.hide_action:
            self.hide_application()
        elif action == self.question_answer_action:
            self.show_question_answer()
        elif action ==self.time_anhour_action:
            self.time_reminder()
        elif action == self.alarm_action:
            self.set_alarm()



    def hide_application(self):
        if self.hide_open == 0:
            self.setWindowOpacity(0)
            self.hide_open=1
            hide_action = self.tray_menu.actions()[0]  
            hide_action.setText("显示")
        elif self.hide_open == 1:
            self.setWindowOpacity(1)
            self.hide_open=0
            hide_action = self.tray_menu.actions()[0]  
            hide_action.setText("隐藏")
    def show_question_answer(self):
        self.talk=Talk()
        self.talk.show()
    def time_reminder(self):
        if self.time == 0:
            self.time=1
            time_action = self.tray_menu.actions()[2] 
            time_action.setText("关闭整点报时")
            time_action_menu = self.menu.actions()[2] 
            time_action_menu.setText("关闭整点报时")
        elif self.time == 1:
            self.time=0 
            time_action = self.tray_menu.actions()[2] 
            time_action.setText("打开整点报时")
            time_action_menu = self.menu.actions()[2] 
            time_action_menu.setText("打开整点报时")
    
    def set_alarm(self):
        self.alarm=AlarmClock()
        self.alarm.show()
    def get_all_alarms_from_database(self):
        self.conn = sqlite3.connect('alarms.db')
        self.c = self.conn.cursor()
        self.c.execute('''SELECT * FROM alarms''')
        return self.c.fetchall()
    def check_alarm(self):
        current_time = QTime.currentTime().toString("hh:mm")
        
        alarms = self.get_all_alarms_from_database()
        for alarm in alarms:
            if current_time == alarm[1] :
                # 创建气泡提示框
                
                self.bubble.setText(f"闹钟响了，现在是北京时间{current_time}")
                self.bubble.show()                
                
                timer = QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(self.bubble.hide)
                timer.start(60000)

    def checkTime(self):
        current_time = QTime.currentTime()
        if self.time == 1 and current_time.second() == 0 and current_time.minute()==0:
            # current_time.second() == 0 and 
            self.showReminder()
    def showReminder(self):
        # 创建气泡提示框
        current_time = datetime.datetime.now().strftime("%H")
    
        # 创建气泡提示框
        self.bubble.setText(f"现在是北京时间{current_time}点")
        self.bubble.show()

        
        # 定时器，十秒后自动关闭气泡提示框
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.bubble.hide)
        timer.start(10000)
    
    #绑定气泡与宠物
    def updateBubblePosition(self):
        pet_pos = self.frameGeometry()
        self.bubble.move(pet_pos.right() - self.bubble.width()+30, pet_pos.top()+120)
    #换动作
    def changeAction(self):
        #加载运动动作
        if self.is_move_action:
            self.is_move_action = False
            self.action_images = random.choice(self.pet_move_images)
            self.action_max_len = len(self.action_images)
            self.action_pointer = 0
        else :
            #静止的动作
            if not self.is_running_action:
                self.is_running_action = True
                self.action_images = random.choice(self.pet_images)
                self.action_max_len = len(self.action_images)
                self.action_pointer = 0
        self.runFrame()
    #播放一个动作的每一帧
    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_running_action = False
            self.action_pointer = 0
            self.action_max_len = 0
        self.setImage(self.action_images[self.action_pointer])
        self.action_pointer += 1
    #加载宠物图片和图标
    def LoadPetImage(self):
        cfg=self.cfg
        actions = cfg.PET_STATIC
        pet_images = []
        move_actions = cfg.PET_ACTIONS_MAP
        pet_move_images = []
        #按照自定义的动作顺序加载图片(静止和运动图片分开加载)
        for action in actions:
            pet_images.append([self.loadImage(os.path.join(cfg.ROOT_DIR, 'png', item+'.png')) for item in action])
        for action in move_actions:
            pet_move_images.append([self.loadImage(os.path.join(cfg.ROOT_DIR, 'png', item+'.png')) for item in action])
        return pet_images,pet_move_images
    
    def loadImage(self, path):
        image=QImage()
        image.load(path)
        return image

    # def setImage(self, image):
    #     self.image.setPixmap(QPixmap.fromImage(image))
    #     self.image.setGeometry(0, 0, image.width(), image.height())
    #     self.image.show()
    def setImage(self, image):
        # 获取原始图像宽高
        original_width = image.width()
        original_height = image.height()

        # 设置目标宽度
        target_width = 300  # 你可以根据需要设置目标宽度

        # 计算保持宽高比例的高度
        ratio = target_width / original_width
        target_height = int(original_height * ratio)

        # 调整图像大小并保持平滑
        resized_image = image.scaled(target_width, target_height, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

        # 将调整大小后的图像设置为 QPixmap，并显示
        self.image.setPixmap(QPixmap.fromImage(resized_image))
        self.image.setGeometry(0, 0, resized_image.width(), resized_image.height())
        self.image.show()
    
    #加载宠物在某一位置
    def randomPosition(self):
        
        screen_pos = QDesktopWidget().screenGeometry()
       
        pet_pos = self.geometry()
        
        x = random.randint(0, screen_pos.width() - pet_pos.width())
        y = random.randint(0, screen_pos.height() - pet_pos.height())
        
        self.move(x, y)
    #按下鼠标
    def mousePressEvent(self, event):
        #捕获鼠标左键按下瞬间
        if event.buttons() == Qt.LeftButton:
            #计算拖动位置并需要加载move动作
            self.is_move_action=True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    # 移动鼠标
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    

    #退出宠物
    def exit_application(self):
        self.tray_icon.hide()
        self.close()
        sys.exit()

   

if __name__ == "__main__":
  app = QApplication(sys.argv)
  desktop_pet = WindowPet()
  sys.exit(app.exec_())