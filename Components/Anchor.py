from PyQt5 import QtCore, QtGui, QtWidgets
from Components.AnchorMenu import AnchorMenu
from Settings import Utilities


class Anchor(QtWidgets.QPushButton):

    def __init__(self, window_pos, world_coord, controller, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)

        self.x = window_pos[0]
        self.y = window_pos[1]
        self.lon = world_coord[0]
        self.lat = world_coord[1]
        self.controller = controller

        # Dragging
        self.is_mouse_pressed = False
        self.is_anchor_dragged = False
        self.mouse_click_rel_pos = None
        
        self.setGeometry(self.x, self.y, 10, 10) 
        self.setStyleSheet("""  
            background-color: gold;
            border-radius: 5; 
            border: 1px solid black
            """)

        self.setMouseTracking(True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.clicked.connect(self.anchor_clicked)

    def anchor_clicked(self):
        anchor_menu = AnchorMenu(self.lon, self.lat)
        anchor_menu.accepted.connect(self.update_coordinates)
        anchor_menu.exec_()

    def update_coordinates(self, values):
        self.lon = values['Longitude']
        self.lat = values['Latitude']
        self.controller.update_limits()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_mouse_pressed = True
            self.mouse_click_rel_pos = event.pos()
        super(Anchor, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.is_mouse_pressed:
            self.is_mouse_pressed = False

        if not self.is_anchor_dragged:
            super(Anchor, self).mouseReleaseEvent(event)
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

            self.controller.fix_anchor_world_coordinates()
            
            # Update plot limits
            self.controller.update_limits()
        super(Anchor, self).mouseMoveEvent(event)

    def get_window_coordinates(self):
        return (self.x, self.y)

    @staticmethod
    def get_point_diff(p1, p2):
        return p2.x() - p1.x(), p2.y() - p1.y()
