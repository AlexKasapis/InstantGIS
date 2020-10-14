from PyQt5 import QtCore, QtGui, QtWidgets

from Components.AnchorView import AnchorView
from Components.MapView import MapView

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
        
        self.dpi = QtGui.QGuiApplication.primaryScreen().physicalDotsPerInch()
        self.map_view = MapView(parent=self, model=model, width=self.width(), height=self.height(), dpi=self.dpi)

        self.model.subscribe_update_func(self.reset_frame)

        self.reset_frame()

    def mousePressEvent(self, event):
        self.main_ctrl.close_anchor_form()

    def resizeEvent(self, event):
        self.map_view.fit_to_frame(event.size().width(), event.size().height())

    def resetMap(self, reset_path):
        if reset_path:
            self.current_path = []

    def redraw(self):
        pass

    def reset_frame(self):
        self.map_view.reset()
        self.resetMap(True)

        self.redraw()

        

        
        