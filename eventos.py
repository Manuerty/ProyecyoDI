import csv
import json
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
import eventos
import facturas
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
        var.ui.cmbProCli.addItems(listado)

    def cargarMunicipios(self):
        var.ui.cmbMuniCli.clear()
        provincia = var.ui.cmbProCli.currentText()
        listado = conexion.Conexion.listaMuni(provincia)
        var.ui.cmbMuniCli.addItems(listado)

    def cargarProvinciasProp(self):
            var.ui.cmbProvProp.clear()
            listado = conexion.Conexion.listaProv(self)
            var.ui.cmbProvProp.addItems(listado)

    def cargarMunicipiosProp(self):
        var.ui.cmbMuniProp.clear()
        provincia = var.ui.cmbProvProp.currentText()
        listado = conexion.Conexion.listaMuni(provincia)
        var.ui.cmbMuniProp.addItems(listado)

    def cargarProvinciasVen(self):
        var.ui.cmbDelegVen.clear()
        listado = conexion.Conexion.listaProv(self)
        var.ui.cmbDelegVen.addItems(listado)

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

    def validarDNIven(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniVen.setText(str(dni))
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

    def chekTelefono(dni):
        try:
            dni = dni.lower()
            regex = r'^(?:\+34|0034)?[\s.-]?[67]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}$'
            if re.match(regex, dni):
                return True
            else:
                return False
        except Exception as error:
            print("error en checkDNI ", error)

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
            if var.panel == 0 and var.btn == 0:
                var.ui.txtAltaCli.setText(str(data))
            elif var.panel == 0 and var.btn == 1:
                var.ui.txtBajaCli.setText(str(data))
            elif var.panel == 1 and var.btn == 0:
                var.ui.txtFechaAltaProp.setText(str(data))
            elif var.panel == 1 and var.btn == 1:
                var.ui.txtFechaBajaProp.setText(str(data))
            elif var.panel == 2 and var.btn == 0:
                var.ui.txtAltaVen.setText(str(data))
            elif var.panel == 3 and var.btn == 0:
                var.ui.txtFechaFactura.setText(str(data))

            time.sleep(0.125)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def validarMail(mail):
        mail = mail.lower()
        regex = r'[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,5}'
        if re.match(regex, mail) or mail == '':
            return True
        else:
            return False

    def resizeTablaClientes(self):
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if i == 1 or i == 2 or i == 4 or i == 5:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaClientes.horizontalHeaderItem(i)
                if header_item is not None:
                    font = header_item.font()
                    font.setBold(True)
                    header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes", e)

    def resizeTablaPropiedades(self):
        try:
            header = var.ui.tablaProp.horizontalHeader()
            for i in range(header.count()):
                if i == 1 or i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaProp.horizontalHeaderItem(i)
                if header_item is not None:
                    font = header_item.font()
                    font.setBold(True)
                    header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla prop", e)

    def resizeTablaVendedores(self):
        try:
            header = var.ui.tablaVen.horizontalHeader()
            for i in range(header.count()):
                if i == 1 or i == 2 or i == 4 or i == 5:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaVen.horizontalHeaderItem(i)
                if header_item is not None:
                    font = header_item.font()
                    font.setBold(True)
                    header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla vendedores", e)

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

    def limpiarPanel(self):
        try:
            current_index = var.ui.panPrincipal.currentIndex()

            if current_index == 0:
                objetospanelcli = [var.ui.txtDniCli, var.ui.txtAltaCli, var.ui.txtApelCli, var.ui.txtNomCli,
                            var.ui.txtEmailCli, var.ui.txtMovilCli,var.ui.txtDirCli, var.ui.cmbProCli,
                            var.ui.cmbMuniCli, var.ui.txtBajaCli]
                for i, dato in enumerate(objetospanelcli):
                    if i == 7 or i == 8:
                        pass
                    else:
                        dato.setText('')

                eventos.Eventos.cargarProvincias(self)
            elif current_index == 1:
                listado = [var.ui.lblProp, var.ui.txtFechaAltaProp, var.ui.txtFechaBajaProp, var.ui.txtDirProp,
                           var.ui.cmbProvProp, var.ui.cmbMuniProp, var.ui.txtCpProp, var.ui.cmbTipoProp,
                           var.ui.spinNumhabitProp,
                           var.ui.spinNumbanProp, var.ui.txtSuperficieProp, var.ui.txtPrecioVProp,
                           var.ui.txtPrecioAProp,
                           var.ui.textDescriptProp, var.ui.rbtDisponibleProp, var.ui.rbtAlquiladoProp,
                           var.ui.rbtVendidoProp, var.ui.chkIntercambioProp,
                           var.ui.chkAlquilerProp, var.ui.chkVentaProp,
                           var.ui.txtPropietarioProp, var.ui.txtMovilpropietarioProp]

                for i, dato in enumerate(listado):
                    if i not in {4,5,7,8,9,14,15,16,17,18,19}:
                        dato.setText('')
                    if i in {8,9}:
                        dato.setValue(0)
                    if i in {14}:
                        dato.setChecked(True)
                    if i in {15,16}:
                        dato.setChecked(False)
                    if i in {17,18,19}:
                        dato.setChecked(False)

                eventos.Eventos.cargarProvinciasProp(self)
                Eventos.cargarTipoProp()
            elif current_index == 2:
                vendedor = [var.ui.lblVen, var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen,
                            var.ui.txtBajaVen, var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDelegVen]

                for i, dato in enumerate(vendedor):
                    if i != 7:
                        dato.setText("")
                    else:
                        dato.setCurrentIndex(0)

                Eventos.cargarDelegacion()

            elif current_index == 3:
                    ventas = [var.ui.lblNumFactura, var.ui.txtdniclifac, var.ui.txtFechaFactura, var.ui.txtnomeclifac,
                          var.ui.txtapelclifac,
                          var.ui.txtidvenfac, var.ui.txtcodpropfac, var.ui.txttipopropfac, var.ui.txtpreciofac,
                          var.ui.txtmunipropfac,
                          var.ui.txtdirpropfac]
                    for i, dato in enumerate(ventas):
                        if i != 2:
                            dato.setText("")
                        else:
                            dato.setText(datetime.today().strftime('%d/%m/%Y'))
                    facturas.Facturas.cargaTablaVentas()
            else:
                print("panPrincipal es nulo")
        except Exception as e:
            print(f"Se ha producido una excepción: {e}")


    def cargarDelegacion(self):
        var.ui.cmbDelegVen.clear()
        listado = conexion.Conexion().listaProv(self)
        var.ui.cmbDelegVen.addItems(listado)


    def clearCampos(self):
        var.ui.txtDniCli.setText(None)
        var.ui.txtApelCli.setText(None)
        var.ui.txtNomCli.setText(None)
        var.ui.txtMovilCli.setText(None)
        var.ui.txtEmailCli.setText(None)
        var.ui.txtAltaCli.setText(None)
        var.ui.txtDirCli.setText(None)
        var.ui.cmbProCli.setCurrentIndex(0)

    def clearCamposProp(self):
        var.ui.lblProp.setText(None)
        var.ui.txtFechaAltaProp.setText(None)
        var.ui.txtDirProp.setText(None)
        var.ui.cmbProvProp.setCurrentIndex(0)
        var.ui.cmbMuniProp.setCurrentIndex(0)
        var.ui.txtCpProp.setText(None)
        var.ui.cmbTipoProp.setCurrentIndex(0)
        var.ui.spinNumhabitProp.setValue(0)
        var.ui.spinNumbanProp.setValue(0)
        var.ui.txtSuperficieProp.setText(None)
        var.ui.txtPrecioVProp.setText(None)
        var.ui.txtPrecioAProp.setText(None)
        var.ui.textDescriptProp.setText(None)
        var.ui.txtPropietarioProp.setText(None)
        var.ui.txtMovilpropietarioProp.setText(None)
        var.ui.chkAlquilerProp.setChecked(False)
        var.ui.chkIntercambioProp.setChecked(False)
        var.ui.chkVentaProp.setChecked(False)
        var.ui.rbtAlquiladoProp.setChecked(False)
        var.ui.rbtVendidoProp.setChecked(False)

    def abrirTipoProp(self):
        try:
            var.dlggestion.show()
        except Exception as error:
            print("error en abrir tipo propiedad", error)

    def abrirAbout(self):
        try:
            var.dlgabout.show()
        except Exception as error:
            print("error en abrir about", error)

    def cerrarAbout(self):
        try:
            var.dlgabout.close()
        except Exception as error:
            print("error en abrir about", error)


    def cargarTipoProp(self):
        try:
            registro = conexion.Conexion.cargarTipoProp(self)
            var.ui.cmbTipoProp.clear()
            var.ui.cmbTipoProp.addItems(registro)
        except Exception as error:
            print('Error cargarTipoProp: %s ' % str(error))

    @staticmethod
    def crearMensajeSalida(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/icono.svg'))
        mbox.setText(mensaje)
        mbox.setWindowTitle(titulo_ventana)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        return mbox

    @staticmethod
    def crearMensajeInfo(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        return mbox

    @staticmethod
    def crearMensajeError(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        return mbox



    def exportCSVProp(self):
        try:
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_propiedades.csv')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos en CSV", file, '.csv')
            if fichero:
                registros = conexion.Conexion.listadoPropiedadesExport(self)
                with open (fichero, "w", newline='', encoding= 'utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo", "Alta", "Baja", "Direccion", "Provincia", "Municipio", "CP", "Tipo", "Habitaciones",
                    "Banos", "Superficie", "Precio Venta", "Precio Alquiler","Descripción",  "Operación", "Estado", "Propietario", "Movil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError('Exportar CSV', 'No se ha seleccionado ningún fichero')

        except Exception as error:
            print("error en exportar csv propiedades", error)

    def exportJSONProp(self):
        try:
            var.historiaprop = 0
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_propiedades.json')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos en JSON", file, '.json')
            if fichero:
                keys = ['codigo', 'alta', 'baja', 'direccion', 'provincia', 'municipio', 'cp', 'tipo', 'habitaciones',
                        'banos', 'superficie', 'precioventa', 'precioalquiler', 'descripcion', 'operacion', 'estado', 'propietario', 'movil']
                registros = conexion.Conexion.listadoPropiedadesExport(self)
                lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
                with open (fichero, "w", encoding= 'utf-8') as jsonfile:
                    json.dump(lista_propiedades, jsonfile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError('Exportar JSON', 'No se ha seleccionado ningún fichero')
        except Exception as error:
            print("error en exportar json porpiedades" , error)

    def exportCSVClientes(self):
        try:
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_clientes.csv')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos en CSV", file, '.csv')
            if fichero:
                registros = conexion.Conexion.listadoClientesExport(self)
                with open (fichero, "w", newline='', encoding= 'utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["DNI", "Fecha de Alta", "Fecha de Baja", "Apellidos", "Nombre","Email", "Telefono", "Direccion", "Provincia", "Municipio"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError('Exportar CSV', 'No se ha seleccionado ningún fichero')

        except Exception as error:
            print("error en exportar csv clientes", error)


    def exportJSONClientes(self):
        try:
            var.historiacli = 0
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_clientes.json')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos en JSON", file, '.json')
            if fichero:
                keys = ['dni', 'alta', 'baja', 'apellidos', 'nombre', 'email', 'telefono', 'direccion', 'provincia', 'municipio']
                registros = conexion.Conexion.listadoClientesExport(self)
                lista_clientes = [dict(zip(keys, registro)) for registro in registros]
                with open (fichero, "w", encoding= 'utf-8') as jsonfile:
                    json.dump(lista_clientes, jsonfile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError('Exportar JSON', 'No se ha seleccionado ningún fichero')

        except Exception as error:
            print("error en exportar json clientes", error)

    def exportJSONVendedor(self):
        try:
            var.historiacli = 0
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_vendedores.json')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos en JSON", file, '.json')
            if fichero:
                keys = ['id', 'dni', 'nombre y apellidos', 'fecha de alta', 'fecha de baja', 'numero', 'email', 'delegacion']
                registros = conexion.Conexion.listadoVendedoresExport(self)
                lista_vendedores = [dict(zip(keys, registro)) for registro in registros]
                with open (fichero, "w", encoding= 'utf-8') as jsonfile:
                    json.dump(lista_vendedores, jsonfile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError('Exportar JSON', 'No se ha seleccionado ningún fichero')

        except Exception as error:
            print("error en exportar json clientes", error)

    @staticmethod
    def resizeTablaFacturas():
        try:
            header = var.ui.tablaFacturas.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaFacturas.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes ", e)

    @staticmethod
    def resizeTablaVentas():
        try:
            header = var.ui.tablaVentas.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaVentas.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes ", e)
