import win32gui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton
from Components.AnchorMenu import AnchorMenu
from Settings import Utilities
from Settings import CanvasUtilities


class Anchor(QPushButton):

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
        
        self.setGeometry(self.x, self.y, 12, 12) 
        self.setStyleSheet("""  
            background-color: #CCBF8F;
            border-radius: 6; 
            border: 2px solid #808080;
            """)

        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.clicked.connect(self.anchor_clicked)

    def anchor_clicked(self):
        if self.controller.free_map_mode:
            _, _, (x, y) = win32gui.GetCursorInfo()
            anchor_menu = AnchorMenu(self.lon, self.lat, x, y)
            anchor_menu.accepted.connect(self.update_coordinates)
            anchor_menu.exec_()

    def update_coordinates(self, values):
        self.lon = values['Longitude']
        self.lat = values['Latitude']
        self.controller.update_limits()

    def enterEvent(self, event):
        super(Anchor, self).enterEvent(event)

    def leaveEvent(self, event):
        self.controller.set_footer_description('')
        super(Anchor, self).leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.mouse_click_rel_pos = event.pos()
        super(Anchor, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_mouse_pressed:
            self.is_mouse_pressed = False

        if not self.is_anchor_dragged:
            super(Anchor, self).mouseReleaseEvent(event)
        else:
            self.is_anchor_dragged = False

    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed:
            self.is_anchor_dragged = True

            if self.controller.free_map_mode:
                new_x = Utilities.clamp(self.mapToParent(event.pos()).x() - self.mouse_click_rel_pos.x(), 0, self.parent().width())
                new_y = Utilities.clamp(self.mapToParent(event.pos()).y() - self.mouse_click_rel_pos.y(), 0, self.parent().height())

                if Utilities.get_euclidean_distance((new_x, new_y), self.controller.get_other_anchor(self).get_window_coordinates()) < 15:
                    return

                # Apply the move.
                self.setGeometry(new_x, new_y, self.width(), self.height())
                self.x = new_x
                self.y = new_y
                (lon, lat) = CanvasUtilities.convert_window_to_world(self.controller.map_canvas, self.x, self.y)
                self.lon = lon
                self.lat = lat

                #self.controller.fix_anchor_world_coordinates()
                
                # Update plot limits
                #self.controller.update_limits()
        super(Anchor, self).mouseMoveEvent(event)

    def get_window_coordinates(self):
        return (self.x, self.y)

    @staticmethod
    def get_point_diff(p1, p2):
        return p2.x() - p1.x(), p2.y() - p1.y()
