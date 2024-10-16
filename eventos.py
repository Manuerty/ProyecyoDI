import os.path
import sys
from datetime import datetime

from PyQt6.QtGui import QIcon

import clientes
import conexion
import time
from PyQt6 import QtWidgets, QtGui
import zipfile
import shutil
import conexionserver
import eventos
import var
import re
import locale


locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')


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
        #listado = conexionserver.ConexionServer.listaProv()
        var.ui.cmbProCli.addItems(listado)

    def cargarMunicipios(self):
        var.ui.cmbMuniCli.clear()
        provincia = var.ui.cmbProCli.currentText()
        listado = conexion.Conexion.listaMuni(provincia)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMuniCli.addItems(listado)

    def validarDNIcli(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCli.setText(str(dni))
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
                    return True
                else:
                    return False
            else:
                return False
        except Exception as error:
            print("error en validar dni ", error)

    def abrirCalendar(pan, btn):
        try:
            var.panel = pan
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == var.ui.panPrincipal.currentIndex() and var.btn == 0:
                var.ui.txtAltaCli.setText(str(data))
            elif var.panel == var.ui.panPrincipal.currentIndex() and var.btn == 1:
                var.ui.txtBajaCli.setText(str(data))
            time.sleep(0.125)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def validarMail(mail):
        mail = mail.lower()
        regex = r'[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,5}'
        if re.match(regex, mail):
            return True
        else:
            return False

    def resizeTablaClientes(self):
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range (header.count()):
                if i==1 or i==2 or i==4 or i == 5:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaClientes.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes", e)

    def crearBackUp(self):
        try:
            fecha = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            copia = str(fecha) + '_backup.zip'
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Guardar Copia de Seguridad", copia, '.zip')
            if var.dlgabrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, "w")
                fichzip.write('bbdd.sqlite', os.path.basename('bbdd.sqlite'), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Copia de Seguridad')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('Copia de Seguridad creada correctamente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()


        except Exception as error:
            print("error en crear backup", error)

    def restaurarBackUp(self):
        try:
            filename = var.dlgabrir.getOpenFileName(None, "Restaurar Copia de Seguridad", "", '*.zip;;All Files(*)')
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowTitle('Copia de Seguridad')
            mbox.setWindowIcon(QIcon('./img/logo.ico'))
            mbox.setText('Copia de Seguridad restaurada correctamente')
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            mbox.exec()
            conexion.Conexion.db_conexion(self)
            eventos.Eventos.cargarProvincias(self)
            clientes.Clientes.cargaTablaClientes(self)
        except Exception as error:
            print("Eroor al restaurar el BackUp", error)