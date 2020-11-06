import win32gui
import enum
from PyQt5 import QtWidgets, QtCore, QtGui
from Settings import ResizeUtilities


class Footer(QtWidgets.QFrame):

    def __init__(self, controller, *args, **kwargs):
        
        QtWidgets.QFrame.__init__(self, *args, **kwargs)

        self.controller = controller
        self.controller.footer = self
        
        self.setFixedHeight(20)
        self.setStyleSheet('''background-color: #323232;''')

        # Layout
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(3, 0, 2, 0)
        self.setLayout(layout)

        self.description_label = QtWidgets.QLabel('')
        self.description_label.setStyleSheet('''
            color: #808080;
            font-weight: 500;''')
        
        self.mode_label = QtWidgets.QLabel('')
        self.mode_label.setStyleSheet('''
            color: #808080;
            font-weight: 500;''')

        layout.addWidget(self.description_label, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(self.mode_label, 0, QtCore.Qt.AlignRight)

        self.update_mode_label()

    def update_mode_label(self):
        self.mode_label.setText('(Free map mode)' if self.controller.free_map_mode else '(Path creation mode)')
