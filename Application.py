import sys
from PyQt5 import QtWidgets
from MainWindow import MainWindow


def run_application():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("QtCurve")
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
