from PyQt5 import QtCore, QtWidgets
from Header import Header
from GISFrame import GISFrame
from Footer import Footer
from Controllers.MainController import MainController


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, model, main_ctrl, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.model = model
        self.main_ctrl = main_ctrl

        self.setWindowTitle("InstantGIS")
        self.setMinimumSize(QtCore.QSize(640, 480))

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

        # Header
        header = Header(self.main_ctrl, parent=self)
        main_layout.addWidget(header, QtCore.Qt.AlignTop)

        # Main body
        center_widget = QtWidgets.QWidget(self)
        center_layout = QtWidgets.QHBoxLayout()
        center_widget.setLayout(center_layout)
        center_layout.setSpacing(0)
        center_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(center_widget, QtCore.Qt.AlignTop)

        # Main body -> Left bar.
        left_bar = QtWidgets.QWidget(center_widget)
        left_bar.setFixedWidth(3)
        left_bar.setStyleSheet("""
            background-color:#cbaf87;""")
        center_layout.addWidget(left_bar, QtCore.Qt.AlignLeft)

        # Main body -> GIS frame
        gis_frame = GISFrame(self.main_ctrl, self.model, parent=center_widget)
        center_layout.addWidget(gis_frame, QtCore.Qt.AlignLeft)

        # Main body -> Right bar.
        right_bar = QtWidgets.QWidget(center_widget)
        right_bar.setFixedWidth(3)
        right_bar.setStyleSheet("""
            background-color:#cbaf87;""")
        center_layout.addWidget(right_bar, QtCore.Qt.AlignLeft)

        # Footer.
        footer = Footer(self.main_ctrl, self.model, parent=self)
        main_layout.addWidget(footer, QtCore.Qt.AlignTop)