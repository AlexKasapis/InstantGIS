import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets


class HelpButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(HelpButton, self).__init__(*args, **kwargs)

        self.setText("")
        self.setIcon(QtGui.QIcon("icons/icons8-question-mark-48.png"))
        self.setIconSize(QtCore.QSize(35, 35))
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        print("Clicked on the Help Button!")
