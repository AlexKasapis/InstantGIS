from PyQt5 import QtCore, QtWidgets
from Header import Header
from GISFrame import GISFrame
from Footer import Footer


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
        main_layout.addWidget(header, QtCore.Qt.AlignTop)

        # Main body.
        gis_frame = GISFrame(self)
        main_layout.addWidget(gis_frame, QtCore.Qt.AlignTop)

        # Footer.
        footer = Footer(self)
        main_layout.addWidget(footer, QtCore.Qt.AlignTop)
