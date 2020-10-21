import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets


class HelpButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(HelpButton, self).__init__(*args, **kwargs)

        self.setFixedSize(QtCore.QSize(40, 30))
        self.setText("")
        self.setIcon(QtGui.QIcon("./Resources/Icons/icons8-question-mark-48.png"))
        self.setIconSize(QtCore.QSize(25, 25))
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        print("Clicked on the Help Button!")

    def enterEvent(self, event):
        self.setStyleSheet('''background-color: #ec1c2a;''')

    def leaveEvent(self, event):
        self.setStyleSheet('''background-color: green;''')
