from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QVBoxLayout


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
            QCheckBox {
                color: #808080;
                font-size: 14px;
                font-weight: bold;
            }
            ''')

        self.create_new_csv_button = QPushButton('Create new csv file...')
        self.add_to_csv_button = QPushButton('Add to csv file...')
        self.create_new_excel_button = QPushButton('Create new excel file...')
        self.add_to_excel_button = QPushButton('Add to excel file...')
        self.reset_path_checkbox = QCheckBox('Reset path after export')
        self.reset_path_checkbox.setChecked(True)
        self.cancel_button = QPushButton('Cancel')
        
        self.create_new_csv_button.clicked.connect(self.new_csv_pressed)
        self.add_to_csv_button.clicked.connect(self.append_csv_pressed)
        self.create_new_excel_button.clicked.connect(self.new_excel_pressed)
        self.add_to_excel_button.clicked.connect(self.append_excel_pressed)
        self.cancel_button.clicked.connect(self.cancel_pressed)

        layout = QVBoxLayout(self)
        layout.setSpacing(3)
        layout.setContentsMargins(5,5,5,5)
        self.setLayout(layout)
        layout.addWidget(self.create_new_csv_button)
        layout.addWidget(self.add_to_csv_button)
        layout.addWidget(self.create_new_excel_button)
        layout.addWidget(self.add_to_excel_button)
        layout.addWidget(self.reset_path_checkbox)
        layout.addWidget(self.cancel_button)
        
        self.move(x, y)

    def new_csv_pressed(self):
        values = {'export_type': 'new_csv', 'reset_path': self.reset_path_checkbox.isChecked()}
        self.accepted.emit(values)
        self.accept()

    def append_csv_pressed(self):
        values = {'export_type': 'append_csv', 'reset_path': self.reset_path_checkbox.isChecked()}
        self.accepted.emit(values)
        self.accept()

    def new_excel_pressed(self):
        values = {'export_type': 'new_excel', 'reset_path': self.reset_path_checkbox.isChecked()}
        self.accepted.emit(values)
        self.accept()

    def append_excel_pressed(self):
        values = {'export_type': 'append_excel', 'reset_path': self.reset_path_checkbox.isChecked()}
        self.accepted.emit(values)
        self.accept()

    def cancel_pressed(self):
        self.close()
