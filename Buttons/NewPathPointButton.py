import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets


class NewPathPointButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(NewPathPointButton, self).__init__(*args, **kwargs)

        self.setText("")
        self.setIcon(QtGui.QIcon("icons/icons8-anchor-nodes-48.png"))
        self.setIconSize(QtCore.QSize(35, 35))
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        print("Clicked on New Path Button!")
