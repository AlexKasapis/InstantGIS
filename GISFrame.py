from PyQt5 import QtCore, QtGui, QtWidgets

from Components.CoordinateInput import CoordinateInput

class GISFrame(QtWidgets.QWidget):

    def __init__(self, main_ctrl, model, *args, **kwargs):
        
        self.main_ctrl = main_ctrl
        self.model = model
        QtWidgets.QWidget.__init__(self, *args, **kwargs)

        self.anchor1 = None
        self.anchor2 = None
        self.current_path = []

        self.setAutoFillBackground(True)
        p = self.palette()
        color = QtGui.QColor("gray")
        color.setAlpha(50)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)


        # Create the input form for latitude and longitude and display it
        self.coord_input = CoordinateInput(self.main_ctrl, parent=self)

        self.model.subscribe_update_func(self.reset_frame)

        self.reset_frame()
        self.resetMap(True)

    def mousePressEvent(self, event):
        if self.main_ctrl.adding_anchors_flag:
            
            self.coord_input.display(event.localPos())
        

    def resetMap(self, reset_path):
        self.anchor1 = ((0, 0), (-180, 90))
        self.anchor2 = ((0, self.height()), (-180, -90))
        if reset_path:
            self.current_path = []

    def redraw(self):
        pass

    def reset_frame(self):
        if hasattr(self, 'coord_input'):
            self.coord_input.reset()

        self.redraw()

        

        
        