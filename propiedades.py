from xml.sax.handler import property_interning_dict

import conexion
import var
from PyQt6 import QtWidgets, QtGui, QtCore

class Propiedades():

    def altaTipoPropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtTipoProp.text().title()
            registro = conexion.Conexion.altaTipoProp(tipo)
            if registro:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Tipo añadido a la BBDD")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                var.ui.cmbTipoProp.clear()
                var.ui.cmbTipoProp.addItems(registro)
                var.dlggestion.ui.txtTipoProp.setText('')
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Ya existe ese tipo en la BBDD")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print('Error altaTipoPropiedad: %s ' % str(error))

    def bajaTipoPropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtTipoProp.text().title()
            if conexion.Conexion.bajaTipoProp(tipo):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Tipo dado de baja")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                var.dlggestion.ui.txtTipoProp.setText('')
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("No se ha podido dar de baja el tipo")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print('Error bajaTipoPropiedad: %s ' % str(error))

    def altaPropiedad(self):
        try:
            propiedad = [ var.ui.txtFechaAltaProp.text(), var.ui.txtDirProp.text(),
                          var.ui.cmbProvProp.currentText(), var.ui.cmbMuniProp.currentText(), var.ui.cmbTipoProp.currentText(),
                          var.ui.spinNumhabitProp.text(), var.ui.spinNumbanProp.text(), var.ui.txtSuperficieProp.text(),
                          var.ui.txtPrecioVProp.text(), var.ui.txtPrecioAProp.text(), var.ui.txtCpProp.text(),
                          var.ui.textDescriptProp.toPlainText()]

            tipoOper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipoOper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipoOper.append(var.ui.chkIntercambioProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipoOper.append(var.ui.chkVentaProp.text())

            propiedad.append(tipoOper)

            if var.ui.rbtAlquiladoProp.isChecked():
                propiedad.append(var.ui.rbtAlquiladoProp.text())
            elif var.ui.rbtVendidoProp.isChecked():
                propiedad.append(var.ui.rbtVendidoProp.text())
            elif var.ui.rbtDisponibleProp.isChecked():
                propiedad.append(var.ui.rbtDisponibleProp.text())


            propiedad.append(var.ui.txtPropietarioProp.text())
            propiedad.append(var.ui.txtMovilpropietarioProp.text())
            conexion.Conexion.altaPropiedad(propiedad)
            print(propiedad)

        except Exception as error:
            print('Error altaPropiedad: %s ' % str(error))

