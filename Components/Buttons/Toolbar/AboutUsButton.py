import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets


class AboutUsButton(QtWidgets.QPushButton):
    def __init__(self, parent, controller, *args, **kwargs):
        super(AboutUsButton, self).__init__(*args, **kwargs)

        # Visuals
        self.setFixedSize(QtCore.QSize(37, 37))
        self.setText("")
        self.setIcon(QtGui.QIcon("./Resources/Icons/icon_about_us.png"))
        self.setIconSize(QtCore.QSize(30, 30))
        self.setStyleSheet('''
            background-color: #323232;
            border: 0px;''')

        # Connections
        self.clicked.connect(self.button_clicked)

        # Attributes
        self.controller = controller
    
    def button_clicked(self):
        self.controller.show_about_us_window()

    def enterEvent(self, event):
        self.controller.set_footer_description('Display the About Us window')
        self.setStyleSheet('''
        background-color: #555555;
        border: 0px''')

    def leaveEvent(self, event):
        self.controller.set_footer_description('')
        self.setStyleSheet('''
        background-color: #323232;
        border: 0px''')

    def mousePressEvent(self, event):
        super(AboutUsButton, self).mousePressEvent(event)
        event.accept()
