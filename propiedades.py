import datetime
from xml.sax.handler import property_interning_dict

import conexion
import eventos
import facturas
import var
from PyQt6 import QtWidgets, QtGui, QtCore

class Propiedades():

    def altaTipoPropiedad(self):
        """
        Método que maneja el alta de un nuevo tipo de propiedad en la base de datos.

        Este método obtiene el nombre de un nuevo tipo de propiedad desde un campo de texto, lo valida y lo inserta en la base
        de datos. Si el tipo de propiedad ya existe, se muestra un mensaje de error. Si la inserción es exitosa, se actualiza
        el combo de tipos de propiedad con los nuevos datos.

        :return: None
        :rtype: None
        """
        try:
            # Obtiene el valor del campo de texto donde se introduce el nuevo tipo de propiedad, y lo convierte en título
            tipo = var.dlggestion.ui.txtTipoProp.text().title()

            # Intenta insertar el tipo en la base de datos llamando a la función correspondiente
            registro = conexion.Conexion.altaTipoProp(tipo)

            if registro:
                # Si el registro se inserta correctamente, muestra un mensaje informativo
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Tipo añadido a la BBDD")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

                # Limpiar y actualizar el combo de tipos de propiedad con los nuevos datos
                var.ui.cmbTipoProp.clear()
                var.ui.cmbTipoProp.addItems(registro)

                # Limpia el campo de texto donde se ingresó el nuevo tipo
                var.dlggestion.ui.txtTipoProp.setText('')

            else:
                # Si el tipo de propiedad ya existe en la base de datos, muestra un mensaje de error
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Ya existe ese tipo en la BBDD")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as error:
            # Si ocurre un error en el proceso, se captura y muestra el mensaje de error
            print('Error altaTipoPropiedad: %s ' % str(error))

    def bajaTipoPropiedad(self):
        """
        Método que maneja la baja de un tipo de propiedad en la base de datos.

        Este método obtiene el nombre de un tipo de propiedad desde un campo de texto, lo valida y lo elimina de la base
        de datos. Si el tipo de propiedad se elimina correctamente, se muestra un mensaje de éxito. Si no se puede eliminar,
        se muestra un mensaje de error.

        :return: None
        :rtype: None
        """
        try:
            # Obtiene el valor del campo de texto donde se introduce el tipo de propiedad a eliminar, y lo convierte en título
            tipo = var.dlggestion.ui.txtTipoProp.text().title()

            # Intenta eliminar el tipo de propiedad de la base de datos llamando a la función correspondiente
            if conexion.Conexion.bajaTipoProp(tipo):
                # Si el tipo de propiedad se elimina correctamente, muestra un mensaje de éxito
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Tipo dado de baja")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

                # Limpia el campo de texto donde se ingresó el tipo
                var.dlggestion.ui.txtTipoProp.setText('')

            else:
                # Si no se pudo eliminar el tipo de propiedad, muestra un mensaje de error
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("No se ha podido dar de baja el tipo")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as error:
            # Si ocurre un error durante el proceso, se captura y muestra el mensaje de error
            print('Error bajaTipoPropiedad: %s ' % str(error))

    def altaPropiedad(self):
        """
        Método para gestionar el alta de una propiedad en la base de datos.

        Este método recoge los datos de la propiedad desde la interfaz de usuario, los organiza en un formato adecuado,
        y los envía a la base de datos para ser guardados. Si la propiedad se agrega correctamente, se muestra un mensaje
        de éxito. Si ocurre un error, se muestra un mensaje de fallo.

        :return: None
        :rtype: None
        """
        try:
            # Recoge los datos de la propiedad desde los campos de la interfaz de usuario
            propiedad = [
                var.ui.txtFechaAltaProp.text(),
                var.ui.txtDirProp.text(),
                var.ui.cmbProvProp.currentText(),
                var.ui.cmbMuniProp.currentText(),
                var.ui.cmbTipoProp.currentText(),
                var.ui.spinNumhabitProp.text(),
                var.ui.spinNumbanProp.text(),
                var.ui.txtSuperficieProp.text(),
                var.ui.txtPrecioVProp.text(),
                var.ui.txtPrecioAProp.text(),
                var.ui.txtCpProp.text(),
                var.ui.textDescriptProp.toPlainText()
            ]

            # Recoge los tipos de operación seleccionados (Alquiler, Intercambio, Venta)
            tipoOper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipoOper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipoOper.append(var.ui.chkIntercambioProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipoOper.append(var.ui.chkVentaProp.text())

            # Añade la lista de tipos de operación a los datos de la propiedad
            propiedad.append(tipoOper)

            # Recoge el estado de la propiedad (Alquilado, Vendido, Disponible)
            if var.ui.rbtAlquiladoProp.isChecked():
                propiedad.append(var.ui.rbtAlquiladoProp.text())
            elif var.ui.rbtVendidoProp.isChecked():
                propiedad.append(var.ui.rbtVendidoProp.text())
            elif var.ui.rbtDisponibleProp.isChecked():
                propiedad.append(var.ui.rbtDisponibleProp.text())

            # Recoge los datos del propietario de la propiedad
            propiedad.append(var.ui.txtPropietarioProp.text())
            propiedad.append(var.ui.txtMovilpropietarioProp.text())

            # Llama al método para dar de alta la propiedad en la base de datos
            if conexion.Conexion.altaPropiedad(propiedad):
                # Si la propiedad se añade correctamente, muestra un mensaje de éxito
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Propiedad añadida a la BBDD")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

                # Recarga la tabla de propiedades
                Propiedades.cargaTablaPropiedades(self)
                # Limpia los campos de la interfaz
                eventos.Eventos.clearCamposProp(self)
            else:
                # Si no se puede añadir la propiedad, muestra un mensaje de error
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))
                mbox.setWindowTitle('Aviso')
                mbox.setText("No se ha podido añadir la propiedad a la BBDD")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as error:
            # Si ocurre algún error durante el proceso, se captura y se imprime el error
            print('Error altaPropiedad: %s ' % str(error))

    def cargaTablaPropiedades(self):
        """
        Método para cargar las propiedades en la tabla de la interfaz.

        Este método obtiene un listado de propiedades de la base de datos, paginado en función de las variables de
        control de la interfaz (por ejemplo, página actual y cantidad de elementos por página). Luego, llena la tabla
        de propiedades con los datos obtenidos.

        Si no hay propiedades disponibles, se muestra un mensaje indicando que no hay propiedades de ese tipo. También
        se habilitan o deshabilitan los botones de navegación (siguiente y anterior) según sea necesario.

        :return: None
        :rtype: None
        """
        try:
            # Se limpia la tabla para asegurarse de que no haya filas anteriores
            var.ui.tablaProp.setRowCount(0)

            # Obtiene el listado completo de propiedades desde la base de datos
            listado = conexion.Conexion.listadoPropiedades(self)
            total = len(listado)  # Total de propiedades en el listado

            # Calcula los índices de inicio y fin de la página actual de propiedades
            start_index = var.current_page_prop * var.items_per_page_prop
            end_index = start_index + var.items_per_page_prop

            # Obtiene el sublistado de propiedades según la página actual
            sublistado = listado[start_index:end_index] if listado else []

            # Se establece el número de filas de la tabla en función de las propiedades a mostrar
            var.ui.tablaProp.setRowCount(len(sublistado))

            if not listado:
                # Si no hay propiedades, muestra un mensaje en la tabla
                var.ui.tablaProp.setRowCount(1)
                var.ui.tablaProp.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay propiedades de este tipo"))
                var.ui.tablaProp.item(0, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                # Si hay propiedades, las carga en la tabla
                for index, registro in enumerate(sublistado):
                    var.ui.tablaProp.setRowCount(index + 1)

                    # Asigna los valores de cada propiedad en las celdas correspondientes
                    var.ui.tablaProp.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))  # ID
                    var.ui.tablaProp.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[5])))  # Dirección
                    var.ui.tablaProp.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[7])))  # Superficie
                    var.ui.tablaProp.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[8])))  # Precio Venta
                    var.ui.tablaProp.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[9])))  # Precio Alquiler

                    # Si hay campos vacíos (precio alquiler o precio venta), asigna un valor predeterminado
                    if registro[11] == "":
                        registro[11] = "-"
                    elif registro[12] == "":
                        registro[12] = "-"

                    # Muestra los precios en la tabla (con el símbolo de €)
                    var.ui.tablaProp.setItem(index, 5,
                                             QtWidgets.QTableWidgetItem(str(registro[11]) + "€"))  # Precio Alquiler
                    var.ui.tablaProp.setItem(index, 6,
                                             QtWidgets.QTableWidgetItem(str(registro[12]) + "€"))  # Precio Venta

                    # Asigna el estado de la propiedad
                    var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14])))  # Estado
                    var.ui.tablaProp.setItem(index, 8,
                                             QtWidgets.QTableWidgetItem(str(registro[2])))  # Tipo de Propiedad

                    # Alinea los textos de las celdas para mejor presentación
                    var.ui.tablaProp.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)

                # Habilita o deshabilita los botones de navegación según la página actual
                var.ui.BtnSiguienteProp.setEnabled(end_index < total)
                var.ui.BtnAnteriorProp.setEnabled(var.current_page_prop > 0)

        except Exception as error:
            # Si ocurre algún error durante el proceso, se captura y se imprime el error
            print('Error cargaTablaPropiedades: %s ' % str(error))

    def anteriorPropiedad(self):
        """
        Método para navegar a la página anterior en el listado de propiedades.

        Este método disminuye el contador de la página actual si no estamos en la primera página,
        y luego recarga la tabla de propiedades para mostrar los resultados de la nueva página.

        :return: None
        :rtype: None
        """
        try:
            # Si no estamos en la primera página, disminuimos el número de la página actual
            if var.current_page_prop > 0:
                var.current_page_prop -= 1

            # Recarga la tabla con los datos de la página actualizada
            Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            # Si ocurre un error, se captura y se imprime en la consola
            print("Error en anteriorPropiedad: ", error)

    def siguientePropiedad(self):
        """
        Método para navegar a la siguiente página en el listado de propiedades.

        Este método aumenta el contador de la página actual en 1 y luego recarga la tabla de propiedades
        para mostrar los resultados de la nueva página.

        :return: None
        :rtype: None
        """
        try:
            # Aumenta el número de la página actual en 1 para ir a la siguiente página
            var.current_page_prop += 1

            # Recarga la tabla con los datos de la nueva página
            Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            # Si ocurre un error, se captura y se imprime en la consola
            print("Error en siguientePropiedad: ", error)

    @staticmethod
    def cargaOnePropiedad():
        """
        Método para cargar los detalles de una propiedad seleccionada en la interfaz.

        Este método recupera la información de una propiedad desde la base de datos,
        y luego actualiza los campos correspondientes en la interfaz de usuario.

        :return: None
        :rtype: None
        """
        try:
            # Recupera los datos de la propiedad seleccionada en la tabla
            fila = var.ui.tablaProp.selectedItems()
            datos = [dato.text() for dato in fila]  # Extrae el texto de las celdas seleccionadas

            # Obtiene la información de la propiedad desde la base de datos
            registro = conexion.Conexion.datosOnePropiedad((datos[0]))

            # Lista de elementos de la interfaz que deben ser actualizados
            listado = [
                var.ui.lblProp, var.ui.txtFechaAltaProp, var.ui.txtFechaBajaProp, var.ui.txtDirProp,
                var.ui.cmbProvProp, var.ui.cmbMuniProp, var.ui.txtCpProp, var.ui.cmbTipoProp,
                var.ui.spinNumhabitProp, var.ui.spinNumbanProp, var.ui.txtSuperficieProp,
                var.ui.txtPrecioVProp, var.ui.txtPrecioAProp, var.ui.textDescriptProp, var.ui.rbtDisponibleProp,
                var.ui.rbtAlquiladoProp, var.ui.rbtVendidoProp, var.ui.chkIntercambioProp,
                var.ui.chkAlquilerProp, var.ui.chkVentaProp, var.ui.txtPropietarioProp, var.ui.txtMovilpropietarioProp
            ]

            listadoVentas = []  # Lista para almacenar los tipos de operaciones de venta (intercambio, alquiler, etc.)

            # Recorrer cada campo de la interfaz y actualizar con los valores del registro
            for i in range(len(listado)):
                if i in (4, 5, 7):  # Campos de tipo combo box
                    listado[i].setCurrentText(registro[i])  # Establece el texto seleccionado
                elif i in (8, 9):  # Campos numéricos
                    listado[i].setValue(int(registro[i]))  # Establece el valor numérico
                elif i == 13:  # Campo de descripción
                    listado[i].setPlainText(registro[i])  # Establece el texto de la descripción
                elif i == 14:  # Propiedad disponible
                    listado[i].setChecked(registro[15] == "Disponible")
                elif i == 15:  # Propiedad alquilada
                    listado[i].setChecked(registro[15] == "Alquilado")
                elif i == 16:  # Propiedad vendida
                    listado[i].setChecked(registro[15] == "Vendido")
                elif i in (17, 18, 19):  # Tipo de operaciones (intercambio, alquiler, venta)
                    listado[17].setChecked("Intercambio" in registro[14])
                    listado[18].setChecked("Alquiler" in registro[14])
                    listado[19].setChecked("Venta" in registro[14])
                    if "Venta" in registro[14] and "Venta" not in listadoVentas:
                        listadoVentas.append("Venta")
                elif i == 20:  # Propietario
                    listado[i].setText(registro[16])  # Establece el nombre del propietario
                elif i == 21:  # Teléfono del propietario
                    listado[i].setText(registro[17])  # Establece el teléfono del propietario
                else:
                    listado[i].setText(str(registro[i]))  # Para el resto, convierte a string

            # Se agrega información adicional a la lista de ventas
            listadoVentas.append(registro[0])  # Tipo de propiedad
            listadoVentas.append(registro[6])  # Código postal
            listadoVentas.append(registro[11])  # Precio de venta
            listadoVentas.append(registro[3])  # Dirección
            listadoVentas.append(registro[5])  # Ciudad o municipio

            # Verifica si la propiedad tiene alguna de las condiciones (Disponible, Alquilado, Vendido)
            if "Disponible" in registro and "Disponible" not in listadoVentas:
                listadoVentas.append("Disponible")
            if "Alquilado" in registro and "Alquilado" not in listadoVentas:
                listadoVentas.append("Alquilado")
            if "Vendido" in registro and "Vendido" not in listadoVentas:
                listadoVentas.append("Vendido")

            # Si la propiedad es de tipo "Venta" y está disponible, se carga la información en las facturas
            if listadoVentas[0] == "Venta" and listadoVentas[6] == "Disponible":
                facturas.Facturas.cargarPropiedadVenta(listadoVentas)
        except Exception as e:
            # Si ocurre un error durante la ejecución, se captura y se imprime en la consola
            print("Error cargando UNA propiedad en propiedades.", e)

    @staticmethod
    def modifPropiedad(self):
        """
        Método encargado de modificar los detalles de una propiedad en la base de datos.
        Realiza las siguientes tareas:
        - Recopila la información de los campos de la interfaz de usuario.
        - Valida las fechas y los campos obligatorios.
        - Realiza la modificación en la base de datos.
        - Muestra mensajes de éxito o error dependiendo del resultado.

        :param self: Referencia a la instancia de la clase (para acceder a atributos o métodos de la misma).
        :type self: object
        :return: None
        :rtype: None

        Ejemplo:
            modifPropiedad()
        """
        try:
            # Recopilación de datos de la interfaz de usuario
            propiedad = [
                var.ui.lblProp.text(),  # ID de la propiedad (o nombre)
                var.ui.txtFechaAltaProp.text(),  # Fecha de alta
                var.ui.txtFechaBajaProp.text(),  # Fecha de baja
                var.ui.txtDirProp.text(),  # Dirección
                var.ui.cmbProvProp.currentText(),  # Provincia
                var.ui.cmbMuniProp.currentText(),  # Municipio
                var.ui.cmbTipoProp.currentText(),  # Tipo de propiedad
                var.ui.spinNumhabitProp.text(),  # Número de habitaciones
                var.ui.spinNumbanProp.text(),  # Número de baños
                var.ui.txtSuperficieProp.text(),  # Superficie
                var.ui.txtPrecioVProp.text(),  # Precio de venta
                var.ui.txtPrecioAProp.text(),  # Precio de alquiler
                var.ui.txtCpProp.text(),  # Código postal
                var.ui.textDescriptProp.toPlainText()  # Descripción
            ]

            # Recopilación de los tipos de operación asociados a la propiedad (Alquiler, Venta, Intercambio)
            tipoOper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipoOper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipoOper.append(var.ui.chkVentaProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipoOper.append(var.ui.chkIntercambioProp.text())

            propiedad.append(tipoOper)

            # Recopilación del estado de la propiedad (Disponible, Alquilado, Vendido)
            if var.ui.rbtDisponibleProp.isChecked():
                propiedad.append(var.ui.rbtDisponibleProp.text())
            elif var.ui.rbtAlquiladoProp.isChecked():
                propiedad.append(var.ui.rbtAlquiladoProp.text())
            elif var.ui.rbtVendidoProp.isChecked():
                propiedad.append(var.ui.rbtVendidoProp.text())

            # Recopilación de la información del propietario
            propiedad.append(var.ui.txtPropietarioProp.text())
            propiedad.append(var.ui.txtMovilpropietarioProp.text())

            # Validación de las fechas de alta y baja
            if propiedad[2] != "" and not Propiedades.esFechasValidas(propiedad):
                # Si la fecha de baja es posterior a la de alta, se muestra un error
                mbox = eventos.Eventos.crearMensajeError("Error",
                                                         "La fecha de baja no puede ser posterior a la fecha de alta.")
                mbox.exec()

            # Validación de los campos obligatorios y modificación de la propiedad
            elif Propiedades.checkDatosVaciosModifProp(propiedad) and conexion.Conexion.modifPropiedad(propiedad):
                # Si todos los datos son válidos y la modificación en la base de datos es exitosa
                mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Se ha modificado la propiedad correctamente.")
                mbox.exec()
                Propiedades.cargaTablaPropiedades(self)  # Actualiza la tabla de propiedades

            # Validación de campos vacíos
            elif not Propiedades.checkDatosVaciosModifProp(propiedad):
                mbox = eventos.Eventos.crearMensajeError("Error", "Hay algunos campos obligatorios que están vacíos.")
                mbox.exec()

            else:
                # Si ocurrió un error en la modificación de la propiedad
                mbox = eventos.Eventos.crearMensajeError("Error", "Se ha producido un error al modificar la propiedad")
                mbox.exec()

        except Exception as e:
            # Manejo de excepciones, en caso de que algo falle en el proceso
            print("Error modificando cliente en propiedades.", e)

    @staticmethod
    def checkDatosVaciosModifProp(datosPropiedades):
        """
        Verifica si alguno de los campos de datos de la propiedad está vacío o es None.

        Este método recibe una lista con los datos de la propiedad y verifica si alguno de los campos obligatorios
        está vacío o contiene un valor `None`. Se excluyen algunos campos como la descripción, los precios, el número
        de baños, el número de habitaciones y la fecha de baja, ya que no son parte de la validación de campos obligatorios.

        :param datosPropiedades: Lista que contiene los datos de la propiedad.
        :type datosPropiedades: list
        :return: True si todos los campos están completos, False si algún campo está vacío o es None.
        :rtype: bool

        Ejemplo:
            checkDatosVaciosModifProp(datosPropiedades)
        """
        datos = datosPropiedades[:]  # Se hace una copia de la lista para evitar modificar la original

        # Se eliminan algunos campos que no se necesitan para la validación
        descripcion = datos.pop(13)  # Descripción (No se valida)
        precio_venta = datos.pop(11)  # Precio de venta (No se valida)
        precio_alquiler = datos.pop(10)  # Precio de alquiler (No se valida)
        num_banos = datos.pop(8)  # Número de baños (No se valida)
        num_habitaciones = datos.pop(7)  # Número de habitaciones (No se valida)
        fecha_baja = datos.pop(2)  # Fecha de baja (No se valida)

        # Se recorre la lista de datos y se valida que ninguno sea vacío o None
        for dato in datos:
            if dato == "" or dato is None:
                return False  # Si algún dato es vacío o None, devuelve False

        return True  # Si todos los datos son válidos, devuelve True

    @staticmethod
    def esFechasValidas(datosPropiedades):
        """
        Verifica que la fecha de baja no sea anterior a la fecha de alta.

        Este método compara las fechas de alta y baja de una propiedad, asegurando que la fecha de baja no sea
        anterior a la fecha de alta. Si las fechas no son válidas, el método devuelve False. Si la fecha de alta
        es anterior a la de baja, devuelve True.

        :param datosPropiedades: Lista que contiene los datos de la propiedad.
        :type datosPropiedades: list
        :return: True si la fecha de alta es anterior a la fecha de baja, False si la fecha de baja es anterior a la de alta.
        :rtype: bool

        Ejemplo:
            esFechasValidas(datosPropiedades)
        """
        datos = datosPropiedades[:]  # Se hace una copia de la lista para evitar modificar la original
        alta = datos[1]  # Se obtiene la fecha de alta (índice 1)
        baja = datos[2]  # Se obtiene la fecha de baja (índice 2)

        # Convertir las fechas a objetos datetime para compararlas
        fecha_alta = datetime.datetime.strptime(alta, "%d/%m/%Y")
        fecha_baja = datetime.datetime.strptime(baja, "%d/%m/%Y")

        # Comparar las fechas
        return fecha_alta < fecha_baja  # Devuelve True si la fecha de alta es anterior a la de baja

    @staticmethod
    def bajaPropiedad(self):
        """
        Da de baja una propiedad, cambiando su estado a 'Vendido' o 'Alquilado' según corresponda.

        Este método actualiza el estado de una propiedad en la base de datos a 'Vendido', 'Alquilado' o 'Disponible',
        según los campos seleccionados en la interfaz de usuario. Además, verifica que las fechas sean válidas y que
        se haya ingresado una fecha de baja. Si la operación es exitosa, se muestra un mensaje de éxito, de lo contrario,
        se muestra un mensaje de error.

        :param self: Referencia a la instancia de la clase (para acceder a atributos o métodos de la misma).
        :type self: object
        :return: None
        :rtype: None

        Ejemplo:
            bajaPropiedad()
        """
        propiedad = [var.ui.lblProp.text(), var.ui.txtFechaAltaProp.text(), var.ui.txtFechaBajaProp.text()]

        # Determinar el estado de la propiedad (Vendido, Alquilado, Intercambio)
        if var.ui.chkAlquilerProp.isChecked():
            var.ui.rbtAlquiladoProp.setChecked(True)
        elif var.ui.chkVentaProp.isChecked():
            var.ui.rbtVendidoProp.setChecked(True)
        elif var.ui.chkIntercambioProp.isChecked() and var.ui.txtPrecioAProp.text() == "":
            var.ui.rbtVendidoProp.setChecked(True)
        elif var.ui.chkIntercambioProp.isChecked() and var.ui.txtPrecioVProp.text() == "":
            var.ui.rbtAlquiladoProp.setChecked(True)

        # Determinar el estado final de la propiedad según los radio buttons
        if var.ui.rbtDisponibleProp.isChecked():
            propiedad.append(var.ui.rbtDisponibleProp.text())
        elif var.ui.rbtAlquiladoProp.isChecked():
            propiedad.append(var.ui.rbtAlquiladoProp.text())
        elif var.ui.rbtVendidoProp.isChecked():
            propiedad.append(var.ui.rbtVendidoProp.text())

        # Validación de la fecha de baja y la actualización en la base de datos
        if Propiedades.esFechasValidas(propiedad) and conexion.Conexion.bajaProp(propiedad):
            mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Se ha dado de baja la propiedad.")
            mbox.exec()
            Propiedades.cargaTablaPropiedades(self)  # Actualiza la tabla de propiedades
        elif propiedad[2] == "" or propiedad[2] is None:
            mbox = eventos.Eventos.crearMensajeError("Error",
                                                     "Es necesario elegir una fecha para dar de baja la propiedad.")
            mbox.exec()
        elif not Propiedades.esFechasValidas(propiedad):
            mbox = eventos.Eventos.crearMensajeError("Error",
                                                     "La fecha de baja no puede ser anterior a la fecha de alta.")
            mbox.exec()
        else:
            mbox = eventos.Eventos.crearMensajeError("Error", "Se ha producido un error al dar de baja la propiedad.")
            mbox.exec()

    def manageChkBox(self):
        """
        Gestiona el estado de los checkboxes relacionados con las opciones de alquiler, venta e intercambio
        de una propiedad, según los valores ingresados en los campos de precios.

        Este método desactiva los checkboxes de alquiler y venta si los precios correspondientes son vacíos.
        También marca automáticamente la opción de 'Intercambio' si no se han ingresado precios de alquiler ni de venta.

        :param self: Referencia a la instancia de la clase (para acceder a atributos o métodos de la misma).
        :type self: object
        :return: None
        :rtype: None

        Ejemplo:
            manageChkBox()
        """
        var.ui.chkAlquilerProp.setEnabled(False)  # Desactiva el checkbox de alquiler
        var.ui.chkVentaProp.setEnabled(False)  # Desactiva el checkbox de venta

        # Verifica si el precio de alquiler está vacío y actualiza el checkbox de alquiler en consecuencia
        if var.ui.txtPrecioAProp.text() == "":
            var.ui.chkAlquilerProp.setChecked(False)  # Si el precio de alquiler está vacío, desmarca el checkbox
        else:
            var.ui.chkAlquilerProp.setChecked(True)  # Si hay un precio de alquiler, marca el checkbox

        # Verifica si el precio de venta está vacío y actualiza el checkbox de venta en consecuencia
        if var.ui.txtPrecioVProp.text() == "":
            var.ui.chkVentaProp.setChecked(False)  # Si el precio de venta está vacío, desmarca el checkbox
        else:
            var.ui.chkVentaProp.setChecked(True)  # Si hay un precio de venta, marca el checkbox

        # Si tanto el precio de alquiler como el de venta están vacíos, marca el checkbox de intercambio
        if var.ui.txtPrecioAProp.text() == "" and var.ui.txtPrecioVProp.text() == "":
            var.ui.chkIntercambioProp.setChecked(True)  # Marca el checkbox de intercambio

    def manageRadioButtons(self):
        """
        Gestiona el estado y la selección de los botones de radio relacionados con el estado de la propiedad
        (Disponible, Alquilado, Vendido), basándose en la fecha de baja de la propiedad.

        Este método habilita y selecciona el botón correspondiente (Disponible, Alquilado o Vendido) según
        si se ha ingresado una fecha de baja. Si la fecha de baja está vacía, la propiedad se marca como 'Disponible'
        y los botones para 'Alquilado' y 'Vendido' se desactivan. Si la fecha de baja no está vacía, los botones
        de estado se activan.

        :param self: Referencia a la instancia de la clase (para acceder a atributos o métodos de la misma).
        :type self: object
        :return: None
        :rtype: None

        Ejemplo:
            manageRadioButtons()
        """
        if var.ui.txtFechaBajaProp.text() == "":
            # Si la fecha de baja está vacía, habilita y selecciona el estado 'Disponible'
            var.ui.rbtDisponibleProp.setEnabled(True)
            var.ui.rbtDisponibleProp.setChecked(True)
            var.ui.rbtAlquiladoProp.setChecked(False)
            var.ui.rbtVendidoProp.setChecked(False)

            # Desactiva los botones de 'Alquilado' y 'Vendido'
            var.ui.rbtAlquiladoProp.setEnabled(False)
            var.ui.rbtVendidoProp.setEnabled(False)
        else:
            # Si la fecha de baja no está vacía, desactiva 'Disponible' y habilita los otros botones
            var.ui.rbtDisponibleProp.setChecked(False)
            var.ui.rbtDisponibleProp.setEnabled(False)
            var.ui.rbtAlquiladoProp.setChecked(True)
            var.ui.rbtAlquiladoProp.setEnabled(True)
            var.ui.rbtVendidoProp.setEnabled(True)

    def filtrarProp(self):
        """
        Filtra las propiedades según el estado del botón de búsqueda de tipo de propiedad.

        Este método alterna el estado de selección del botón `btnBuscarTipoProp` y luego recarga la tabla
        de propiedades para aplicar el filtro correspondiente.

        :param self: Referencia a la instancia de la clase (para acceder a atributos o métodos de la misma).
        :type self: object
        :return: None
        :rtype: None

        Ejemplo:
            filtrarProp()
        """
        checkeado = var.ui.btnBuscarTipoProp.isChecked()  # Verifica si el botón de búsqueda está seleccionado
        var.ui.btnBuscarTipoProp.setChecked(
            not checkeado)  # Alterna el estado del botón (si está marcado, lo desmarca, y viceversa)
        Propiedades.cargaTablaPropiedades(self)  # Recarga la tabla de propiedades para aplicar el filtro




