from PyQt5 import QtCore, QtWidgets

class MainController(QtCore.QObject):

    def __init__(self, model, *args, **kwargs):
        QtCore.QObject.__init__(self)

        self.model = model
        self.adding_anchors_flag = False

    def projection_anchor_enable(self):
        self.adding_anchors_flag = True
        self.model.footer_description_label = "Click a point to add the first anchor"
        
        self.model.announce_update()        
       
    def projection_anchor_disable(self):
        self.adding_anchors_flag = False
        self.model.footer_description_label = ""

        self.model.announce_update()