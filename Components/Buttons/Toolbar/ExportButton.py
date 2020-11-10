import win32gui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class ExportButton(QPushButton):
    def __init__(self, parent, controller, *args, **kwargs):
        super(ExportButton, self).__init__(*args, **kwargs)

        # Visuals
        self.setFixedSize(QSize(37, 37))
        self.setText("")
        self.setIcon(QIcon("./Resources/Icons/icon_export.png"))
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
        _, _, (x, y) = win32gui.GetCursorInfo()
        self.controller.show_export_menu(x, y)

    def enterEvent(self, event):
        self.controller.set_footer_description('Export to...')
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
        super(ExportButton, self).mousePressEvent(event)
        event.accept()
