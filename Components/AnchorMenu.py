from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout


class AnchorMenu(QDialog):

    accepted = QtCore.pyqtSignal(dict)

    def __init__(self, lon, lat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle("Set coordinates")

        self.longitude_input = QLineEdit()
        self.longitude_input.setText(str(lon))
        self.longitude_input.textEdited[str].connect(self.unlock)

        self.latitude_input = QLineEdit()
        self.latitude_input.setText(str(lat))
        self.latitude_input.textEdited[str].connect(self.unlock)

        self.ok_button = QPushButton('OK')
        self.ok_button.setEnabled(self.are_inputs_valid())
        self.ok_button.clicked.connect(self.ok_pressed)

        form = QFormLayout(self)
        form.addRow('Longitude', self.longitude_input)
        form.addRow('Latitude', self.latitude_input)
        form.addRow(self.ok_button)

    def unlock(self, text):
        if self.are_inputs_valid():
            self.ok_button.setEnabled(True)
        else:
            self.ok_button.setDisabled(True)

    def ok_pressed(self):
        values = {'Longitude': int(self.longitude_input.text()), 'Latitude': int(self.latitude_input.text())}
        self.accepted.emit(values)
        self.accept()

    def are_inputs_valid(self):
        try: 
            lon = int(self.longitude_input.text())
            lat = int(self.latitude_input.text())
            return -180 <= lon <= 180 and -90 <= lat <= 90
        except ValueError:
            return False