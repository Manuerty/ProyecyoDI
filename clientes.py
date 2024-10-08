from tabnanny import check

from PyQt6 import QtWidgets, QtGui

import conexion
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

    def altaCliente(self):
        try:
            nuevocli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(), var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(),  var.ui.txtMovilCli.text(), var.ui.txtDirCli.text(),  var.ui.cmbProCli.currentText(), var.ui.cmbMuniCli.currentText()]
            conexion.Conexion.altaCliente(nuevocli)

        except Exception as e:
            print("error alta cliente", e)