from PyQt5 import QtCore, QtGui, QtWidgets

class AnchorView(QtWidgets.QPushButton):

    def __init__(self, main_ctrl, anchor_model, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)

        self.anchor_model = anchor_model
        
        self.setGeometry(anchor_model.x, anchor_model.y, 12, 12) 
        self.setStyleSheet("""  
                            background-color: gold;
                            border-radius: 6; 
                            border: 1px solid black
                            """)

        self.clicked.connect(self.anchor_clicked_handle)
 

    def anchor_clicked_handle(self):
        if not hasattr(self, "anchor_form"):
            self.anchor_form = AnchorFormView(self.anchor_model, parent=self.parent())
            
        self.anchor_model.form_is_visible = not self.anchor_model.form_is_visible

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        
        super(AnchorView, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            curr_pos = self.mapToGlobal(self.pos())
            global_pos = event.globalPos()
            diff = global_pos - self.__mouseMovePos
            new_pos = self.mapFromGlobal(curr_pos + diff)

            frame_geom = self.parent().geometry()

            if frame_geom.contains(new_pos + QtCore.QPoint(12, 12)) and frame_geom.contains(new_pos):
                self.move(new_pos)
                self.anchor_model.update(pos=new_pos)
                self.__mouseMovePos = global_pos

        super(AnchorView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return
    
        super(AnchorView, self).mouseReleaseEvent(event)

    def reset(self):
        self.move(self.anchor_model.x, self.anchor_model.y)

        if hasattr(self, "anchor_form"):
            self.anchor_form.reset()
        


""" Displays an input form for the latitude and longitude of the clicked point """
class AnchorFormView(QtWidgets.QFrame):

    def __init__(self, anchor_model, *args, **kwargs):
        QtWidgets.QFrame.__init__(self, *args, **kwargs)

        self.anchor_model = anchor_model

        self.setStyleSheet("background-color: lightblue;")

        layout = QtWidgets.QGridLayout()
        
        # Latitude label
        lat_label = QtWidgets.QLabel("Lat:")
        layout.addWidget(lat_label, 0, 0, QtCore.Qt.AlignCenter)
        # Latitude input text field
        self.lat_input = QtWidgets.QLineEdit(dragEnabled=True)
        self.lat_input.setText(str(self.anchor_model.lat))
        self.lat_input.setFixedWidth(30)
        self.lat_validator = QtGui.QDoubleValidator(bottom=float(-90), top=float(90), decimals=7, notation=0)
        self.lat_input.setValidator(self.lat_validator)
        layout.addWidget(self.lat_input, 0, 1)

        # Longitude label
        long_label = QtWidgets.QLabel("Long:")
        layout.addWidget(long_label, 0, 2, QtCore.Qt.AlignCenter)
        # Longitude input text field
        self.long_input = QtWidgets.QLineEdit(dragEnabled=True)
        self.long_input.setText(str(self.anchor_model.long))     
        self.long_input.setFixedWidth(30)   
        self.long_validator = QtGui.QDoubleValidator(bottom=float(-180), top=float(180), decimals=7, notation=0)
        self.long_input.setValidator(self.long_validator)
        layout.addWidget(self.long_input, 0, 3)

        # X label
        x_label = QtWidgets.QLabel("X:")
        layout.addWidget(x_label, 1, 0, QtCore.Qt.AlignCenter)
        # X input text field
        self.x_input = QtWidgets.QLineEdit()
        self.x_input.setText(str(self.anchor_model.x))
        self.x_input.setFixedWidth(30)
        self.x_validator = QtGui.QIntValidator(bottom=int(0), top=int(self.parent().width()))
        self.x_input.setValidator(self.x_validator)
        layout.addWidget(self.x_input, 1, 1)

        # Y label
        y_label = QtWidgets.QLabel("Y:")
        layout.addWidget(y_label, 1, 2, QtCore.Qt.AlignCenter)

        self.y_input = QtWidgets.QLineEdit()
        self.y_input.setText(str(self.anchor_model.y))
        self.y_input.setFixedWidth(30)
        self.y_validator = QtGui.QIntValidator(bottom=int(0), top=int(self.parent().height()))
        self.y_input.setValidator(self.y_validator)
        layout.addWidget(self.y_input, 1, 3)

        self.setLayout(layout)
        
        self.show()
        self.reset()


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            coords, pos = self.get_form_values()
            self.anchor_model.update(coords=coords, pos=pos)
        else:
            event.ignore()

    def mousePressEvent(self, event):
        pass

    def move_to_point(self):
        """ Moves the anchor form to the xy point of the anchor """

        x_offset = self.anchor_model.x - self.width() / 2 
        y_offset = self.anchor_model.y + 15

        if (x_offset < 0):
            x_offset = 0
        elif (x_offset + self.width() > self.parent().width()):
            x_offset = self.parent().width() - self.width()
        
        if (y_offset + self.height() > self.parent().height()):
            y_offset -= self.height() + 20

        self.move(x_offset, y_offset)


    def get_form_values(self):
        state_lat, lat_value, _ = self.lat_validator.validate(self.lat_input.text(), 0)
        state_long, long_value, _ = self.long_validator.validate(self.long_input.text(), 0)

        if state_lat != QtGui.QValidator.Acceptable:
            lat_value = self.anchor_model.lat
        if state_long != QtGui.QValidator.Acceptable:
            long_value = self.anchor_model.long

        coords = QtCore.QPointF(float(lat_value), float(long_value))
        
        state_x, x_value, _ = self.x_validator.validate(self.x_input.text(), 0)
        state_y, y_value, _ = self.y_validator.validate(self.y_input.text(), 0)

        if state_x != QtGui.QValidator.Acceptable:
            x_value = self.anchor_model.x
        if state_y != QtGui.QValidator.Acceptable:
            y_value = self.anchor_model.y

        pos = QtCore.QPoint(int(x_value), int(y_value))

        return coords, pos


    def reset(self):
        """ Reset the input text and the flags and hide the input form """
        
        self.x_input.setText(str(self.anchor_model.x))
        self.y_input.setText(str(self.anchor_model.y))

        self.lat_input.setText(str(self.anchor_model.lat))
        self.long_input.setText(str(self.anchor_model.long))

        if self.anchor_model.form_is_visible:
            self.move_to_point()
            self.show()
        else:
            self.hide()