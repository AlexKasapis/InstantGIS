import win32gui, win32con
from PyQt5 import QtCore, QtGui, QtWidgets


class MinimizeButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(MinimizeButton, self).__init__(*args, **kwargs)

        self.setText("")
        self.setIcon(QtGui.QIcon("icons/icons8-minimize-window-48.png"))
        self.setIconSize(QtCore.QSize(35, 35))
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MINIMIZE)

