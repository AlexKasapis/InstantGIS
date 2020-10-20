import win32gui, win32con
from PyQt5 import QtCore, QtGui, QtWidgets


class MinimizeButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(MinimizeButton, self).__init__(*args, **kwargs)

        self.setFixedSize(QtCore.QSize(40, 30))
        self.setText("")
        self.setIcon(QtGui.QIcon("icons/icon_minimize.png"))
        self.setIconSize(QtCore.QSize(25, 25))
        self.setStyleSheet('''
            background-color: #323232;
            border: 0px''')
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MINIMIZE)

    def enterEvent(self, event):
        self.setStyleSheet('''
        background-color: #555555;
        border: 0px''')

    def leaveEvent(self, event):
        self.setStyleSheet('''
        background-color: #323232;
        border: 0px''')

    def mousePressEvent(self, event):
        super(MinimizeButton, self).mousePressEvent(event)
        event.accept()

