from PyQt5 import QtCore

class Anchor(QtCore.QObject):

    modelChanged = QtCore.pyqtSignal()

    def __init__(self, x, y, lat, longi):
        QtCore.QObject.__init__(self)

        self.x = x
        self.y = y
        self.lat = lat
        self.long = longi

        self._form_is_visible = False

    @property
    def form_is_visible(self):
        return self._form_is_visible

    @form_is_visible.setter
    def form_is_visible(self, is_visible):
        self._form_is_visible = is_visible
        self.modelChanged.emit()

    def update(self, coords=None, pos=None):
        """ Updates either the coordinate or the position of the anchor """
        if coords is not None:
            self.lat = coords.x()
            self.long = coords.y()
        if pos is not None:
            self.x = pos.x()
            self.y = pos.y()
            
        self.modelChanged.emit()
