
import sys
from openai import OpenAI
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from threading import Thread


#借鉴往上配置的风格
scrollStyle="""
QScrollBar:vertical {
border-width: 0px;
border: none;
background: white;
width:12px;
margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
stop: 0 gray, stop: 0.5 gray, stop:1 gray); 
min-height: 20px;
max-height: 20px;
margin: 0 0px 0 0px;
border-radius: 6px;
}
QScrollBar::add-line:vertical {
background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
height: 0px;
border: none;
subcontrol-position: bottom;
subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
height: 0 px;
border: none;
subcontrol-position: top;
subcontrol-origin: margin;
}
QScrollBar::sub-page:vertical {
background: white;
}
QScrollBar::add-page:vertical {
background: white;
}
"""
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
    base_url="https://api.chatanywhere.tech/v1"
)

# text_generator = TextGenerationPipeline(model, tokenizer)   
class Talk(QWidget):
    # 初始化界面
    def __init__(self, parent=None, **kwargs):
        super(Talk, self).__init__(parent)
        self.setWindowTitle("聊天室")
        self.setGeometry(600, 300, 600, 337)

        # 添加背景
        palette = QPalette()
        bg = QPixmap("resources/png/background")
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(bg))
        self.setPalette(palette)

        # 创建主布局
        main_layout = QGridLayout()  
        main_layout.setSpacing(20) 
        # 创建多行文本显示，显示所有的聊天信息
        # self.content = QTextBrowser()
        # self.content.setStyleSheet("font-family: Arial; font-size: 10pt; color: #333; background-color: #FFF;border-radius:10px")
        
        
        # main_layout.addWidget(self.content,1,0,1,10)
        # 创建滚动区域"font-family: Arial; font-size: 10pt; color: #333; background-color: #FFF;border-radius:10px"
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(scrollStyle)

        scroll_area.setWidgetResizable(True)
        
        # 创建聊天消息显示区域
        self.chat_layout = QVBoxLayout()
        chat_widget = QWidget()
        chat_widget.setLayout(self.chat_layout)
        scroll_area.setWidget(chat_widget)
        
        main_layout.addWidget(scroll_area,1,0,1,10)

        # 创建单行文本，消息发送框
        self.message = QLineEdit()
        self.message.setPlaceholderText("请输入发送内容")
        self.message.setStyleSheet("font-family: Arial; font-size: 10pt; color: #333; background-color: #FFF;border-radius:5px;padding-top: 5px; padding-bottom: 5px;")

        main_layout.addWidget(self.message,2,0,1,10)

        # 创建发送按钮
        self.button = QPushButton("发送")
        self.button.setFont(QFont("微软雅黑", 10, QFont.Bold))
        main_layout.addWidget(self.button,3,9,1,1,alignment=Qt.AlignRight)
        
        self.setLayout(main_layout) 

        # 启动线程
        self.work_thread()


   #参考https://github.com/chatanywhere/GPT_API_free/blob/main/demo.py 
    def gpt_35_api(self,messages: list):
        """为提供的对话消息创建新的回答 (流式传输)

        Args:
            messages (list): 完整的对话消息
        """
        
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        self.add_pikachu_message(completion.choices[0].message.content)
        # self.content.append(" Pikachu: "+completion.choices[0].message.content)
        
    def add_user_message(self, message):
        user_frame = QFrame()
        user_layout = QVBoxLayout()
        user_label = QLabel("I:")
        user_text = QTextBrowser()
        user_text.setStyleSheet("font-family: Arial; font-size: 10pt; color: #333; background-color: #FFF;border-radius:10px")
        user_text.setPlainText(message)
        user_text.verticalScrollBar().setStyleSheet
        # 获取字体信息
        font_metrics = QFontMetrics(user_text.font())
        # 获取文本行数，由于存在边框故人为增加6行以保持消息框的正常显示
        lines = message.count('\n') + 6
        # 获取每行的高度
        line_height = font_metrics.lineSpacing()
        # 计算QTextBrowser的高度
        height = lines * line_height
        # 设置QTextBrowser的大小
        user_text.setFixedHeight(height)
        user_layout.addWidget(user_label)
        user_layout.addWidget(user_text)
        user_frame.setLayout(user_layout)
        user_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 10px; margin-bottom: 10px;")
        user_frame.setFixedHeight(height+100)
        self.chat_layout.addWidget(user_frame)
        self.scroll_down()
    
    def add_pikachu_message(self, message):
        assistant_frame = QFrame()
        assistant_layout = QVBoxLayout()
        assistant_label = QLabel("Pikachu:")
        assistant_text = QTextBrowser()
        assistant_text.setStyleSheet("font-family: Arial; font-size: 10pt; color: #333; background-color: #FFF;border-radius:10px")
        assistant_text.setPlainText(message)
        # 获取字体信息
        font_metrics = QFontMetrics(assistant_text.font())
        # 获取文本行数
        lines = message.count('\n') +6
        # 获取每行的高度
        line_height = font_metrics.lineSpacing()
        # 计算QTextBrowser的高度
        height = lines * line_height
        # 设置QTextBrowser的大小
        assistant_text.setFixedHeight(height)
        assistant_layout.addWidget(assistant_label)
        assistant_layout.addWidget(assistant_text)
        assistant_frame.setLayout(assistant_layout)
        assistant_frame.setStyleSheet("background-color: #e0e0e0; border-radius: 10px; padding: 10px; margin-bottom: 10px;")
        assistant_frame.setFixedHeight(height+100)
        self.chat_layout.addWidget(assistant_frame)
        self.scroll_down()
    
    def scroll_down(self):
        # 滚动到最后一条消息
        scroll_bar = self.findChild(QScrollBar)
        if scroll_bar:
            scroll_bar.setValue(scroll_bar.maximum())

    # 发送消息 + 接收消息
    def send_msg(self):
        msg = self.message.text()
        # self.content.append(" I: " + msg)
        self.add_user_message(msg)
        if msg.upper() == "Q":
            self.destroy()
        self.message.clear()
        # text_generator(str(msg), max_length=50, do_sample=True)
        messages = [{'role': 'user','content': str(msg)},]
        self.gpt_35_api(messages)
        

 
    # 点击按钮发送消息
    def btn_send(self):
        self.button.clicked.connect(self.send_msg)
 
    # 线程处理
    def work_thread(self):
        Thread(target=self.btn_send).start()
       

    # 推出销毁对话窗口
    def closeEvent(self, event):
        self.destroy()


if __name__ == '__main__':
    # 创建了一个QApplication对象
    app = QApplication(sys.argv)
    # 窗口组件初始化
    Talk = Talk()
    Talk.show()

    sys.exit(app.exec_())
