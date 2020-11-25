from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QVBoxLayout, QLineEdit, QLabel, QSizePolicy, QScrollArea, QWidget


class HelpWindow(QDialog):

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
            QScrollArea {
                border: 0px;
            }
            QScrollBar:vertical {   
                width: 10px;
                background: #808080;
                border-radius: 5px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #323232;
                border: 1px solid black;
                border-radius: 5px;
                min-height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QWidget {
                background: #323232;
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

        # Title
        self.title_label = QLabel('How To Use InstantGIS')
        self.title_label.setAlignment(Qt.AlignHCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold; margin-bottom: 40px;')
        
        # Description
        self.intro1_label = QLabel('The process in which to export paths from images is fairly simple and can be split into three parts:')
        self.intro1_label.setAlignment(Qt.AlignLeft)
        self.intro1_label.setWordWrap(True)
        self.intro2_label = QLabel('1. Centering the map')
        self.intro2_label.setAlignment(Qt.AlignLeft)
        self.intro2_label.setStyleSheet('margin-left: 40px;')
        self.intro3_label = QLabel('2. Creating the path')
        self.intro3_label.setAlignment(Qt.AlignLeft)
        self.intro3_label.setStyleSheet('margin-left: 40px;')
        self.intro4_label = QLabel('3. Exporting the path')
        self.intro4_label.setAlignment(Qt.AlignLeft)
        self.intro4_label.setStyleSheet('margin-left: 40px; margin-bottom: 40px;')
        
        # Step 1
        self.step1_label = QLabel('Step 1: Centering the map')
        self.step1_label.setAlignment(Qt.AlignLeft)
        self.step1_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        self.step1_1_label = QLabel('Centering the map is the first step in order to extract world coordinates from images.')
        self.step1_1_label.setAlignment(Qt.AlignLeft)
        self.step1_1_label.setWordWrap(True)
        self.step1_2_label = QLabel('The goal is to scale the map to the point where the coastlines from the application overlap those in your image.')
        self.step1_2_label.setAlignment(Qt.AlignLeft)
        self.step1_2_label.setWordWrap(True)
        self.step1_2_label.setStyleSheet('margin-bottom: 40px;')
        
        self.step1_3_label = QLabel('There are two independent systems used for this purpose:')
        self.step1_3_label.setAlignment(Qt.AlignLeft)
        self.step1_3_label.setWordWrap(True)
        self.step1_3_label.setStyleSheet('margin-bottom: 40px;')
        
        # Anchors
        self.anchors_1_label = QLabel('The anchors\' system')
        self.anchors_1_label.setAlignment(Qt.AlignLeft)
        self.anchors_1_label.setWordWrap(True)
        self.anchors_1_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.anchors_2_label = QLabel("In this system you can place two anchors on the map and set their world coordinates in respect to the data from your image. The application will calculate the rest and will automatically scale the map in order to match your image.")
        self.anchors_2_label.setAlignment(Qt.AlignLeft)
        self.anchors_2_label.setWordWrap(True)
        self.anchors_2_label.setStyleSheet('margin-bottom: 40px;')

        # [TODO] INSERT GIF: anchor_centering

        # Mouse centering
        self.manual_centering1_label = QLabel('Using the mouse')
        self.manual_centering1_label.setAlignment(Qt.AlignLeft)
        self.manual_centering1_label.setWordWrap(True)
        self.manual_centering1_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.manual_centering2_label = QLabel("You can use the mouse to scale the map according to your preferences. The mouse wheel zooms the map in or out. The left mouse button is used to drag the map. The right mouse button is used to scale the map on the X and Y axis SEPARATELY. Use this for ultimate precision.")
        self.manual_centering2_label.setAlignment(Qt.AlignLeft)
        self.manual_centering2_label.setWordWrap(True)
        self.manual_centering2_label.setStyleSheet(' margin-bottom: 40px;')

        # [TODO] INSERT GIF: map_centering

        # Path creation
        
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_button_clicked)


        # Container Widget       
        self.widget = QWidget()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 10, 10)
        self.widget.setLayout(layout)
        layout.addWidget(self.title_label)
        layout.addWidget(self.intro1_label)
        layout.addWidget(self.intro2_label)
        layout.addWidget(self.intro3_label)
        layout.addWidget(self.intro4_label)
        layout.addWidget(self.step1_label)
        layout.addWidget(self.step1_1_label)
        layout.addWidget(self.step1_2_label)
        layout.addWidget(self.step1_3_label)
        layout.addWidget(self.anchors_1_label)
        layout.addWidget(self.anchors_2_label)
        layout.addWidget(self.manual_centering1_label)
        layout.addWidget(self.manual_centering2_label)
        layout.addWidget(self.close_button)

        # Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)

        # Scroll Area Layer add
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(3, 3, 3, 3)
        vLayout.setSpacing(0)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)

    def close_button_clicked(self):
        self.close()
