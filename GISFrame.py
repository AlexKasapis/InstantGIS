from PyQt5 import QtCore, QtGui, QtWidgets


class GISFrame(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        left_bar = QtWidgets.QWidget(self)
        left_bar.setFixedWidth(3)
        left_bar.setStyleSheet("""
            background-color:#cbaf87;""")
        layout.addWidget(left_bar, QtCore.Qt.AlignLeft)

        main_frame = MainFrame(self)
        layout.addWidget(main_frame, QtCore.Qt.AlignLeft)

        right_bar = QtWidgets.QWidget(self)
        right_bar.setFixedWidth(3)
        right_bar.setStyleSheet("""
            background-color:#cbaf87;""")
        layout.addWidget(right_bar, QtCore.Qt.AlignLeft)


class MainFrame(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)

        self.setAutoFillBackground(True)
        p = self.palette()
        color = QtGui.QColor("gray")
        color.setAlpha(50)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def mousePressEvent(self, event):
        print(event)
