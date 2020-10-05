import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets


class ResizeButton(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(ResizeButton, self).__init__(*args, **kwargs)

        self.is_mouse_pressed = False
        self.mouse_pos = (0, 0)

        self.setText("")
        self.setPixmap(QtGui.QPixmap("icons/resize-48.png").scaled(20, 20, QtCore.Qt.KeepAspectRatio))
        self.setFixedSize(QtCore.QSize(20, 20))

    def mousePressEvent(self, *args, **kwargs):
        self.is_mouse_pressed = True
        self.mouse_pos = win32gui.GetCursorInfo()[2]

    def mouseReleaseEvent(self, *args, **kwargs):
        if not self.is_mouse_pressed:
            self.is_mouse_pressed = False

    def mouseMoveEvent(self, *args, **kwargs):
        if self.is_mouse_pressed:
            # Get the current mouse position.
            curr_mouse_position = win32gui.GetCursorInfo()[2]

            # Get the cursor's move vector.
            mouse_distance = self.get_point_diff(self.mouse_pos, curr_mouse_position)

            # Resize
            main_window = self.parent().parent().parent()
            new_w = main_window.width() + mouse_distance[0]
            new_h = main_window.height() + mouse_distance[1]
            main_window.resize(new_w, new_h)

            # Update the current mouse position.
            self.mouse_pos = curr_mouse_position

    @staticmethod
    def get_point_diff(p1, p2):
        return p2[0] - p1[0], p2[1] - p1[1]