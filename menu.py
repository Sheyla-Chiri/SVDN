import sys
# from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QPushButton, QAction
from PyQt5 import uic, QtCore, QtGui
import time
import login


class Principal(QMainWindow):   # Clase heredada de QMainWindow(Constructor de Ventanas)
    # Metodo constructor de la clase
    def __init__(self, parent=None, *datos):
        # Iniciamos el objeto QMainWindow
        super(Principal, self).__init__(parent)
        # Cargar la configuracion del archivo .ui en el objeto
        uic.loadUi("pantallas/menu.ui", self)

        # MainWindow
        # Agrandar la ventana
        self.setWindowTitle("SVDN ENTERPRISE " + time.strftime("%c"))
        self.setGeometry(600, 400, 1000, 500)
        self.showMaximized()

        self.actionSalir.triggered.connect(self.salirApp)

    # funcion para cerrar ventana
    def salirApp(self):
        cerrar = QMessageBox()

        cerrar.setWindowTitle("¿Salir del SVDN ENTERPRISE?")
        cerrar.setIcon(QMessageBox.Question)
        cerrar.setText("¿Estas seguro que deseas cerrar SVDN ENTERPRISE?")
        salirBtn = cerrar.addButton("Salir", QMessageBox.YesRole)
        cancelarBtn = cerrar.addButton("Cancelar", QMessageBox.NoRole)

        cerrar.exec_()

        if cerrar.clickedButton() == salirBtn:
            self.close()


# codigo para lanzar la aplicacion
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Principal()
    main.show()
    sys.exit(app.exec_())
