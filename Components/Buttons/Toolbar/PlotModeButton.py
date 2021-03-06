from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class PlotModeButton(QPushButton):

    def __init__(self, parent, controller, *args, **kwargs):
        super(PlotModeButton, self).__init__(*args, **kwargs)

        # Visuals
        self.setFixedSize(QSize(37, 37))
        self.setText("")
        self.setIcon(QIcon("./Resources/Icons/icon_move.png"))
        self.setIconSize(QSize(30, 30))
        self.setStyleSheet('''
            background-color: #323232;
            border: 2px solid #808080;
            border-radius: 7px;''')

        # Connections
        self.clicked.connect(self.button_clicked)

        # Attributes
        self.controller = controller
        self.icon_move = QIcon("./Resources/Icons/icon_move.png")
        self.icon_pin = QIcon("./Resources/Icons/icon_pin.png")
        
        # Call functions
        self.set_icon()
        
    def button_clicked(self):
        self.controller.toggle_plot_mode()
        self.set_icon()

    def set_icon(self):
        self.setIcon(self.icon_move if self.controller.free_map_mode == True else self.icon_pin)

    def enterEvent(self, event):
        self.controller.set_footer_description('Change to {} mode'.format('path creation' if self.controller.free_map_mode else 'free map'))
        self.setStyleSheet('''
        background-color: #555555;
        border: 0px;
        border: 2px solid #808080;
        border-radius: 7px;''')

    def leaveEvent(self, event):
        self.controller.set_footer_description('')
        self.setStyleSheet('''
        background-color: #323232;
        border: 0px;
        border: 2px solid #808080;
        border-radius: 7px;''')

    def mousePressEvent(self, event):
        super(PlotModeButton, self).mousePressEvent(event)
        event.accept()