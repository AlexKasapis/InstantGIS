import sys
from PyQt5.QtGui import QColor, QGuiApplication
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from Settings import CanvasUtilities
from Components.MapCanvas import MapCanvas


class GISFrame(QWidget):

    def __init__(self, controller, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        
        self.controller = controller
        self.controller.gis_frame = self

        self.setAutoFillBackground(True)
        color = QColor("gray")
        color.setAlpha(50)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)
        
        self.dpi = QGuiApplication.primaryScreen().physicalDotsPerInch()
        self.map_canvas = QWidget()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.map_canvas)
        self.setLayout(layout)

        # Load the map on 1 - Medium resolution [0 1 2]
        self.controller.reset_map(1)

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
