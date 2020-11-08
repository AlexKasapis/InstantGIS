from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QLabel


class AnchorMenu(QDialog):

    accepted = QtCore.pyqtSignal(dict)

    def __init__(self, lon, lat, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setWindowTitle("Set coordinates")

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
                height: 20px;
                width: 60px;
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
            ''')

        self.lon_label = QLabel('Longitude')
        
        self.longitude_input = QLineEdit()
        self.longitude_input.setText(str(lon))
        self.longitude_input.textEdited[str].connect(self.unlock)

        self.lat_label = QLabel('Latitude')

        self.latitude_input = QLineEdit()
        self.latitude_input.setText(str(lat))
        self.latitude_input.textEdited[str].connect(self.unlock)

        self.ok_button = QPushButton('OK')
        self.ok_button.setEnabled(self.are_inputs_valid())
        self.ok_button.clicked.connect(self.ok_pressed)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel_pressed)

        layout = QGridLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.lon_label, 0, 0)
        layout.addWidget(self.longitude_input, 0, 1)
        layout.addWidget(self.lat_label, 1, 0)
        layout.addWidget(self.latitude_input, 1, 1)
        layout.addWidget(self.ok_button, 2, 0)
        layout.addWidget(self.cancel_button, 2, 1)
        
        self.move(x, y)

    def unlock(self, text):
        if self.are_inputs_valid():
            self.ok_button.setEnabled(True)
        else:
            self.ok_button.setDisabled(True)

    def ok_pressed(self):
        values = {'Longitude': int(self.longitude_input.text()), 'Latitude': int(self.latitude_input.text())}
        self.accepted.emit(values)
        self.accept()

    def cancel_pressed(self):
        self.close()

    def are_inputs_valid(self):
        try: 
            lon = int(self.longitude_input.text())
            lat = int(self.latitude_input.text())
            return -180 <= lon <= 180 and -90 <= lat <= 90
        except ValueError:
            return False