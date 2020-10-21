from PyQt5 import QtCore, QtWidgets
from MainController import MainController
from Components.Header import Header
from Components.GISFrame import GISFrame
from Components.BorderFrame import BorderFrame, BorderOrientation


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, controller, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.controller = controller
        self.controller.main_window = self

        self.setWindowTitle('InstantGIS')
        self.setMinimumSize(QtCore.QSize(self.controller.get_window_min_width(), self.controller.get_window_min_height()))

        # Make background transparent
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Structure the main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Top border.
        top_border = BorderFrame(BorderOrientation.Top, self.controller, parent=main_widget)
        main_layout.addWidget(top_border, QtCore.Qt.AlignTop)

        # Header
        header = Header(self.controller, parent=main_widget)
        main_layout.addWidget(header, QtCore.Qt.AlignTop)

        # Main body
        center_widget = QtWidgets.QWidget(main_widget)
        center_layout = QtWidgets.QHBoxLayout()
        center_widget.setLayout(center_layout)
        center_layout.setSpacing(0)
        center_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(center_widget, QtCore.Qt.AlignTop)

        # Main body -> Left border.
        left_border = BorderFrame(BorderOrientation.Left, self.controller, parent=center_widget)
        center_layout.addWidget(left_border, QtCore.Qt.AlignLeft)

        # Main body -> GIS frame
        gis_frame = GISFrame(self.controller, parent=center_widget)
        center_layout.addWidget(gis_frame, QtCore.Qt.AlignLeft)

        # Main body -> Right border.
        right_border = BorderFrame(BorderOrientation.Right, self.controller, parent=center_widget)
        center_layout.addWidget(right_border, QtCore.Qt.AlignLeft)

        # Bottom border.
        bottom_border = BorderFrame(BorderOrientation.Bottom, self.controller, parent=main_widget)
        main_layout.addWidget(bottom_border, QtCore.Qt.AlignTop)
