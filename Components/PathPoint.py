from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton
from Components.AnchorMenu import AnchorMenu
from Settings import Utilities


class PathPoint(QPushButton):

    def __init__(self, window_pos, world_coord, controller, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)

        self.x = window_pos[0]
        self.y = window_pos[1]
        self.lon = world_coord[0]
        self.lat = world_coord[1]
        self.controller = controller

        # Dragging
        self.is_mouse_pressed = False
        self.is_anchor_dragged = False
        self.mouse_click_rel_pos = None
        
        # Set the geometry, shape and color of the point object.
        self.reset_visuals()

        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def enterEvent(self, event):
        self.controller.set_footer_description('Path point at ({}x, {}y) -> ({}°, {}°). Left click to drag, right click to remove.'.format(self.x, self.y, self.lon, self.lat))
        super(PathPoint, self).enterEvent(event)

    def leaveEvent(self, event):
        self.controller.set_footer_description('')
        super(PathPoint, self).leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.mouse_click_rel_pos = event.pos()
        super(PathPoint, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_mouse_pressed:
            self.is_mouse_pressed = False

        if not self.is_anchor_dragged and event.button() == Qt.RightButton:
            self.controller.remove_path_point(self)
        else:
            self.is_anchor_dragged = False

    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed:
            self.is_anchor_dragged = True

            new_x = Utilities.clamp(self.mapToParent(event.pos()).x() - self.mouse_click_rel_pos.x(), 0, self.parent().width())
            new_y = Utilities.clamp(self.mapToParent(event.pos()).y() - self.mouse_click_rel_pos.y(), 0, self.parent().height())

            if Utilities.get_euclidean_distance((new_x, new_y), self.controller.get_other_anchor(self).get_window_coordinates()) < 15:
                return

            # Apply the move.
            self.setGeometry(new_x, new_y, self.width(), self.height())
            self.x = new_x
            self.y = new_y

            self.controller.fix_path_world_coordinates()
            self.controller.redraw_path()
        super(PathPoint, self).mouseMoveEvent(event)

    def get_window_coordinates(self):
        return (self.x, self.y)

    @staticmethod
    def get_point_diff(p1, p2):
        return p2.x() - p1.x(), p2.y() - p1.y()

    def reset_visuals(self):
        colors = ['#C7371E', '#02D444']
        sizes = [5, 6, 7]
        radius_sizes = [2, 3, 3]

        size = sizes[self.controller.point_size_index]
        color = colors[self.controller.path_color_index]
        border_radius = radius_sizes[self.controller.point_size_index]

        self.setGeometry(self.x - int(size / 2), self.y - int(size / 2), size, size) 
        self.setStyleSheet('background-color: {}; border-radius: {}; border: 0px;'.format(color, border_radius))