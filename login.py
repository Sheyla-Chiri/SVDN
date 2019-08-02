"""import sys
import re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow

# importamos de la carpeta pantallas el archivo de uilogin
from pantallas.uilogin import *

# importamos el archivo menu
# import menu

# importamos el archivo conexionbd de conexion a la base de datos
# import conexionbd


class Logueo(QMainWindow, UILogin):
    def __init__(self, parent=None):
        super(Logueo, self).__init__(parent)

        self.ui = UILogin()
        self.ui.iniGui()

        self.ui.applyBtn.clicked.connect(self.validar_formulario)

        self.ui.cancelBtn.clicked.connect(self.salir)
        self.ui.cancelBtn.returnPressed.connect(self.salir)
        print(self.ui.userLbl.text())

    def validar_nombre(self):
        user = self.userLbl.text()
        print(user)
        validar = re.match('[0]+$', user, re.I)
        if user == "":
            self.user.setStyleSheet("border: 1px solod yellow;")
            return False
        elif not validar:
            self.user.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.user.setStyleSheet("border: 1px solid green;")
            return True

    def validar_formulario(self):
        if self.validar_nombre():
            QMessageBox.information(self, "Formulario Correcto", "Validacion correcta", QMessageBox.Discard)
        else:
            QMessageBox.warning(self, "Formulario Incorrecto", "Validacion incorrecta", QMessageBox.Discard)

    # funcion para cerrar ventana
    def salir(self):
        # se cierra la ventana
        self.close()
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic, QtGui
import conexion
import menu
from clases import encriptar


class Login(QMainWindow):   # Clase heredada de QMainWindow(Constructor de Ventanas)
    # Metodo constructor de la clase
    def __init__(self):
        # Iniciamos el objeto QMainWindow
        QMainWindow.__init__(self)
        # Cargar la configuracion del archivo .ui en el objeto
        uic.loadUi("pantallas/login.ui", self)

        # Imagen Principal
        self.imagePath = "./image/login.jpg"
        self.image = QtGui.QImage(self.imagePath)
        self.pixmapImage = QtGui.QPixmap.fromImage(self.image)
        self.label.setPixmap(self.pixmapImage)
        self.label.setScaledContents(True)

        # boton Cancelar
        self.cancelarBtn.clicked.connect(self.salir)

        # boton Ingresar
        self.ingresarBtn.clicked.connect(self.permisos)  # (self.campo_vacio)

    # funcion para cerrar ventana
    def salir(self):
        # se cierra la ventana
        self.close()

    # metodo para cotejar los campos de logueo
    def campo_vacio(self):
        # valora si la longitud del campo es 0
        if len(self.usuarioLbl.text()) == 0:
            # mensaje falta ususario
            QMessageBox.warning(self, "Informacion", "Necesita ingresar su usuario", QMessageBox.Ok)
            # print "te faltan usuario"
        # valora si la longitud del campo es 0
        elif len(self.contrasenaLbl.text()) == 0:
            # mensaje falta contraseña
            QMessageBox.warning(self, "Informacion", "Necesita ingresar su contraseña", QMessageBox.Ok)
            # print "te falta contraseña"
        else:
            # llama al metodo usuario
            self.usuario()

    # funcion para checar si el usuario existe en la bd
    def usuario(self):
        # se toma el valor de el campo usuario
        usuario = self.usuarioLbl.text()  # unicode()
        # se crea una consulta a la bd para cotejar usuario
        query = "SELECT usuario, clave FROM admusuario WHERE usuario ='" + usuario + "'"
        # se ejecuta la consulta
        self.datos = conexion.consultas(query)
        print(self.datos)
        # se coteja el resultado de la consulta si la longitud del campo es 0
        if len(self.datos) == 0:
            QMessageBox.warning(self, "Informacion", """No existe el usuario en la base de datos""", QMessageBox.Ok)
            # print "no existe el usuario en la bd"
        # se coteja si el usuario es igual el obtenido en la consulta a la bd
        elif usuario == self.datos[0][1]:
            # Se manda a llamar el metodo contraseña
            #self.contrasena()
            print("Conforme")
        # en caso contrario
        else:
            # mensaje de usuario incorrecto
            QMessageBox.warning(self, "Informacion", """Usuario incorrecto""", QMessageBox.Ok)
            # print "usuario incorrecto"

    # Metodo permisos
    def permisos(self):
        """"
        # se toma el valor de la consulta realizada
        permiso = self.datos[0][3]
        nombre = self.datos[0][1]
        datos = []
        datos.append(permiso)
        datos.append(nombre)
        # se cierra la ventana
        """
        datos = None
        self.close()
        # se asigna el archivo menu a la variable y se le pasa el parametro permiso
        ventana_2 = menu.Principal(self, datos)
        # se muestra la ventana
        ventana_2.show()


if __name__ == "__main__":      # Instancia para iniciar una aplicacion
    app = QApplication(sys.argv)    # Inicia la aplicacion
    ventana = Login()              # Se establece una ventana principal para arrancar
    ventana.show()                  # Muestra la ventana principal (por default estan ocultas)
    app.exec_()                     # Ejecutamos nuestra app
