from tabnanny import check

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QIcon

import clientes
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


    def checktelefono(tlf):
        try:
            tlf = str(var.ui.txtMovilCli.text())
            if eventos.Eventos.chekTelefono(tlf):
                var.ui.txtMovilCli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtMovilCli.setText(tlf)

            else:
                var.ui.txtMovilCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilCli.setText(None)
                var.ui.txtMovilCli.setText("telefono no válido")
                var.ui.txtMovilCli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    def altaCliente(self):
        try:
            nuevoCli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(),
                         var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                         var.ui.txtDirCli.text(), var.ui.cmbProCli.currentText(),
                         var.ui.cmbMuniCli.currentText()]
            camposObligatorios = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(), var.ui.txtNomCli.text(),
                                    var.ui.txtMovilCli.text(), var.ui.txtDirCli.text(), var.ui.cmbProCli.currentText(), var.ui.cmbMuniCli.currentText()]
            for i in range(len(camposObligatorios)):
                if camposObligatorios[i] == "":
                    QtWidgets.QMessageBox.critical(None, 'Error', "Faltan campos por cubrir")
                    return
                else:
                    pass
            if not conexion.Conexion.altaCliente(nuevoCli):
                QtWidgets.QMessageBox.critical(None, 'Error', "Ha ocurrido un error")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Cliente grabado en la base de datos")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
                eventos.Eventos.clearCampos(self)
        except Exception as e:
            print("error alta cliente",e)


    def cargaTablaClientes(self):
        try:
            listado= conexion.Conexion.listadoClientes(self)
            #listado = conexionserver.ConexionServer.listadoClientes(self)
            index = 0
            var.ui.tablaClientes.setRowCount(len(listado))
            if not listado:
                var.ui.tablaClientes.setRowCount(1)
                var.ui.tablaClientes.setItem(0, 2, QtWidgets.QTableWidgetItem("No existen Clientes con ese DNI"))
                var.ui.tablaClientes.item(0 , 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                for registro in listado:
                    var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem((registro[0])))
                    var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem((registro[3])))
                    var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem((registro[4])))
                    var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(("  " + registro[6] + "  ")))
                    var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem((registro[8])))
                    var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem((registro[9])))
                    var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(("  " + registro[2] + "  ")))

                    var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1

        except Exception as error:
            print("Error al cargar tabla clientes", error)

    def cargaOneCliente(self):
        try:
            fila = var.ui.tablaClientes.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneCliente(datos[0])
            listado = [var.ui.txtDniCli, var.ui.txtAltaCli, var.ui.txtBajaCli,  var.ui.txtApelCli,
                        var.ui.txtNomCli, var.ui.txtEmailCli, var.ui.txtMovilCli,
                        var.ui.txtDirCli, var.ui.cmbProCli,var.ui.cmbMuniCli ]
            for i in range(len(listado)):
                if i ==  8 or i == 9 :
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            return registro

        except Exception as error:
            print("Error al cargar tabla clientes", error)

    def modifCliente(self):
        try:
            modifcli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtBajaCli.text(), var.ui.txtApelCli.text(),
                        var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.txtDirCli.text(), var.ui.cmbProCli.currentText(),
                        var.ui.cmbMuniCli.currentText()]
            if conexion.Conexion.checkUserInDb(modifcli[0]):
                if conexion.Conexion.modifCliente(modifcli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Datos del cliente modificados')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    clientes.Clientes.cargaTablaClientes(self)
                    eventos.Eventos.clearCampos(self)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Error al modificar los datos del cliente')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('El cliente no existe en la base de datos')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print("Error en modifiCliente: ", error)



    def bajaCliente(self):
        try:

            datos = [var.ui.txtBajaCli.text(), var.ui.txtDniCli.text()]
            if conexion.Conexion.checkUserInDb(datos[1]):
                    if conexion.Conexion.bajaCliente(datos) :
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setWindowTitle('Aviso')
                        mbox.setWindowIcon(QIcon('./img/logo.ico'))
                        mbox.setText('Cliente borrado')
                        mbox.setStandardButtons(
                            QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()
                        clientes.Clientes.cargaTablaClientes(self)
                        eventos.Eventos.clearCampos(self)
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        mbox.setWindowTitle('Aviso')
                        mbox.setWindowIcon(QIcon('./img/logo.ico'))
                        mbox.setText('Error al dar de baja')
                        mbox.setStandardButtons(
                            QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('El cliente no existe en la base de datos')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print("Error en bajaCliente: ", error)


    def historicoCli(self):
        try:
            if var.ui.chkHistoriaCli.isChecked():
                var.historico = 0
            else:
                var.historico = 1
            Clientes.cargaTablaClientes(self)
        except Exception as error:
            print("Error en historicoCli: ", error)

    def filtrarProp(self):
        checkeado = var.ui.btnBuscarCli.isChecked()
        var.ui.btnBuscarCli.setChecked(not checkeado)
        Clientes.cargaTablaClientes(self)