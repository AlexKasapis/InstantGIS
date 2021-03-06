from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class ResetButton(QPushButton):

    def __init__(self, parent, controller, *args, **kwargs):
        super(ResetButton, self).__init__(*args, **kwargs)

        # Visuals
        self.setFixedSize(QSize(37, 37))
        self.setText('')
        self.setIcon(QIcon("./Resources/Icons/icon_reset_plot.png"))
        self.setIconSize(QSize(30, 30))
        self.setStyleSheet('''
            background-color: #323232;
            border: 0px;
            border-radius: 7px;''')

        # Connections
        self.clicked.connect(self.button_clicked)

        # Attributes
        self.controller = controller
    
    def button_clicked(self):
        if self.controller.free_map_mode:
            self.controller.reset_plot()
        else:
            self.controller.reset_path()

    def enterEvent(self, event):
        self.controller.set_footer_description('Reset {}'.format('plot view' if self.controller.free_map_mode else 'path'))
        self.setStyleSheet('''
        background-color: #555555;
        border: 0px;
        border-radius: 7px;''')

    def leaveEvent(self, event):
        self.controller.set_footer_description('')
        self.setStyleSheet('''
        background-color: #323232;
        border: 0px;
        border-radius: 7px;''')

    def mousePressEvent(self, event):
        super(ResetButton, self).mousePressEvent(event)
        event.accept()