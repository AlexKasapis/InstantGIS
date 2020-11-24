from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter
from matplotlib.figure import Figure
from matplotlib import lines
import geopandas
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from Components.Anchor import Anchor
from Components.AnchorMenu import AnchorMenu
from Settings import CanvasUtilities


class MapCanvas(FigureCanvasQTAgg):

    def __init__(self, controller, map_file, parent, dpi):

        matplotlib.rcParams["axes.axisbelow"] = False

        self.controller = controller
        self.controller.map_canvas = self
        self.dpi = dpi
        self.parent = parent

        # Setup figure.
        self.figure = Figure(dpi=dpi)
        self.figure.patch.set_alpha(0)
        super(MapCanvas, self).__init__(self.figure)

        self.setStyleSheet('''background-color: transparent;''')

        self.path = []

        self.anchor_diameter = 10

        self.pressed_mouse_button = None  # None, QtCore.Qt.LeftButton, QtCore.Qt.RightButton
        self.drag_separately = False  # If true, zooming is axis independent
        self.mouse_dragged = False

        # Setup plot axes.
        self.figure.tight_layout()
        self.axes = self.figure.add_subplot(111)
        self.axes.patch.set_alpha(0)
        self.axes.set_position([0, 0, 1, 1])

        self.axes.set_xlim([-180, 180])
        self.axes.set_ylim([-90, 90])

        # Plot axes visuals.
        self.axes.grid(color='black', alpha=0.2)
        self.axes.tick_params(axis='both', which='both', length=0, labeltop=True, labelright=True)
        self.axes.tick_params(axis="y", labelcolor='#C7371E', direction="in", pad=-22)
        self.axes.tick_params(axis="x", labelcolor='#C7371E', direction="in", pad=-10)
        self.axes.spines["left"].set_visible(False)
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)
        self.axes.spines["bottom"].set_visible(False)

        # Setup anchors.
        self.controller.anchors = [
            Anchor(CanvasUtilities.convert_world_to_window(self, -160, 70), (-160, 70), self.controller, parent=self), 
            Anchor(CanvasUtilities.convert_world_to_window(self, 160, -70), (160, -70), self.controller, parent=self)
            ]

        # Load data file.
        self.world = geopandas.read_file('./Resources/MapData/{}'.format(map_file))
        #self.drop_resolution(2, 5)
        # self.world = world.to_crs(epsg=3857)  # Web Mercator
        self.world.plot(ax=self.axes, color='black', linewidth=1)

        self.controller.reset_plot()

    def drop_resolution(self, keep_amount, keep_total):
        for i in range(len(self.world['geometry'])):
            line_coords = self.world['geometry'][i].coords
            new_coords = []
            for j in range(1, len(line_coords)):
                if not j % keep_total > keep_amount:
                    new_coords.append(line_coords[j])
            self.world['geometry'][i].coords = [line_coords[0]] + new_coords + [line_coords[-1]]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed_mouse_button = Qt.LeftButton
        elif event.button() == Qt.RightButton:
            self.pressed_mouse_button = Qt.RightButton
        self.cursor_position = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.pressed_mouse_button == Qt.LeftButton:
            self.pressed_mouse_button = None
            if not self.controller.free_map_mode and not self.mouse_dragged:
                self.controller.add_path_point(event.pos().x(), event.pos().y())
            self.mouse_dragged = False
        elif event.button() == Qt.RightButton and self.pressed_mouse_button == Qt.RightButton:
            self.pressed_mouse_button = None
            self.mouse_dragged = False

    def mouseMoveEvent(self, event):
        if self.pressed_mouse_button != None:
            self.mouse_dragged = True

            if self.controller.free_map_mode:
                dist = event.globalPos() - self.cursor_position

                if (self.pressed_mouse_button == Qt.LeftButton):
                    self.controller.plot_pan(dist)
                elif self.pressed_mouse_button == Qt.RightButton:
                    self.controller.plot_zoom((dist.x(), -dist.y()))

                self.cursor_position = event.globalPos()
            
        x = event.pos().x()
        y = event.pos().y()
        (lon, lat) = CanvasUtilities.convert_window_to_world(self, x, y)
        self.controller.set_footer_description('Cursor at ({}x, {}y) -> ({}°, {}°). {}'.format(x, y, lon, lat, 
            '' if self.controller.free_map_mode else 'Click to place path point.'))

    def is_path_same(self):
        if len(self.path) != len(self.controller.current_path):
            return False
        for i in range(len(self.path)):
            if self.path[i][0] != self.controller.current_path[i].x or self.path[i][1] != self.controller.current_path[i].y:
                return False
        return True

    def leaveEvent(self, event):
        self.controller.set_footer_description('')

    def wheelEvent(self, event):
        if (self.controller.free_map_mode):
            zoom_value = event.angleDelta() * 0.2
            self.controller.plot_zoom((zoom_value.y(), zoom_value.y()))

    def resizeEvent(self, event):
        # The aspect ratio seeks to make the plot fit the window
        self.axes.set_aspect('auto')
        
        super(MapCanvas, self).resizeEvent(event)

    
