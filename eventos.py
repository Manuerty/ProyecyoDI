import sys
import conexion

from PyQt6 import QtWidgets, QtGui

import var


class Eventos():
    def mensajeSalir(self=None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
        mbox.setWindowTitle("Salir")
        mbox.setText("¿Desea usted salir?")
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText("Si")
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText("No")

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()


    def cargarProvincias(self):
        var.ui.cmbProCli.clear()
        listado = conexion.Conexion.listaProv(self)
        var.ui.cmbProCli.addItems(listado)

    def cargarMunicipios(self):
        var.ui.cmbMuniCli.clear()
        listado = conexion.Conexion.listaMuni(self)
        var.ui.cmbMuniCli.addItems(listado)

    def validarDNIcli(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDni.setText(str(dni))
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.lbldnicli.setStyleSheet('color:green;')  # si es válido se pone una V en color verde
                    var.ui.lbldnicli.setText('V')
                    return True
                else:
                    var.ui.lbldnicli.setStyleSheet('color:red;')  # y si no un aspa en color rojo
                    var.ui.lbldnicli.setText('X')
                    var.ui.txtdnicliente.setText(None)
                    var.ui.txtdnicliente.setFocus()
            else:
                var.ui.lbldnicli.setStyleSheet('color:red;')
                var.ui.lbldnicli.setText('X')
                var.ui.txtdnicliente.setText(None)
                var.ui.txtdnicliente.setFocus()

        except Exception as error:
            print("error en validar dni ", error)