from PyQt5 import QtCore, QtGui, QtWidgets


class GISFrame(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)

        self.anchor1 = None
        self.anchor2 = None
        self.current_path = []

        self.setAutoFillBackground(True)
        p = self.palette()
        color = QtGui.QColor("gray")
        color.setAlpha(50)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

        self.resetMap(True)
        self.redraw()

    def mousePressEvent(self, event):
        print(event)

    def resetMap(self, reset_path):
        self.anchor1 = ((0, 0), (-180, 90))
        self.anchor2 = ((0, self.height()), (-180, -90))
        if reset_path:
            self.current_path = []

    def redraw(self):
        pass
