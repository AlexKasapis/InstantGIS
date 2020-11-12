from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QGridLayout, QLineEdit, QLabel


class ExportMenu(QDialog):

    accepted = QtCore.pyqtSignal(dict)

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
            QLineEdit {
                height: 24px;
                color: #808080;
                background: #202020;
                font-size: 14px;
                font-weight: bold;
                selection-background-color: #AAAAAA;
                border: 1px solid black;
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
            QPushButton:disabled {
                color: #343434;
                border: 2px solid #343434;
            }
            QCheckBox {
                color: #808080;
                font-size: 14px;
                font-weight: bold;
            }
            QCheckBox:disabled {
                color: #484848;
                background: #343434;
            }
            ''')

        self.id_label = QLabel('Path ID: ')
        self.id_input = QLineEdit()
        self.id_input.textEdited[str].connect(self.set_button_status)

        self.export_csv_button = QPushButton('Export to csv...')
        self.export_shapefile_button = QPushButton('Export to shapefile...')
        self.reset_path_checkbox = QCheckBox('Reset path after export')
        self.reset_path_checkbox.setChecked(True)
        self.cancel_button = QPushButton('Cancel')
        
        self.export_shapefile_button.clicked.connect(self.export_shapefile_pressed)
        self.export_csv_button.clicked.connect(self.export_csv_pressed)
        self.cancel_button.clicked.connect(self.cancel_pressed)

        self.set_button_status()

        layout = QGridLayout(self)
        layout.setSpacing(3)
        layout.setContentsMargins(5,5,5,5)
        self.setLayout(layout)
        layout.addWidget(self.id_label, 0, 0)
        layout.addWidget(self.id_input, 0, 1)
        layout.addWidget(self.export_shapefile_button, 1, 0, 1, 2)
        layout.addWidget(self.export_csv_button, 2, 0, 1, 2)
        layout.addWidget(self.reset_path_checkbox, 3, 0, 1, 2)
        layout.addWidget(self.cancel_button, 4, 0, 1, 2)
        
        self.move(x, y)

    def set_button_status(self):
        is_enabled = False
        try:
            int(self.id_input.text())
            is_enabled = True
        except ValueError:
            pass
        self.export_csv_button.setEnabled(is_enabled)
        self.export_shapefile_button.setEnabled(is_enabled)
        self.reset_path_checkbox.setEnabled(is_enabled)

    def export_shapefile_pressed(self):
        values = {'export_type': 'shapefile', 'path_id': self.id_input.text(), 'reset_path': self.reset_path_checkbox.isChecked()}
        self.accepted.emit(values)
        self.accept()

    def export_csv_pressed(self):
        values = {'export_type': 'csv', 'path_id': self.id_input.text(), 'reset_path': self.reset_path_checkbox.isChecked()}
        self.accepted.emit(values)
        self.accept()

    def cancel_pressed(self):
        self.close()
