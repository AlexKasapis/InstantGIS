import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from Components.MapCanvas import MapCanvas
from Settings import CanvasUtilities


class GISFrame(QtWidgets.QWidget):

    def __init__(self, controller, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        
        self.controller = controller

        self.setAutoFillBackground(True)
        color = QtGui.QColor("gray")
        color.setAlpha(50)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)
        
        self.dpi = QtGui.QGuiApplication.primaryScreen().physicalDotsPerInch()
        self.map_canvas = MapCanvas(controller=self.controller, parent=self, dpi=self.dpi)
        self.toolbar = NavigationToolbar2QT(parent=self, canvas=self.map_canvas)
        self.toolbar.hide()
        #self.toolbar.pan()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.map_canvas)
        self.setLayout(layout)

    def fit_to_frame(self, new_width, new_height):
        # Set the size of the widget
        self.resize(new_width, new_height)

        # Set the size of the plot
        width_in, height_in = new_width / self.dpi, new_height / self.dpi
        self.map_canvas.figure.set_size_inches(width_in, height_in, forward=True)
    
    def reset(self):
        self.map_canvas.reset()

    def mousePressEvent(self, event):
        self.controller.close_anchor_forms()

    def resizeEvent(self, event):
        # Set the size of the plot
        width_in, height_in = event.size().width() / self.dpi, event.size().height() / self.dpi
        self.map_canvas.figure.set_size_inches(width_in, height_in, forward=True)
