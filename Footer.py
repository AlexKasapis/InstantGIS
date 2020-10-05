import win32gui
from PyQt5 import QtCore, QtWidgets
from Components.Buttons.ResizeButton import ResizeButton


class Footer(QtWidgets.QFrame):

    def __init__(self, main_ctrl, model, *args, **kwargs):
        
        self.main_ctrl = main_ctrl
        self.model = model
        QtWidgets.QFrame.__init__(self, *args, **kwargs)

        self.setFixedHeight(25)
        self.setStyleSheet("background-color:#cbaf87;")

        # Layout
        footer_layout = QtWidgets.QHBoxLayout()
        footer_layout.setSpacing(5)
        footer_layout.setContentsMargins(5, 3, 3, 2)
        self.setLayout(footer_layout)

        self.description_label = QtWidgets.QLabel(self)
        footer_layout.addWidget(self.description_label, 1, QtCore.Qt.AlignLeft)
        
        self.model.subscribe_update_func(self.update_description_label)


        resize_button = ResizeButton(self)
        footer_layout.addWidget(resize_button, 0, QtCore.Qt.AlignRight)

    def update_description_label(self):
        self.description_label.setText(self.model.footer_description_label)