from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QGridLayout, QLineEdit, QLabel, QSizePolicy


class AboutUsWindow(QDialog):

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.controller = controller

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet('''
            QDialog {
                background: #323232;
                border: 2px solid black;
                border-radius: 4px;
            }
            QLabel {
                color: #808080;
                font-size: 14px;
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
            ''')

        self.title_label = QLabel('InstantGIS - version {}'.format(self.controller.version))
        self.title_label.setAlignment(Qt.AlignHCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.creators_label = QLabel('InstantGIS was created by Alex Kasapis with the help of Filippos Zacharopoulos.')
        self.creators_label.setAlignment(Qt.AlignHCenter)
        self.creators_label.setWordWrap(True)
        
        self.goal_label = QLabel('InstantGIS is a free tool that tries to cut down the time required to transfer world coordinate points stored in analog media (publications, books, etc) into digital files.')
        self.goal_label.setAlignment(Qt.AlignHCenter)
        self.goal_label.setWordWrap(True)
        
        self.icons8_label = QLabel('This application was created using image assets from icons8.com.')
        self.icons8_label.setAlignment(Qt.AlignHCenter)
        self.icons8_label.setWordWrap(True)
        
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_button_clicked)

        layout = QGridLayout(self)
        layout.setSpacing(40)
        layout.setContentsMargins(15, 10, 10, 10)
        layout.setRowStretch(3, 1)
        self.setLayout(layout)
        layout.addWidget(self.title_label, 0, 0)
        layout.addWidget(self.creators_label, 1, 0)
        layout.addWidget(self.goal_label, 2, 0)
        layout.addWidget(self.icons8_label, 3, 0)
        layout.addWidget(self.close_button, 4, 0)

    def close_button_clicked(self):
        self.close()
