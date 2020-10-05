from PyQt5 import QtCore, QtGui, QtWidgets


class ProjectionAnchorButton(QtWidgets.QPushButton):
    def __init__(self, main_ctrl, *args, **kwargs):
    
        self.main_ctrl = main_ctrl
        super(ProjectionAnchorButton, self).__init__(*args, **kwargs) 
        
        self.setText("")
        self.setIcon(QtGui.QIcon("icons/icons8-map-pin-48.png"))
        self.setIconSize(QtCore.QSize(35, 35))
        self.setCheckable(True)
        self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        print("Clicked on Projection Anchor Button!")
        
        if self.isChecked():
            self.main_ctrl.projection_anchor_enable()
        else:
            self.main_ctrl.projection_anchor_disable()