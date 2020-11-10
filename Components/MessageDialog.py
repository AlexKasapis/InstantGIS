from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel


class MessageDialog(QDialog):

    accepted = QtCore.pyqtSignal(dict)

    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet('''
            QDialog {
                background: #323232;
                border: 2px solid black;
                border-radius: 4px;
            }
            QPushButton {
                height: 25px;
                width: 70px;
                color: #808080;
                background: #202020;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #808080;
                border-radius: 3px;
            }
            QPushButton:hover {
                background: #343434;
            }
            QPushButton:pressed {
                background: #484848;
            }
            QLabel {
                color: #808080;
                font-size: 14px;
                font-weight: bold;
            }
            ''')

        self.message_label = QLabel(message)
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.ok_button_pressed)

        layout = QVBoxLayout(self)
        layout.setSpacing(3)
        layout.setContentsMargins(5,5,5,5)
        self.setLayout(layout)
        layout.addWidget(self.message_label)
        layout.addWidget(self.ok_button)

    def ok_button_pressed(self):
        self.close()
