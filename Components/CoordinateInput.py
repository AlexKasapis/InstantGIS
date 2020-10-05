from PyQt5 import QtCore, QtGui, QtWidgets

""" Displays an input form for the latitude and longitude of the clicked point """
class CoordinateInput(QtWidgets.QFrame):

    anchorAdded = QtCore.pyqtSignal(QtCore.QPointF)
    latitude_is_done = False
    longitude_is_done = False

    def __init__(self, main_ctrl, *args, **kwargs):
        QtWidgets.QFrame.__init__(self, *args, **kwargs)

        self.main_ctrl = main_ctrl

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        layout = QtWidgets.QGridLayout()
        
        # Add latitude and longitude labels to the layout
        lat_label = QtWidgets.QLabel(" Latitude ")
        lat_label.setStyleSheet("QLabel { background-color : #cbaf87; } ")
        layout.addWidget(lat_label, 0, 0, QtCore.Qt.AlignCenter)
        
        long_label = QtWidgets.QLabel(" Longitude ")
        long_label.setStyleSheet("QLabel { background-color : #cbaf87; } ")
        layout.addWidget(long_label, 0, 1, QtCore.Qt.AlignCenter)
        
        # Add the latitude and longitude input text fields to the layout
        # Each text field has the appropriate range validator for the coordinates.
        self.lat_input = QtWidgets.QLineEdit(dragEnabled=True)
        self.lat_input.setValidator(QtGui.QDoubleValidator(bottom=float(-90), top=float(90), decimals=7, notation=0))
        self.lat_input.editingFinished.connect(self.latitudeEditingFinished)
        layout.addWidget(self.lat_input, 1, 0)

        self.long_input = QtWidgets.QLineEdit(dragEnabled=True)
        self.long_input.setValidator(QtGui.QDoubleValidator(bottom=float(-180), top=float(180), decimals=7, notation=0))
        self.long_input.editingFinished.connect(self.longitudeEditingFinished)
        layout.addWidget(self.long_input, 1, 1)

        self.setLayout(layout)

    @QtCore.pyqtSlot()
    def latitudeEditingFinished(self):
        self.latitude_is_done = True
        if self.longitude_is_done:
            self.anchorEditingFinished()

    @QtCore.pyqtSlot()
    def longitudeEditingFinished(self):
        self.longitude_is_done = True
        if self.latitude_is_done:
            self.anchorEditingFinished()

    def anchorEditingFinished(self):
        coord_point = QtCore.QPointF(float(self.lat_input.text()), float(self.long_input.text()))
        print(coord_point)
        self.anchorAdded.emit(coord_point)


    def display(self, point):
        """ Displays the input dialog and moves it to the cursor position
            ensuring that it remains within the frame """
        x_offset = point.toPoint().x() - self.width() / 2 
        y_offset = point.toPoint().y()

        if (x_offset < 0):
            x_offset = 0
        elif (x_offset + self.width() > self.parent().width()):
            x_offset = self.parent().width() - self.width()
        
        if (y_offset + self.height() > self.parent().height()):
            y_offset -= self.height()

        self.move(x_offset, y_offset)
        self.show()

    def reset(self):
        self.latitude_is_done = False
        self.lat_input.setText("")
        self.longitude_is_done = False
        self.long_input.setText("")

        self.hide()
        