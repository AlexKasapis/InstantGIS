import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import geopandas as gp

from Components.AnchorView import AnchorView

class MapCanvas(FigureCanvas):

    def __init__(self, parent, model, dpi):
        
        self.model = model

        self.fig = Figure(dpi=dpi)
        self.fig.patch.set_alpha(0)
        super(MapCanvas, self).__init__(self.fig)

        self.axes = self.fig.add_subplot(111)
        self.axes.patch.set_alpha(0)

        #self.fig.tight_layout()
        self.axes.set_position([0, 0, 1, 1]) # left,bottom,width,height
        self.axes.grid(color='black', alpha=0.2)
        self.axes.tick_params(axis='both', which='both', length=0)
        self.axes.tick_params(axis="y", labelcolor='#428071', direction="in", pad=-22)
        self.axes.tick_params(axis="x", labelcolor='#428071', direction="in", pad=-10)

        world = gp.read_file('./maps/coastline.geojson')

        world.plot(ax=self.axes, color='black', linewidth=1)
        self.anchor_view1 = AnchorView(self.model.anchor1, parent=self)
        self.anchor_view2 = AnchorView(self.model.anchor2, parent=self)


    def resizeEvent(self, event):
        # Resize figure
        # self.fig.set_figwidth(event.size().width() / 80)
        #self.fig.set_figheight(event.size().height() / 80)
        self.axes.set_aspect('auto')
        # Move the anchors to the new positions
        super(MapCanvas, self).resizeEvent(event)
        min_pnt = self.axes.get_position().min  # Bottom left corner
        max_pnt = self.axes.get_position().max  # Top right corner
        # min_dsp, max_dsp = self.fig.transFigure.transform_point((min_pnt, max_pnt))
        # self.model.anchor1.update(pos=QtCore.QPoint(min_dsp[0], min_dsp[1]))
        # self.model.anchor2.update(pos=QtCore.QPoint(max_dsp[0], max_dsp[1]))
    
    def reset(self):
        self.anchor_view1.reset()
        self.anchor_view2.reset()

class MapView(QtWidgets.QWidget):

    def __init__(self, parent=None, model=None, dpi=100, *args, **kwargs):
        super(MapView, self).__init__(parent=parent, *args, **kwargs)
        self.dpi = dpi
        self.map_canvas = MapCanvas(self, model=model, dpi=dpi)
        self.toolbar = NavigationToolbar(self.map_canvas, self)
        self.toolbar.hide()
        self.toolbar.pan()

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
        self.map_canvas.fig.set_size_inches(width_in, height_in, forward=True)
    

    def reset(self):
        self.map_canvas.reset()
        