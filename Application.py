import sys
from PyQt5 import QtWidgets
from MainWindow import MainWindow
from Controllers.MainController import MainController
from Models.Model import Model

def run_application():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("QtCurve")
    
    model = Model()
    main_ctrl = MainController(model)
    main_window = MainWindow(model, main_ctrl)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
