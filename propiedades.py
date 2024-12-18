import datetime
from xml.sax.handler import property_interning_dict

import conexion
import eventos
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
            if conexion.Conexion.altaPropiedad(propiedad):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Propiedad añadida a la BBDD")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Propiedades.cargaTablaPropiedades(self)
                eventos.Eventos.clearCamposProp(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("No se ha podido añadir la propiedad a la BBDD")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print('Error altaPropiedad: %s ' % str(error))

    def cargaTablaPropiedades(self):
        try:
            var.ui.tablaProp.setRowCount(0)
            listado = conexion.Conexion.listadoPropiedades(self)
            total = len(listado)
            start_index = var.current_page_prop * var.items_per_page_prop
            end_index = start_index + var.items_per_page_prop
            sublistado = listado[start_index:end_index] if listado else []
            var.ui.tablaProp.setRowCount(len(sublistado))
            if not listado:
                var.ui.tablaProp.setRowCount(1)
                var.ui.tablaProp.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay propiedades de este tipo"))
                var.ui.tablaProp.item(0 , 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                for index, registro in enumerate(sublistado):
                    var.ui.tablaProp.setRowCount(index + 1)
                    var.ui.tablaProp.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                    var.ui.tablaProp.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[5])))
                    var.ui.tablaProp.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[7])))
                    var.ui.tablaProp.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[8])))
                    var.ui.tablaProp.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[9])))
                    if registro[11] == "":
                        registro[11] = "-"
                    elif registro[12] == "":
                        registro[12] = "-"
                    var.ui.tablaProp.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[11]) + "€"))
                    var.ui.tablaProp.setItem(index, 6, QtWidgets.QTableWidgetItem(str(registro[12]) + "€"))
                    var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14])))
                    var.ui.tablaProp.setItem(index, 8, QtWidgets.QTableWidgetItem(str(registro[2])))
                    var.ui.tablaProp.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.BtnSiguienteProp.setEnabled(end_index < total)
                var.ui.BtnAnteriorProp.setEnabled(var.current_page_prop > 0)
        except Exception as error:
            print('Error cargaTablaPropiedades: %s ' % str(error))


    def anteriorPropiedad(self):
        try:
            if var.current_page_prop > 0:
                var.current_page_prop -= 1
            Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            print("Error en anteriorPropiedad: ", error)

    def siguientePropiedad(self):
        try:
            var.current_page_prop += 1
            Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            print("Error en siguientePropiedad: ", error)

    @staticmethod
    def cargaOnePropiedad():
        try:
            fila = var.ui.tablaProp.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad((datos[0]))
            listado = [var.ui.lblProp, var.ui.txtFechaAltaProp, var.ui.txtFechaBajaProp, var.ui.txtDirProp,
                       var.ui.cmbProvProp, var.ui.cmbMuniProp, var.ui.txtCpProp, var.ui.cmbTipoProp,
                       var.ui.spinNumhabitProp,
                       var.ui.spinNumbanProp, var.ui.txtSuperficieProp, var.ui.txtPrecioVProp, var.ui.txtPrecioAProp,
                       var.ui.textDescriptProp,var.ui.rbtDisponibleProp,  var.ui.rbtAlquiladoProp,
                       var.ui.rbtVendidoProp, var.ui.chkIntercambioProp,
                       var.ui.chkAlquilerProp,  var.ui.chkVentaProp,
                       var.ui.txtPropietarioProp, var.ui.txtMovilpropietarioProp]
            for i in range(len(listado)):
                if i in (4, 5, 7):
                    listado[i].setCurrentText(registro[i])
                elif i in (8, 9):
                    listado[i].setValue(int(registro[i]))
                elif i == 13:
                    listado[i].setPlainText(registro[i])
                elif i == 14:
                    listado[i].setChecked(registro[15] == "Disponible")
                elif i == 15:
                    listado[i].setChecked(registro[15] == "Alquilado")
                elif i == 16:
                    listado[i].setChecked(registro[15] == "Vendido")
                elif i in (17, 18, 19):
                    listado[17].setChecked("Intercambio" in registro[14])
                    listado[18].setChecked("Alquiler" in registro[14])
                    listado[19].setChecked("Venta" in registro[14])
                elif i == 20:
                    listado[i].setText(registro[16])
                elif i == 21:
                    listado[i].setText(registro[17])
                else:
                    listado[i].setText(str(registro[i]))  # Convert to string

        except Exception as e:
            print("Error cargando UNA propiedad en propiedades.", e)



    @staticmethod
    def modifPropiedad(self):
        try:
            propiedad = [var.ui.lblProp.text(), var.ui.txtFechaAltaProp.text(),  var.ui.txtFechaBajaProp.text(),
                         var.ui.txtDirProp.text(), var.ui.cmbProvProp.currentText(),
                         var.ui.cmbMuniProp.currentText(), var.ui.cmbTipoProp.currentText(),
                         var.ui.spinNumhabitProp.text(), var.ui.spinNumbanProp.text(), var.ui.txtSuperficieProp.text(),
                         var.ui.txtPrecioVProp.text(), var.ui.txtPrecioAProp.text(), var.ui.txtCpProp.text(),
                         var.ui.textDescriptProp.toPlainText()]
            tipoOper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipoOper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipoOper.append(var.ui.chkVentaProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipoOper.append(var.ui.chkIntercambioProp.text())
            propiedad.append(tipoOper)
            if var.ui.rbtDisponibleProp.isChecked():
                propiedad.append(var.ui.rbtDisponibleProp.text())
            elif var.ui.rbtAlquiladoProp.isChecked():
                propiedad.append(var.ui.rbtAlquiladoProp.text())
            elif var.ui.rbtVendidoProp.isChecked():
                propiedad.append(var.ui.rbtVendidoProp.text())

            propiedad.append(var.ui.txtPropietarioProp.text())
            propiedad.append(var.ui.txtMovilpropietarioProp.text())

            if propiedad[2] != "" and not Propiedades.esFechasValidas(propiedad):
                mbox = eventos.Eventos.crearMensajeError("Error",
                                                         "La fecha de baja no puede ser posterior a la fecha de alta.")
                mbox.exec()
            elif Propiedades.checkDatosVaciosModifProp(propiedad) and conexion.Conexion.modifPropiedad(propiedad):
                mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Se ha modificado la propiedad correctamente.")
                mbox.exec()
                Propiedades.cargaTablaPropiedades(self)
            elif not Propiedades.checkDatosVaciosModifProp(propiedad):
                mbox = eventos.Eventos.crearMensajeError("Error", "Hay algunos campos obligatorios que están vacíos.")
                mbox.exec()
            else:
                mbox = eventos.Eventos.crearMensajeError("Error", "Se ha producido un error al modificar la propiedad")
                mbox.exec()

        except Exception as e:
            print("Error modificando cliente en propiedades.", e)


    @staticmethod
    def checkDatosVaciosModifProp(datosPropiedades):
        datos = datosPropiedades[:]
        descripcion = datos.pop(13)
        precio_venta = datos.pop(11)
        precio_alquiler = datos.pop(10)
        num_banos = datos.pop(8)
        num_habitaciones = datos.pop(7)
        fecha_baja = datos.pop(2)

        for dato in datos:
            if dato == "" or dato is None:
                return False
        return True


    @staticmethod
    def esFechasValidas(datosPropiedades):
        datos = datosPropiedades[:]
        alta = datos[1]
        baja = datos[2]

        fecha_alta = datetime.datetime.strptime(alta, "%d/%m/%Y")
        fecha_baja = datetime.datetime.strptime(baja, "%d/%m/%Y")

        return fecha_alta < fecha_baja

    @staticmethod
    def bajaPropiedad(self):
        propiedad = [var.ui.lblProp.text(), var.ui.txtFechaAltaProp.text(), var.ui.txtFechaBajaProp.text()]

        if var.ui.chkAlquilerProp.isChecked():
            var.ui.rbtAlquiladoProp.setChecked(True)
        elif var.ui.chkVentaProp.isChecked():
            var.ui.rbtVendidoProp.setChecked(True)
        elif var.ui.chkIntercambioProp.isChecked() and var.ui.txtPrecioAProp.text() == "":
            var.ui.rbtVendidoProp.setChecked(True)
        elif var.ui.chkIntercambioProp.isChecked() and var.ui.txtPrecioVProp.text() == "":
            var.ui.rbtAlquiladoProp.setChecked(True)

        if var.ui.rbtDisponibleProp.isChecked():
            propiedad.append(var.ui.rbtDisponibleProp.text())
        elif var.ui.rbtAlquiladoProp.isChecked():
            propiedad.append(var.ui.rbtAlquiladoProp.text())
        elif var.ui.rbtVendidoProp.isChecked():
            propiedad.append(var.ui.rbtVendidoProp.text())
        if Propiedades.esFechasValidas(propiedad) and conexion.Conexion.bajaProp(propiedad):
            mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Se ha dado de baja la propiedad.")
            mbox.exec()
            Propiedades.cargaTablaPropiedades(self)
        elif propiedad[2] == "" or propiedad[2] is None:
            mbox = eventos.Eventos.crearMensajeError("Error", "Es necesario elegir una fecha para dar de baja la propiedad.")
            mbox.exec()
        elif not Propiedades.esFechasValidas(propiedad):
            mbox = eventos.Eventos.crearMensajeError("Error", "La fecha de baja no puede ser anterior a la fecha de alta.")
            mbox.exec()
        else:
            mbox = eventos.Eventos.crearMensajeError("Error", "Se ha producido un error al dar de baja la propiedad.")
            mbox.exec()


    def manageChkBox(self):
        var.ui.chkAlquilerProp.setEnabled(False)
        var.ui.chkVentaProp.setEnabled(False)
        if var.ui.txtPrecioAProp.text() == "":
            var.ui.chkAlquilerProp.setChecked(False)
        else:
            var.ui.chkAlquilerProp.setChecked(True)

        if var.ui.txtPrecioVProp.text() == "":
            var.ui.chkVentaProp.setChecked(False)
        else:
            var.ui.chkVentaProp.setChecked(True)

        if var.ui.txtPrecioAProp.text() == "" and var.ui.txtPrecioVProp.text() == "":
            var.ui.chkIntercambioProp.setChecked(True)

    def manageRadioButtons(self):
        if var.ui.txtFechaBajaProp.text() == "":
            var.ui.rbtDisponibleProp.setEnabled(True)
            var.ui.rbtDisponibleProp.setChecked(True)
            var.ui.rbtAlquiladoProp.setChecked(False)
            var.ui.rbtVendidoProp.setChecked(False)
            var.ui.rbtAlquiladoProp.setEnabled(False)
            var.ui.rbtVendidoProp.setEnabled(False)
        else:
            var.ui.rbtDisponibleProp.setChecked(False)
            var.ui.rbtDisponibleProp.setEnabled(False)
            var.ui.rbtAlquiladoProp.setChecked(True)
            var.ui.rbtAlquiladoProp.setEnabled(True)
            var.ui.rbtVendidoProp.setEnabled(True)

    def filtrarProp(self):
        checkeado = var.ui.btnBuscarTipoProp.isChecked()
        var.ui.btnBuscarTipoProp.setChecked(not checkeado)
        Propiedades.cargaTablaPropiedades(self)



