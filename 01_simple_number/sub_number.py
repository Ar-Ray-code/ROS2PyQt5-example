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

        self.title = 'PyQt test(Subscriber)'
        self.width = 400
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        
        self.create_widgets()

        # ROS2 init
        rclpy.init(args=None)
        self.node = Node('button_sub')
        self.pub = self.node.create_subscription(Int32, 'button_topic', self.sub_int32, 10)
        # spin once
        rclpy.spin_once(self.node)

    def __del__(self):
        self.node.destroy_node()
    
    def create_widgets(self):
        # create label
        self.label = QLabel(self)
        self.label.setText(str(self.number))
        self.label.move(100, 100)
        self.show()

        # create timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(10)
    
    def timer_update(self):
        rclpy.spin_once(self.node)
        self.update_label()
        # show
        self.show()
        # update after 1 second
        self.timer.start(10)

    def update_label(self):
        self.label.setText(str(self.number))
        # show
        self.show()
    
    def sub_int32(self, msg):
        self.number = msg.data
        # rclpy.spin_once(self.node)
        print(self.number)
        self.update_label()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())