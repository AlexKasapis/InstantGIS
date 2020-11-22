from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QGridLayout, QComboBox, QLabel


class OptionsMenu(QDialog):

    def __init__(self, x, y, controller, *args, **kwargs):
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
                font-weight: bold;
            }
            QComboBox {
                height: 24px;
                color: #808080;
                background: #202020;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid black;
            }
            QComboBox::down-arrow {
            }
            QComboBox QAbstractItemView {
                color: #808080;
                background: #202020;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid black;
                selection-background-color: #AAAAAA;
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

        self.map_detail_label = QLabel('Map detail')
        self.map_detail_dropdown = QComboBox()
        self.map_detail_dropdown.addItems(['Low (faster)', 'Medium (Recommended)', 'High (most detailed)'])
        self.map_detail_dropdown.setCurrentIndex(self.controller.map_file_index)
        self.map_detail_dropdown.currentIndexChanged.connect(self.map_detail_changed)

        self.path_color_label = QLabel('Path color')
        self.path_color_dropdown = QComboBox()
        self.path_color_dropdown.addItems(['Red/Blue', 'Green/Magenta'])
        self.path_color_dropdown.setCurrentIndex(self.controller.path_color_index)
        self.path_color_dropdown.currentIndexChanged.connect(self.path_color_changed)

        self.point_size_label = QLabel('Path point size')
        self.point_size_dropdown = QComboBox()
        self.point_size_dropdown.addItems(['Small', 'Medium', 'Large'])
        self.point_size_dropdown.setCurrentIndex(self.controller.point_size_index)
        self.point_size_dropdown.currentIndexChanged.connect(self.point_size_changed)

        self.ok_button = QPushButton('Ok')
        self.ok_button.clicked.connect(self.ok_pressed)

        layout = QGridLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(5,5,5,5)
        self.setLayout(layout)
        layout.addWidget(self.map_detail_label, 0, 0)
        layout.addWidget(self.map_detail_dropdown, 0, 1)
        layout.addWidget(self.path_color_label, 1, 0)
        layout.addWidget(self.path_color_dropdown, 1, 1)
        layout.addWidget(self.point_size_label, 2, 0)
        layout.addWidget(self.point_size_dropdown, 2, 1)
        layout.addWidget(self.ok_button, 3, 0, 1, 2)
        
        self.move(x, y)

    def map_detail_changed(self, event):
        self.controller.reset_map(map_detail=event, keep_coordinates=True)

    def path_color_changed(self, event):
        self.controller.change_path_color(color_index=event)

    def point_size_changed(self, event):
        self.controller.change_point_size(size_index=event)

    def ok_pressed(self):
        self.close()
