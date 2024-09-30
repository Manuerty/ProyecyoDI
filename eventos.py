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
