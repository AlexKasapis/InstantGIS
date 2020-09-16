import win32gui
from PyQt5 import QtCore, QtWidgets
from Buttons.ResizeButton import ResizeButton


class Footer(QtWidgets.QFrame):

    def __init__(self, *args, **kwargs):
        QtWidgets.QFrame.__init__(self, *args, **kwargs)

        self.setFixedHeight(25)
        self.setStyleSheet("background-color:#cbaf87;")

        # Layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(5, 3, 3, 2)
        self.setLayout(header_layout)

        self.description_label = QtWidgets.QLabel(self)
        self.description_label.setText("Sample Text")
        header_layout.addWidget(self.description_label, 1, QtCore.Qt.AlignLeft)

        resize_button = ResizeButton(self)
        header_layout.addWidget(resize_button, 0, QtCore.Qt.AlignRight)
