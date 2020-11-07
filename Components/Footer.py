from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from Settings import ResizeUtilities


class Footer(QFrame):

    def __init__(self, controller, *args, **kwargs):
        
        QFrame.__init__(self, *args, **kwargs)

        self.controller = controller
        self.controller.footer = self
        
        self.setFixedHeight(20)
        self.setStyleSheet('''background-color: #323232;''')

        # Layout
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(3, 0, 2, 0)
        self.setLayout(layout)

        self.description_label = QLabel('')
        self.description_label.setStyleSheet('''
            color: #808080;
            font-weight: 500;''')
        
        self.mode_label = QLabel('')
        self.mode_label.setStyleSheet('''
            color: #808080;
            font-weight: 500;''')

        layout.addWidget(self.description_label, 1, Qt.AlignLeft)
        layout.addWidget(self.mode_label, 0, Qt.AlignRight)

        self.update_mode_label()

    def update_mode_label(self):
        self.mode_label.setText('(Free map mode)' if self.controller.free_map_mode else '(Path creation mode)')
