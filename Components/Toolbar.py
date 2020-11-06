from PyQt5 import QtWidgets, QtCore, QtGui
from Components.Buttons.Toolbar.PlotResetButton import PlotResetButton
from Components.Buttons.Toolbar.PlotModeButton import PlotModeButton
from Components.Buttons.Toolbar.ExportButton import ExportButton
from Components.Buttons.Toolbar.HelpButton import HelpButton
from Components.Buttons.Toolbar.AboutUsButton import AboutUsButton


class Toolbar(QtWidgets.QFrame):

    def __init__(self, parent, controller, *args, **kwargs):
        QtWidgets.QFrame.__init__(self, *args, **kwargs)

        # Visuals
        self.setFixedWidth(40)
        self.setStyleSheet('''
            background-color: #323232;
            border: 0px''')

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(0, 1, 3, 1)
        self.setLayout(layout)
        layout.addWidget(PlotModeButton(self, controller))
        layout.addWidget(ExportButton(self, controller))
        layout.addWidget(PlotResetButton(self, controller))
        layout.addStretch(1)
        layout.addWidget(HelpButton(self, controller))
        layout.addWidget(AboutUsButton(self, controller))
