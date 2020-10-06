import win32gui, win32con
from PyQt5 import QtCore, QtGui, QtWidgets


class MaximizeButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(MaximizeButton, self).__init__(*args, **kwargs)

        self.setFixedSize(QtCore.QSize(40, 30))
        self.setText("")
        self.setIcon(QtGui.QIcon("icons/icon_maximize.png"))
        self.setIconSize(QtCore.QSize(25, 25))
        self.setStyleSheet('''
            background-color: #323232;
            border: 0px''')
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MAXIMIZE)

    def enterEvent(self, event):
        self.setStyleSheet('''
        background-color: #555555;
        border: 0px''')

    def leaveEvent(self, event):
        self.setStyleSheet('''
        background-color: #323232;
        border: 0px''')

