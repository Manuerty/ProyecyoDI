from PyQt6 import QtWidgets, QtGui
import var


class Clientes:
    def altaCliente(self):
        dni = var.ui.txtDniCli.text()
        print(dni)