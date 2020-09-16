from PyQt5 import QtCore, QtWidgets
from Header import Header
from GISFrame import GISFrame


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("InstantGIS")
        self.setMinimumSize(QtCore.QSize(640, 480))

        # Make background transparent.
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Structure the main layout.
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget = QtWidgets.QWidget()
        # main_widget.setStyleSheet("""
        #     background-color: #30475e;""")
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Header.
        header = Header(self)
        main_layout.addWidget(header, 0, QtCore.Qt.AlignTop)

        # Main body.
        gis_frame = GISFrame(self)
        main_layout.addWidget(gis_frame, 0, QtCore.Qt.AlignTop)

        # Footer.
        footer_frame = QtWidgets.QFrame(self)
        footer_frame.setStyleSheet("background-color:blue;")
        main_layout.addWidget(footer_frame, 0, QtCore.Qt.AlignBottom)
        footer_layout = QtWidgets.QHBoxLayout()
        footer_layout.setSpacing(0)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_frame.setLayout(footer_layout)

        close_button2 = QtWidgets.QPushButton("Close", self)
        close_button2.resize(100, 100)
        footer_layout.addWidget(close_button2, 0, QtCore.Qt.AlignLeft)
