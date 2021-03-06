import win32gui
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from Components.Buttons.Header.MinimizeButton import MinimizeButton
from Components.Buttons.Header.CloseButton import CloseButton


class Header(QFrame):

    def __init__(self, controller, *args, **kwargs):
        
        QFrame.__init__(self, *args, **kwargs)

        self.controller = controller
        
        self.is_mouse_pressed = False
        self.mouse_pos = (0, 0)

        self.setFixedHeight(30)
        self.setStyleSheet('''background-color: #323232;''')

        # Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(header_layout)

        title_label = QLabel('InstantGIS')
        title_label.setStyleSheet('''
            color: #808080;
            font-weight: 500''')
        header_layout.addWidget(title_label, 1, Qt.AlignLeft)

        minimize_button = MinimizeButton(self)
        header_layout.addWidget(minimize_button, 0, Qt.AlignLeft)

        close_button = CloseButton(self)
        header_layout.addWidget(close_button, 0, Qt.AlignLeft)

    @staticmethod
    def close_button_click():
        QCoreApplication.instance().quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.mouse_pos = win32gui.GetCursorInfo()[2]

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_mouse_pressed:
            self.is_mouse_pressed = False

    def mouseMoveEvent(self, event):
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
