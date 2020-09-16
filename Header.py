import win32gui
from PyQt5 import QtCore, QtWidgets
from Buttons.NewPathPointButton import NewPathPointButton
from Buttons.ProjectionAnchorButton import ProjectionAnchorButton
from Buttons.LockDragButton import LockDragButton
from Buttons.HelpButton import HelpButton
from Buttons.MinimizeButton import MinimizeButton
from Buttons.CloseButton import CloseButton


class Header(QtWidgets.QFrame):

    def __init__(self, *args, **kwargs):
        QtWidgets.QFrame.__init__(self, *args, **kwargs)

        self.is_mouse_pressed = False
        self.mouse_pos = (0, 0)

        self.setStyleSheet("background-color:#cbaf87;")

        # Layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(5, 2, 5, 2)
        self.setLayout(header_layout)

        new_path_point_button = NewPathPointButton(self)
        header_layout.addWidget(new_path_point_button, 0, QtCore.Qt.AlignLeft)

        projection_anchor_button = ProjectionAnchorButton(self)
        header_layout.addWidget(projection_anchor_button, 0, QtCore.Qt.AlignLeft)

        lock_drag_button = LockDragButton(self)
        header_layout.addWidget(lock_drag_button, 1, QtCore.Qt.AlignLeft)

        help_button = HelpButton(self)
        header_layout.addWidget(help_button, 0, QtCore.Qt.AlignLeft)

        minimize_button = MinimizeButton(self)
        header_layout.addWidget(minimize_button, 0, QtCore.Qt.AlignLeft)

        close_button = CloseButton(self)
        header_layout.addWidget(close_button, 0, QtCore.Qt.AlignLeft)

    @staticmethod
    def close_button_click():
        QtCore.QCoreApplication.instance().quit()

    @staticmethod
    def add_point_button_click():
        print("Add point button clicked.")

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

            # Calculate the new position of the window.
            main_window = self.parent().parent()
            new_x = main_window.x() + mouse_distance[0]
            new_y = main_window.y() + mouse_distance[1]

            # Apply the move.
            main_window.move(new_x, new_y)

            # Update the current mouse position.
            self.mouse_pos = curr_mouse_position

    @staticmethod
    def get_point_diff(p1, p2):
        return p2[0] - p1[0], p2[1] - p1[1]
