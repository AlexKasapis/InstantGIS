from PyQt5.QtWidgets import QLineEdit


class LineInput(QLineEdit):
    def __init__(self, parent=None):
        super(LineInput, self).__init__(parent)

    def mousePressEvent(self, e):
        self.selectAll()  