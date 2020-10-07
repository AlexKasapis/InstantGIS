from PyQt5 import QtCore, QtWidgets


class MainController(QtCore.QObject):

    def __init__(self, model, *args, **kwargs):
        QtCore.QObject.__init__(self)

        self.model = model

    def close_anchor_form(self):

        self.model.anchor1.form_is_visible = False
        self.model.anchor2.form_is_visible = False
