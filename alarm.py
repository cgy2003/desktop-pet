import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTimeEdit, QListWidget, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer, QTime

class AlarmClock(QWidget):
    #初始化界面
    def __init__(self, parent=None, **kwargs):
        super(AlarmClock, self).__init__(parent)
        self.setWindowTitle("闹钟")
        self.setGeometry(100, 100, 400, 300)

        self.setup_database()
        
        layout = QVBoxLayout()

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm")
        layout.addWidget(self.time_edit)

        self.save_button = QPushButton("保存闹钟")
        self.save_button.clicked.connect(self.save_alarm)
        layout.addWidget(self.save_button)

        self.alarms_list = QListWidget()
        layout.addWidget(self.alarms_list)

        buttons_layout = QHBoxLayout()

        self.modify_button = QPushButton("修改闹钟")
        self.modify_button.clicked.connect(self.modify_alarm)
        buttons_layout.addWidget(self.modify_button)

        self.delete_button = QPushButton("删除闹钟")
        self.delete_button.clicked.connect(self.delete_alarm)
        buttons_layout.addWidget(self.delete_button)

        layout.addLayout(buttons_layout)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.now_time)
        self.timer.start(1000)

        self.load_alarms_from_database()

    def setup_database(self):
        self.conn = sqlite3.connect('alarms.db')
        self.c = self.conn.cursor()
        #创建表（如果不存在的话）
        self.c.execute('''CREATE TABLE IF NOT EXISTS alarms (id INTEGER PRIMARY KEY AUTOINCREMENT, alarm_time TEXT)''')
        self.conn.commit()

    def save_alarm(self):
        alarm_time = self.time_edit.time().toString("hh:mm")
        if not self.is_duplicate_alarm(alarm_time):
            self.label.setText(f"闹钟已保存为 {alarm_time}")
            self.save_alarm_to_database(alarm_time)
            self.load_alarms_from_database()
        else:
            QMessageBox.warning(self, "警告", "相同时间的闹钟已存在，请选择其他时间")

    def is_duplicate_alarm(self, alarm_time):
        self.c.execute('''SELECT * FROM alarms WHERE alarm_time = ?''', (alarm_time,))
        return len(self.c.fetchall()) > 0

    def save_alarm_to_database(self, alarm_time):
        self.c.execute('''INSERT INTO alarms (alarm_time) VALUES (?)''', (alarm_time,))
        self.conn.commit()

    #从数据库加载时间信息
    def load_alarms_from_database(self):
        self.alarms_list.clear()
        alarms = self.get_all_alarms_from_database()
        for alarm in alarms:
            self.alarms_list.addItem(alarm[1])

    #处理修改事件
    def modify_alarm(self):
        selected_item = self.alarms_list.currentItem()
        if selected_item:
            new_time = self.time_edit.time().toString("hh:mm")
            old_time = selected_item.text()
            if not self.is_duplicate_alarm(new_time):
                self.label.setText(f"修改闹钟时间: {old_time} -> {new_time}")
                self.modify_alarm_in_database(old_time, new_time)
                self.load_alarms_from_database()
            else:
                QMessageBox.warning(self, "警告", "相同时间的闹钟已存在，请选择其他时间")
    #修改数据库的时间
    def modify_alarm_in_database(self, old_time, new_time):
        self.c.execute('''UPDATE alarms SET alarm_time = ? WHERE alarm_time = ?''', (new_time, old_time))
        self.conn.commit()
    #处理删除事件
    def delete_alarm(self):
        selected_item = self.alarms_list.currentItem()
        if selected_item:
            alarm_time = selected_item.text()
            self.label.setText(f"删除闹钟时间: {alarm_time}")
            self.delete_alarm_from_database(alarm_time)
            self.load_alarms_from_database()
    #从数据库删除闹钟信息
    def delete_alarm_from_database(self, alarm_time):
        self.c.execute('''DELETE FROM alarms WHERE alarm_time = ?''', (alarm_time,))
        self.conn.commit()

    def now_time(self):
        current_time = QTime.currentTime().toString("hh:mm")
        self.label.setText("当前时间："+current_time)
        

    def get_all_alarms_from_database(self):
        self.c.execute('''SELECT * FROM alarms''')
        return self.c.fetchall()
    
    def closeEvent(self, event):
        self.destroy()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = AlarmClock()
    clock.show()
    sys.exit(app.exec_())
