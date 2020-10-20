import win32gui
from PyQt5 import QtWidgets, QtCore, QtGui
import enum

# Denoting the four different placements of a border.
class BorderOrientation(enum.Enum):
    Left = 1
    Top = 2
    Right = 3
    Bottom = 4

# Denoting the resize anchor orientation.
class ResizeOrientation(enum.Enum):
    Left = 1
    TopLeft = 2
    Top = 3
    TopRight = 4
    Right = 5
    BottomRight = 6
    Bottom = 7
    BottomLeft = 8

class BorderFrame(QtWidgets.QLabel):

    def __init__(self, orientation, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, *args, **kwargs)
    
        self.border_orientation = orientation

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
        self.set_resize_mode(event.x(), event.y())
        self.set_cursor(False)

    def leaveEvent(self, event):
        self.is_mouse_pressed = False
        self.set_cursor(True)

    def mousePressEvent(self, event):
        self.is_mouse_pressed = True

    def mouseReleaseEvent(self, event):
        self.is_mouse_pressed = False  

    def mouseMoveEvent(self, event):
        if not self.is_mouse_pressed:
            self.set_resize_mode(event.x(), event.y())
            self.set_cursor(False)

        # Get the distance the cursor traveled since the last call of this function.
        _, _, (x, y) = win32gui.GetCursorInfo()
        distance = (x - self.prev_cursor_pos[0], y - self.prev_cursor_pos[1])
        
        # Update the cursor position.
        self.prev_cursor_pos = (x, y)
        
        if self.is_mouse_pressed:
            self.resize_window(distance)
        else:
            return

    def resize_window(self, distance):

        # Depending on different resize modes, sometimes the window must be moved along with being resized
        # in order to produce the expected resizing functionality. Calculate the resize and move vectors.
        new_size, new_pos = self.get_resize_transformations(distance)

        # Apply the transformations.
        main_window = self.get_main_window()
        main_window.setFixedSize(new_size[0], new_size[1])
        main_window.move(new_pos[0], new_pos[1])
    
    def get_resize_transformations(self, distance):
        
        if self.resize_orientation == ResizeOrientation.Left:
            resize_vector = (-distance[0], 0)
            move_vector = (distance[0], 0)
        elif self.resize_orientation == ResizeOrientation.TopLeft:
            resize_vector = (-distance[0], -distance[1])
            move_vector = (distance[0], distance[1])
        elif self.resize_orientation == ResizeOrientation.Top:
            resize_vector = (0, -distance[1])
            move_vector = (0, distance[1])
        elif self.resize_orientation == ResizeOrientation.TopRight:
            resize_vector = (distance[0], -distance[1])
            move_vector = (0, distance[1])
        elif self.resize_orientation == ResizeOrientation.Right:
            resize_vector = (distance[0], 0)
            move_vector = (0, 0)
        elif self.resize_orientation == ResizeOrientation.BottomRight:
            resize_vector = (distance[0], distance[1])
            move_vector = (0, 0)
        elif self.resize_orientation == ResizeOrientation.Bottom:
            resize_vector = (0, distance[1])
            move_vector = (0, 0)
        else:
            resize_vector = (-distance[0], distance[1])
            move_vector = (distance[0], 0)

        main_window = self.get_main_window()
        geometry = main_window.geometry()
        new_size = (max(geometry.width() + resize_vector[0], 400), max(geometry.height() + resize_vector[1], 400))
        if self.is_resizing_from_left() and geometry.width() == new_size[0] == 400:
            move_vector = (0, move_vector[1])
        if self.is_resizing_from_top() and geometry.height() == new_size[1] == 400:
            move_vector = (move_vector[0], 0)
        new_pos = (geometry.x() + move_vector[0], geometry.y() + move_vector[1])
        return new_size, new_pos

    def is_resizing_from_left(self):
        if self.resize_orientation == ResizeOrientation.Left \
            or self.resize_orientation == ResizeOrientation.TopLeft \
            or self.resize_orientation == ResizeOrientation.BottomLeft:
                return True

    def is_resizing_from_top(self):
        if self.resize_orientation == ResizeOrientation.Top \
            or self.resize_orientation == ResizeOrientation.TopLeft \
            or self.resize_orientation == ResizeOrientation.TopRight:
                return True

    # TODO: Get rid of direct access to the main window. Pass the main controller everywhere and use its utility functions.
    def get_main_window(self):
        if self.border_orientation == BorderOrientation.Left:
            return self.parent().parent().parent()
        elif self.border_orientation == BorderOrientation.Top:
            return self.parent().parent()
        elif self.border_orientation == BorderOrientation.Right:
            return self.parent().parent().parent()
        else:
            return self.parent().parent()

    def set_resize_mode(self, x, y):
        if self.border_orientation == BorderOrientation.Left:
            if y <= self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.TopLeft
            elif y >= self.height() - self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.BottomLeft
            else:
                self.resize_orientation = ResizeOrientation.Left
        elif self.border_orientation == BorderOrientation.Top:
            if x <= self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.TopLeft
            elif x >= self.width() - self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.TopRight
            else:
                self.resize_orientation = ResizeOrientation.Top
        elif self.border_orientation == BorderOrientation.Right:
            if y <= self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.TopRight
            elif y >= self.height() - self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.BottomRight
            else:
                self.resize_orientation = ResizeOrientation.Right
        else:
            if x <= self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.BottomLeft
            elif x >= self.width() - self.diagonal_resize_threshold:
                self.resize_orientation = ResizeOrientation.BottomRight
            else:
                self.resize_orientation = ResizeOrientation.Bottom

    def set_cursor(self, reset):
        cursor = QtGui.QCursor()

        if reset:
            cursor.setShape(QtCore.Qt.SizeAllCursor)
        else:
            if self.resize_orientation == ResizeOrientation.Left:
                cursor.setShape(QtCore.Qt.SizeHorCursor)
            elif self.resize_orientation == ResizeOrientation.TopLeft:
                cursor.setShape(QtCore.Qt.SizeFDiagCursor)
            elif self.resize_orientation == ResizeOrientation.Top:
                cursor.setShape(QtCore.Qt.SizeVerCursor)
            elif self.resize_orientation == ResizeOrientation.TopRight:
                cursor.setShape(QtCore.Qt.SizeBDiagCursor)
            elif self.resize_orientation == ResizeOrientation.Right:
                cursor.setShape(QtCore.Qt.SizeHorCursor)
            elif self.resize_orientation == ResizeOrientation.BottomRight:
                cursor.setShape(QtCore.Qt.SizeFDiagCursor)
            elif self.resize_orientation == ResizeOrientation.Bottom:
                cursor.setShape(QtCore.Qt.SizeVerCursor)
            else:
                cursor.setShape(QtCore.Qt.SizeBDiagCursor)
        
        QtWidgets.QWidget.setCursor (self, cursor)
