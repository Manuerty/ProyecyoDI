from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QIcon


import conexion
import var
import eventos
import vendedor


class Vendedor:
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniVen.setText(str(dni))
            check = eventos.Eventos.validarDNIven(dni)
            if check:
                var.ui.txtDniVen.setStyleSheet('background-color: rgb(255,255,220)')
            else:
                var.ui.txtDniVen.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniVen.setText(None)
                var.ui.txtDniVen.setFocus()
        except Exception as error:
            print("error en validar dni ", error)


    def checkEmail(mail):
        try:
            mail = str(var.ui.txtEmailVen.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailVen.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailVen.setText(mail.lower())

            else:
                var.ui.txtEmailVen.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailVen.setText(None)
                var.ui.txtEmailVen.setText("correo no válido")
                var.ui.txtEmailVen.setFocus()

        except Exception as error:
            print("error check Vendedor", error)


    def checktelefono(tlf):
        try:
            tlf = str(var.ui.txtMovilVen.text())
            if eventos.Eventos.chekTelefono(tlf):
                var.ui.txtMovilVen.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtMovilVen.setText(tlf)

            else:
                var.ui.txtMovilVen.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilVen.setText(None)
                var.ui.txtMovilVen.setText("telefono no válido")
                var.ui.txtMovilVen.setFocus()

        except Exception as error:
            print("error check Vendedor", error)


    def altaVendedor(self):
        try:
            nuevoVendedor = [var.ui.txtDniVen.text(), var.ui.txtNomVen.text(), var.ui.txtMovilVen.text(),
                             var.ui.txtEmailVen.text(), var.ui.cmbDelegVen.currentText(), var.ui.txtAltaVen.text()]
            camposObligatorios = [var.ui.txtDniVen.text(), var.ui.txtNomVen.text(),  var.ui.txtMovilVen.text(),
                                  var.ui.cmbDelegVen.currentText()]
            checkearDNI = var.ui.txtDniVen.text()

            for i in range(len(camposObligatorios)):
                if camposObligatorios[i] == "":
                    QtWidgets.QMessageBox.critical(None, 'Error', "Faltan campos por cubrir")
                    return
                else:
                    pass
            if not conexion.Conexion.checkDNIinDb(checkearDNI):
                if not conexion.Conexion.altaVendedor(nuevoVendedor):
                    QtWidgets.QMessageBox.critical(None, 'Error', "Ha ocurrido un error")

                else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                        mbox.setWindowTitle('Aviso')
                        mbox.setText("Vendedor grabado en la base de datos")
                        mbox.setStandardButtons(
                            QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()
                        Vendedor.cargarTablaVendedores(self)
                        # eventos.Eventos.clearCampos(self)
            else :
                QtWidgets.QMessageBox.critical(None, 'Error', "DNI duplicado")
        except Exception as e:
            print("error alta vendedor clase vendedor",e)


    def cargarTablaVendedores(self):
        try:
            var.ui.tablaVen.setRowCount(0)
            listado= conexion.Conexion.listadoVendedores(self)
            total = len(listado)
            start_index = var.current_page_cli * var.items_per_page_cli
            end_index = start_index + var.items_per_page_cli
            sublistado = listado[start_index:end_index] if listado else []
            var.ui.tablaVen.setRowCount(len(sublistado))

            if not listado:
                var.ui.tablaVen.setRowCount(1)
                var.ui.tablaVen.setItem(0, 2, QtWidgets.QTableWidgetItem("No existen Vendedors con ese DNI"))
                var.ui.tablaVen.item(0 , 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                for index, registro in enumerate(sublistado):
                    var.ui.tablaVen.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                    var.ui.tablaVen.setItem(index, 1, QtWidgets.QTableWidgetItem((registro[1])))
                    var.ui.tablaVen.setItem(index, 2, QtWidgets.QTableWidgetItem((registro[2])))
                    var.ui.tablaVen.setItem(index, 3, QtWidgets.QTableWidgetItem((registro[5])))
                    var.ui.tablaVen.setItem(index, 4, QtWidgets.QTableWidgetItem((registro[6])))
                    var.ui.tablaVen.setItem(index, 5, QtWidgets.QTableWidgetItem((registro[7])))
                    var.ui.tablaVen.setItem(index, 6, QtWidgets.QTableWidgetItem((registro[3])))
                    var.ui.tablaVen.setItem(index, 7, QtWidgets.QTableWidgetItem((registro[4])))

                    var.ui.tablaVen.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaVen.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaVen.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaVen.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaVen.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaVen.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaVen.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaVen.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        except Exception as error:
            print("Error al cargar tabla Vendedors", error)

    @staticmethod
    def cargarOneVendedor():
            try:
                fila = var.ui.tablaVen.selectedItems()
                datos = [dato.text() for dato in fila]
                registro = conexion.Conexion.datosOneVendedor(datos[0])
                listado = [var.ui.lblVen, var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen, var.ui.txtBajaVen,
                           var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDelegVen]
                for i in range(len(listado)):
                    if i == 7:
                        listado[i].setCurrentText(registro[i])
                        break
                    if i == 0:
                        listado[i].setText(str(registro[i]))  # Convert to string
                    else:
                        listado[i].setText(registro[i])
                return registro
            except Exception as error:
                print("Error al cargar one vendedor", error)

    def  bajaVendedor(self):
        try:
            datos = [var.ui.txtBajaVen.text(), var.ui.lblVen.text()]
            print(datos)
            if conexion.Conexion.checkDNIinDb(datos[1]):
                if conexion.Conexion.bajaVendedor(datos):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Vendedor borrado')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    vendedor.Vendedor.cargarTablaVendedores(self)
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
                mbox.setText('El Vendedor no existe en la base de datos')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print("Error en bajaVendedor: ", error)

    def modifVendedor(self):
            try:
                modifVend = [var.ui.lblVen.text(), var.ui.txtDniVen.text(), var.ui.txtNomVen.text(), var.ui.txtMovilVen.text(),
                             var.ui.txtEmailVen.text(), var.ui.cmbDelegVen.currentText(), var.ui.txtAltaVen.text()]
                if conexion.Conexion.checkVendedorinDb(modifVend[0]):
                    if conexion.Conexion.modifVend(modifVend):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setWindowTitle('Aviso')
                        mbox.setWindowIcon(QIcon('./img/logo.ico'))
                        mbox.setText('Datos del vendedor modificados')
                        mbox.setStandardButtons(
                            QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()
                        vendedor.Vendedor.cargarTablaVendedores(self)
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        mbox.setWindowTitle('Aviso')
                        mbox.setWindowIcon(QIcon('./img/logo.ico'))
                        mbox.setText('Error al modificar los datos del vendedor')
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
                    mbox.setText('El vendedor no existe en la base de datos')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
            except Exception as error:
                print("Error en modifVend: ", error)