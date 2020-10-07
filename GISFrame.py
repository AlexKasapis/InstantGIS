from PyQt5 import QtCore, QtGui, QtWidgets

from Components.AnchorView import AnchorView

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

        self.anchor_view1 = AnchorView(self.main_ctrl, self.model.anchor1, parent=self)
        self.anchor_view2 = AnchorView(self.main_ctrl, self.model.anchor2, parent=self)

        self.model.subscribe_update_func(self.reset_frame)

        self.reset_frame()
        self.resetMap(True)

    def mousePressEvent(self, event):
        self.main_ctrl.close_anchor_form()
        

    def resetMap(self, reset_path):
        self.anchor1 = ((0, 0), (-180, 90))
        self.anchor2 = ((0, self.height()), (-180, -90))
        if reset_path:
            self.current_path = []

    def redraw(self):
        pass

    def reset_frame(self):
        self.anchor_view1.reset()
        self.anchor_view2.reset()
        
        self.redraw()

        

        
        