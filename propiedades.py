import conexion
import var
from PyQt6 import QtWidgets, QtGui, QtCore

class Propiedades():

    def altaTipoPropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtTipoProp.text().title()
            registro = conexion.Conexion.altaTipoProp(tipo)
            if registro:
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

    # def bajaTipoPropiedad(self):
    #     try:
    #         tipo = var.dlggestion.ui.txtTipoProp.text().title()
    #         conexion.Conexion.bajaTipoProp(tipo)
    #     except Exception as error:
    #         print('Error bajaTipoPropiedad: %s ' % str(error))



