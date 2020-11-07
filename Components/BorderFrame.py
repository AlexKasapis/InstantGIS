import win32gui
import enum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel, QWidget
from Settings import ResizeUtilities

# Denoting the four different placements of a border.
class BorderOrientation(enum.Enum):
    Left = 1
    Top = 2
    Right = 3
    Bottom = 4

class BorderFrame(QLabel):

    def __init__(self, orientation, controller, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
    
        self.border_orientation = orientation
        self.controller = controller

        # Keep track of the mouse drag.
        self.prev_cursor_pos = (-1, -1)

        # Keeping track of the resizing mode.
        self.is_mouse_pressed = False
        self.resize_orientation = None
        self.diagonal_resize_threshold = 8
        
        # Set geometry and style.
        if self.border_orientation == BorderOrientation.Left or self.border_orientation == BorderOrientation.Right:
            self.setFixedWidth(3)
        else:
            self.setFixedHeight(3)
        self.setStyleSheet('''
            background-color: #323232;''')

        # Fire the mouseMouseEvent always to keep track of when we need to change to diagonal resize and back.
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.resize_orientation = ResizeUtilities.get_resize_mode(
            self.border_orientation,
            self.width(),
            self.height(),
            self.diagonal_resize_threshold,
            event.x(),
            event.y())
        self.set_cursor(False)

    def leaveEvent(self, event):
        self.is_mouse_pressed = False
        self.set_cursor(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_mouse_pressed:
            self.is_mouse_pressed = False  

    def mouseMoveEvent(self, event):
        if not self.is_mouse_pressed:
            self.resize_orientation = ResizeUtilities.get_resize_mode(
                self.border_orientation,
                self.width(),
                self.height(),
                self.diagonal_resize_threshold,
                event.x(),
                event.y())
            self.set_cursor(False)

        # Get the distance the cursor traveled since the last call of this function.
        _, _, (x, y) = win32gui.GetCursorInfo()
        distance = (x - self.prev_cursor_pos[0], y - self.prev_cursor_pos[1])
        
        # Update the cursor position.
        self.prev_cursor_pos = (x, y)
        
        if self.is_mouse_pressed:
            self.controller.resize_window(self, distance)
        else:
            return

    def set_cursor(self, reset):
        cursor = QCursor()

        if reset:
            cursor.setShape(Qt.SizeAllCursor)
        else:
            if self.resize_orientation == ResizeUtilities.ResizeOrientation.Left:
                cursor.setShape(Qt.SizeHorCursor)
            elif self.resize_orientation == ResizeUtilities.ResizeOrientation.TopLeft:
                cursor.setShape(Qt.SizeFDiagCursor)
            elif self.resize_orientation == ResizeUtilities.ResizeOrientation.Top:
                cursor.setShape(Qt.SizeVerCursor)
            elif self.resize_orientation == ResizeUtilities.ResizeOrientation.TopRight:
                cursor.setShape(Qt.SizeBDiagCursor)
            elif self.resize_orientation == ResizeUtilities.ResizeOrientation.Right:
                cursor.setShape(Qt.SizeHorCursor)
            elif self.resize_orientation == ResizeUtilities.ResizeOrientation.BottomRight:
                cursor.setShape(Qt.SizeFDiagCursor)
            elif self.resize_orientation == ResizeUtilities.ResizeOrientation.Bottom:
                cursor.setShape(Qt.SizeVerCursor)
            else:
                cursor.setShape(Qt.SizeBDiagCursor)
        
        QWidget.setCursor (self, cursor)
