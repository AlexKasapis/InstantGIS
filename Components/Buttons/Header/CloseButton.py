import win32gui
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class CloseButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(CloseButton, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(40, 30))
        self.setText("")
        self.setIcon(QIcon("./Resources/Icons/icon_close.png"))
        self.setIconSize(QSize(25, 25))
        self.setStyleSheet('''
            background-color: #323232;
            border: 0px''')
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        QCoreApplication.quit()

    def enterEvent(self, event):
        self.setStyleSheet('''
        background-color: #ec1c2a;
        border: 0px''')

    def leaveEvent(self, event):
        self.setStyleSheet('''
        background-color: #323232;
        border: 0px''')

    def mousePressEvent(self, event):
        super(CloseButton, self).mousePressEvent(event)
        event.accept()
