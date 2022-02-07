import PyQt5
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.number = 0

        self.title = 'PyQt test(QMainWindow)'
        self.width = 400
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        
        self.create_widgets()

        # ROS2 init
        rclpy.init(args=None)
        self.node = Node('button_main')
        self.pub = self.node.create_publisher(Int32, 'button_topic', 10)

    def __del__(self):
        self.node.destroy_node()
    
    def create_widgets(self):
        self.button = QtWidgets.QPushButton('Button', self)
        self.button.move(100, 50)
        self.button.clicked.connect(self.button_update)

        # create label
        self.label = QLabel(self)
        self.label.setText('0')
        self.label.move(100, 100)
        # create timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(1000)

    def button_update(self):
        self.number -= 1
        self.pub_int32(self.number)
    
    def timer_update(self):
        self.number += 1
        self.pub_int32(self.number)
        self.label.setText(str(self.number))
        # show
        self.show()
        # update after 1 second
        self.timer.start(1000)
        
    # --- ros2 publish ---
    def pub_int32(self, number: int):
        time_msg = Int32()
        time_msg.data = number
        self.pub.publish(time_msg)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())