import sys
from PyQt5.QtWidgets import QApplication
from MainController import MainController
from Components.MainWindow import MainWindow


def run_application():
    # Create the app.
    app = QApplication(sys.argv)
    app.setStyle("QtCurve")
    
    # Create the controller and the window.
    controller = MainController()
    window = MainWindow(controller)
    
    # Show the window and launch the application.
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
