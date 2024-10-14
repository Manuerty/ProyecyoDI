from tabnanny import check

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QIcon



import conexion
import conexionserver
import var
import eventos


class Clientes:
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCli.setText(str(dni))
            check = eventos.Eventos.validarDNIcli(dni)
            if check:
                var.ui.txtDniCli.setStyleSheet('background-color: rgb(255,255,220)')
            else:
                var.ui.txtDniCli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniCli.setText(None)
                var.ui.txtDniCli.setFocus()
        except Exception as error:
            print("error en validar dni ", error)


    def checkEmail(mail):
        try:
            mail = str(var.ui.txtEmailCli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailCli.setText(mail.lower())

            else:
                var.ui.txtEmailCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailCli.setText(None)
                var.ui.txtEmailCli.setText("correo no válido")
                var.ui.txtEmailCli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def altaCliente(self):

        try:
            nuevoCli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(),
                        var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.txtDirCli.text(), var.ui.cmbProCli.currentText(),
                        var.ui.cmbMuniCli.currentText()]
            if var.ui.txtDniCli.text() != '':
                if conexion.Conexion.altaCliente(nuevoCli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Cliente dado de alta en la base de datos')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)
                else:
                    QtWidgets.QMessageBox.critical(None, 'Error', 'Error al dar de alta el cliente',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return "False"
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'El DNI no puede estar vacío',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return "False"

        except Exception as e:
            print("error altaCliente", e)


    def cargaTablaClientes(self):
        try:
            listado= conexion.Conexion.listadoClientes(self)
            #listado = conexionserver.ConexionServer.listadoClientes(self)
            index = 0
            for registro in listado:
                var.ui.tablaClientes.setRowCount(index + 1)
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem((registro[2])))
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem((registro[3])))
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(("  " + registro[5] + "  ")))
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem((registro[7])))
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem((registro[8])))
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(("  " + registro[9] + "  ")))

                var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1

        except Exception as error:
            print("Error al cargar tabla clientes", error)