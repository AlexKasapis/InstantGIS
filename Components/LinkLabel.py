from PyQt5.QtWidgets import QLabel
import webbrowser


class LinkLabel(QLabel):
    def __init__(self, parent=None):
        super(LinkLabel, self).__init__(parent)

    def mousePressEvent(self, e):
        webbrowser.open(string(self.text()), new=2)