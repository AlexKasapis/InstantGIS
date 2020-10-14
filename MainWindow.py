from PyQt5 import QtCore, QtWidgets
from Header import Header
from GISFrame import GISFrame
from Controllers.MainController import MainController
from Components.BorderFrame import BorderFrame, BorderOrientation
from Components.MapView import MapView



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, model, main_ctrl, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.model = model
        self.main_ctrl = main_ctrl

        self.setWindowTitle('InstantGIS')
        self.setMinimumSize(QtCore.QSize(800, 600))

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
        top_border = BorderFrame(BorderOrientation.Top, parent=main_widget)
        main_layout.addWidget(top_border, QtCore.Qt.AlignTop)

        # Header
        header = Header(self.main_ctrl, parent=main_widget)
        main_layout.addWidget(header, QtCore.Qt.AlignTop)

        # Main body
        center_widget = QtWidgets.QWidget(main_widget)
        center_layout = QtWidgets.QHBoxLayout()
        center_widget.setLayout(center_layout)
        center_layout.setSpacing(0)
        center_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(center_widget, QtCore.Qt.AlignTop)

        # Main body -> Left border.
        left_border = BorderFrame(BorderOrientation.Left, parent=center_widget)
        center_layout.addWidget(left_border, QtCore.Qt.AlignLeft)

        # Main body -> GIS frame
        gis_frame = GISFrame(self.main_ctrl, self.model, parent=center_widget)
        center_layout.addWidget(gis_frame, QtCore.Qt.AlignLeft)

        # Main body -> Right border.
        right_border = BorderFrame(BorderOrientation.Right, parent=center_widget)
        center_layout.addWidget(right_border, QtCore.Qt.AlignLeft)

        # Bottom border.
        bottom_border = BorderFrame(BorderOrientation.Bottom, parent=main_widget)
        main_layout.addWidget(bottom_border, QtCore.Qt.AlignTop)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.main_ctrl.close_anchor_form()