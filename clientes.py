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
        """
        :param dni: Es el DNI del cliente que se desea validar.
        :type dni: String
        :return: None
        :rtype: None

        Este método se encarga de validar si el DNI introducido es válido, mediante un
        proceso de verificación que utiliza un evento de validación preexistente.
        Si el DNI es válido, se resalta el campo de texto correspondiente con un color de fondo
        adecuado. Si no es válido, se cambia el color de fondo a rojo y se limpia el campo de texto.

        Utiliza el método `validarDNIcli` de la clase `Eventos` para realizar la validación del DNI.

        Ejemplo:
            checkDNI("12345678Z")
        """
        try:
            # Convertimos el DNI a mayúsculas y lo asignamos al campo de texto
            dni = str(dni).upper()
            var.ui.txtDniCli.setText(str(dni))

            # Validamos el DNI con un evento específico
            check = eventos.Eventos.validarDNIcli(dni)

            # Si el DNI es válido, se cambia el color de fondo del campo de texto a amarillo
            if check:
                var.ui.txtDniCli.setStyleSheet('background-color: rgb(255,255,220)')
            else:
                # Si el DNI no es válido, se cambia el color de fondo a rosa y se limpia el campo de texto
                var.ui.txtDniCli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniCli.setText(None)
                var.ui.txtDniCli.setFocus()
        except Exception as error:
            # Si ocurre algún error durante la ejecución, lo capturamos y mostramos el mensaje
            print("error en validar dni ", error)

    def checkEmail(mail):
        """
        Método que valida la dirección de correo electrónico ingresada por el usuario.

        :param mail: Correo electrónico a verificar.
        :type mail: str
        :return: None
        :rtype: None

        Este método valida la dirección de correo electrónico utilizando un validador externo,
        y actualiza la interfaz de usuario dependiendo de si la dirección es válida o no. Si el correo
        es válido, se cambia el fondo del campo de texto a blanco y se establece el texto en minúsculas.
        Si el correo no es válido, se cambia el fondo del campo a color rosa, el texto se pone en cursiva,
        y se muestra un mensaje de error.
        """
        try:
            mail = str(var.ui.txtEmailCli.text())  # Obtiene el correo del campo de texto en la interfaz
            if eventos.Eventos.validarMail(mail):  # Valida el correo con un validador externo
                # Si el correo es válido, cambia el color de fondo del campo de texto y convierte el correo a minúsculas
                var.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailCli.setText(mail.lower())

            else:
                # Si el correo no es válido, cambia el fondo a rosa, el texto a cursiva y muestra un mensaje de error
                var.ui.txtEmailCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailCli.setText(None)  # Limpia el campo de texto
                var.ui.txtEmailCli.setText("correo no válido")  # Muestra el mensaje de error
                var.ui.txtEmailCli.setFocus()  # Pone el foco nuevamente en el campo de texto

        except Exception as error:
            print("error check cliente", error)  # En caso de error, lo imprime en la consola

    def checktelefono(tlf):
        """
        Método que valida el número de teléfono ingresado por el usuario.

        :param tlf: Número de teléfono a verificar.
        :type tlf: str
        :return: None
        :rtype: None

        Este método valida el número de teléfono utilizando un validador externo,
        y actualiza la interfaz de usuario dependiendo de si el número es válido o no. Si el número
        es válido, se cambia el fondo del campo de texto a blanco y se muestra el número ingresado.
        Si el número no es válido, se cambia el fondo del campo a color rosa, el texto se pone en cursiva,
        y se muestra un mensaje de error.
        """
        try:
            tlf = str(var.ui.txtMovilCli.text())  # Obtiene el teléfono del campo de texto en la interfaz
            if eventos.Eventos.chekTelefono(tlf):  # Valida el número de teléfono con un validador externo
                # Si el teléfono es válido, cambia el color de fondo del campo de texto
                var.ui.txtMovilCli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtMovilCli.setText(tlf)  # Muestra el número de teléfono ingresado

            else:
                # Si el teléfono no es válido, cambia el fondo a rosa, el texto a cursiva y muestra un mensaje de error
                var.ui.txtMovilCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilCli.setText(None)  # Limpia el campo de texto
                var.ui.txtMovilCli.setText("telefono no válido")  # Muestra el mensaje de error
                var.ui.txtMovilCli.setFocus()  # Pone el foco nuevamente en el campo de texto

        except Exception as error:
            print("error check cliente", error)  # En caso de error, lo imprime en la consola

    def altaCliente(self):
        """
        Método que inserta los datos de un nuevo cliente en la base de datos.

        Este método recoge los datos del cliente desde la interfaz de usuario, valida que todos los campos obligatorios
        estén llenos y luego intenta insertar los datos en la base de datos. Si la inserción es exitosa, se muestra
        un mensaje informativo al usuario y se actualiza la tabla de clientes. Si hay algún error, se muestra un
        mensaje de error.

        :return: None
        :rtype: None
        """
        try:
            # Recoge los datos del cliente desde la interfaz de usuario y los almacena en una lista
            nuevoCli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(),
                        var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.txtDirCli.text(), var.ui.cmbProCli.currentText(),
                        var.ui.cmbMuniCli.currentText()]

            # Lista de campos obligatorios para la inserción
            camposObligatorios = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtApelCli.text(),
                                  var.ui.txtNomCli.text(),
                                  var.ui.txtMovilCli.text(), var.ui.txtDirCli.text(), var.ui.cmbProCli.currentText(),
                                  var.ui.cmbMuniCli.currentText()]

            # Verifica que todos los campos obligatorios están completos
            for i in range(len(camposObligatorios)):
                if camposObligatorios[i] == "":  # Si algún campo está vacío, muestra un mensaje de error
                    QtWidgets.QMessageBox.critical(None, 'Error', "Faltan campos por cubrir")
                    return
                else:
                    pass  # Si el campo está completo, continúa

            # Llama al método para insertar el nuevo cliente en la base de datos
            if not conexion.Conexion.altaCliente(nuevoCli):  # Si ocurre un error al insertar los datos
                QtWidgets.QMessageBox.critical(None, 'Error', "Ha ocurrido un error")  # Muestra un mensaje de error
            else:
                # Si la inserción es exitosa, muestra un mensaje de éxito
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/icono.svg"))  # Establece el icono de la ventana
                mbox.setWindowTitle('Aviso')
                mbox.setText("Cliente grabado en la base de datos")  # Mensaje informativo
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)  # Establece el botón OK
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()  # Ejecuta la ventana de mensaje

                # Actualiza la tabla de clientes y limpia los campos del formulario
                Clientes.cargaTablaClientes(self)
                eventos.Eventos.clearCampos(self)

        except Exception as e:
            print("error alta cliente", e)  # Si ocurre una excepción, imprime el error

    def cargaTablaClientes(self):
        """
        Método que carga y muestra la lista de clientes en una tabla.

        Este método obtiene los datos de los clientes desde la base de datos y los muestra en una tabla
        en la interfaz de usuario. Los resultados se dividen en páginas, mostrando solo una cantidad
        específica de registros por página. Si no hay clientes o si no se encuentran registros con el
        DNI buscado, muestra un mensaje en la tabla.

        :return: None
        :rtype: None
        """
        try:
            # Limpia la tabla antes de cargar nuevos datos
            var.ui.tablaClientes.setRowCount(0)

            # Obtiene la lista de clientes desde la base de datos
            listado = conexion.Conexion.listadoClientes(self)
            total = len(listado)  # Total de clientes en la base de datos

            # Calcula el índice de inicio y fin para paginación
            start_index = var.current_page_cli * var.items_per_page_cli
            end_index = start_index + var.items_per_page_cli

            # Selecciona un subconjunto de clientes para la página actual
            sublistado = listado[start_index:end_index] if listado else []

            # Establece el número de filas en la tabla según el subconjunto de clientes
            var.ui.tablaClientes.setRowCount(len(sublistado))

            # Si no se encontraron clientes, muestra un mensaje en la tabla
            if not listado:
                var.ui.tablaClientes.setRowCount(1)
                var.ui.tablaClientes.setItem(0, 2, QtWidgets.QTableWidgetItem("No existen Clientes con ese DNI"))
                var.ui.tablaClientes.item(0, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            else:
                # Si hay clientes, los agrega a la tabla
                for index, registro in enumerate(sublistado):
                    var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem((registro[0])))  # DNI
                    var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem((registro[3])))  # Apellido
                    var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem((registro[4])))  # Nombre
                    var.ui.tablaClientes.setItem(index, 3,
                                                 QtWidgets.QTableWidgetItem(("  " + registro[6] + "  ")))  # Dirección
                    var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem((registro[8])))  # Provincia
                    var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem((registro[9])))  # Municipio
                    var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(
                        ("  " + registro[2] + "  ")))  # Fecha de alta

                    # Alinea el texto de las celdas en la tabla
                    var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # Habilita o deshabilita los botones de navegación según la paginación
                var.ui.BtnSiguienteCli.setEnabled(end_index < total)  # Habilita el botón siguiente si hay más registros
                var.ui.BtnAnteriorCli.setEnabled(
                    var.current_page_cli > 0)  # Habilita el botón anterior si no estamos en la primera página

        except Exception as e:
            print("Error al cargar la tabla de clientes:", e)  # Si ocurre un error, se imprime el error


        except Exception as error:
            print("Error al cargar tabla clientes", error)

    def anteriorCliente(self):
        """
        Método que maneja la acción de navegar a la página anterior en la lista de clientes.

        Este método verifica si la página actual no es la primera (es decir, si el índice de la página es mayor que 0).
        Si es posible, decrementa el índice de la página y recarga la tabla de clientes para mostrar los datos correspondientes
        a la página anterior.

        :return: None
        :rtype: None
        """
        try:
            # Verifica si la página actual no es la primera
            if var.current_page_cli > 0:
                var.current_page_cli -= 1  # Decrementa el índice de la página para ir a la anterior

            # Llama al método para recargar la tabla de clientes con la página actualizada
            Clientes.cargaTablaClientes(self)

        except Exception as error:
            print("Error en anteriorCliente: ", error)  # En caso de error, lo imprime en la consola

    def siguienteCliente(self):
        """
        Método que maneja la acción de navegar a la siguiente página en la lista de clientes.

        Este método incrementa el índice de la página actual, permitiendo al usuario navegar hacia adelante
        en la lista de clientes. Después de actualizar el índice de la página, recarga la tabla de clientes para
        mostrar los datos correspondientes a la nueva página.

        :return: None
        :rtype: None
        """
        try:
            # Incrementa el índice de la página para ir a la siguiente
            var.current_page_cli += 1

            # Llama al método para recargar la tabla de clientes con la nueva página
            Clientes.cargaTablaClientes(self)

        except Exception as error:
            print("Error en siguienteCliente: ", error)  # Si ocurre un error, lo imprime en la consola

    def cargaTablaClientesServer(self):
        """
        Método que carga y muestra la lista de clientes desde un servidor en una tabla.

        Este método obtiene los datos de los clientes desde un servidor utilizando la conexión
        a través de `conexionserver.ConexionServer.listadoClientes`. Los datos obtenidos se presentan
        en una tabla en la interfaz de usuario. Si no hay clientes en la respuesta del servidor, se muestra un mensaje
        en la tabla indicando que no existen clientes.

        :return: None
        :rtype: None
        """
        try:
            # Obtiene la lista de clientes desde el servidor
            listado = conexionserver.ConexionServer.listadoClientes(self)

            # Establece el número de filas en la tabla según el número de clientes
            index = 0
            var.ui.tablaClientes.setRowCount(len(listado))

            # Si no se encontraron clientes, muestra un mensaje en la tabla
            if not listado:
                var.ui.tablaClientes.setRowCount(1)
                var.ui.tablaClientes.setItem(0, 2, QtWidgets.QTableWidgetItem("No existen Clientes con ese DNI"))
                var.ui.tablaClientes.item(0, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            else:
                # Si hay clientes, los agrega a la tabla
                for registro in listado:
                    var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem((registro[0])))  # DNI
                    var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem((registro[2])))  # Apellido
                    var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem((registro[3])))  # Nombre
                    var.ui.tablaClientes.setItem(index, 3,
                                                 QtWidgets.QTableWidgetItem(("  " + registro[5] + "  ")))  # Dirección
                    var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem((registro[7])))  # Provincia
                    var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem((registro[8])))  # Municipio
                    var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem((registro[9])))  # Fecha de alta

                    # Alinea el texto de las celdas en la tabla
                    var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1  # Aumenta el índice para la siguiente fila

        except Exception as error:
            print("Error al cargar tabla clientes", error)  # Si ocurre un error, se imprime el error

    def cargaOneCliente(self):
        """
        Método que carga los datos de un cliente seleccionado en la tabla y los muestra en los campos correspondientes.

        Este método obtiene los datos del cliente seleccionado en la tabla de clientes. Utiliza el DNI del cliente (obtenido
        de la selección en la tabla) para consultar los detalles completos del cliente a través de la conexión a la base de datos.
        Luego, los datos recuperados se muestran en los campos correspondientes de la interfaz de usuario, incluyendo
        texto y opciones de selección como provincia y municipio.

        :return: registro con los datos del cliente seleccionado
        :rtype: list
        """
        try:
            # Obtiene la fila seleccionada en la tabla de clientes
            fila = var.ui.tablaClientes.selectedItems()

            # Extrae los textos de las celdas seleccionadas para formar una lista de datos
            datos = [dato.text() for dato in fila]

            # Consulta los datos completos del cliente usando el DNI obtenido de la tabla
            registro = conexion.Conexion.datosOneCliente(datos[0])

            # Lista de campos de entrada en la interfaz donde se mostrarán los datos
            listado = [var.ui.txtDniCli, var.ui.txtAltaCli, var.ui.txtBajaCli, var.ui.txtApelCli,
                       var.ui.txtNomCli, var.ui.txtEmailCli, var.ui.txtMovilCli,
                       var.ui.txtDirCli, var.ui.cmbProCli, var.ui.cmbMuniCli]

            # Establece el DNI del cliente en el campo correspondiente
            var.ui.txtdniclifac.setText(registro[0])

            # Asigna los valores del cliente a los campos correspondientes
            for i in range(len(listado)):
                if i == 8 or i == 9:
                    # Si es un campo de selección (provincia o municipio), usa setCurrentText
                    listado[i].setCurrentText(registro[i])
                else:
                    # Para los demás campos, usa setText
                    listado[i].setText(registro[i])

            return registro  # Devuelve el registro con los datos del cliente

        except Exception as error:
            print("Error al cargar one clientes", error)  # En caso de error, lo imprime

    def modifCliente(self):
        """
        Método que permite modificar los datos de un cliente existente en la base de datos.

        Este método obtiene los datos del cliente desde los campos de la interfaz de usuario, verifica si el cliente
        existe en la base de datos y, si es así, procede a actualizar los datos. Si la modificación es exitosa, muestra
        un mensaje de éxito y actualiza la tabla de clientes. En caso de error, muestra un mensaje indicando el fallo.

        :return: None
        :rtype: None
        """
        try:
            # Obtiene los datos del cliente desde la interfaz de usuario
            modifcli = [var.ui.txtDniCli.text(), var.ui.txtAltaCli.text(), var.ui.txtBajaCli.text(),
                        var.ui.txtApelCli.text(),
                        var.ui.txtNomCli.text(), var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.txtDirCli.text(), var.ui.cmbProCli.currentText(),
                        var.ui.cmbMuniCli.currentText()]

            # Verifica si el cliente con el DNI especificado existe en la base de datos
            if conexion.Conexion.checkUserInDb(modifcli[0]):
                # Si el cliente existe, se modifica la información
                if conexion.Conexion.modifCliente(modifcli):
                    # Si la modificación es exitosa, muestra un mensaje de éxito
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Datos del cliente modificados')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()  # Muestra el mensaje de éxito
                    clientes.Clientes.cargaTablaClientes(self)  # Actualiza la tabla de clientes
                    eventos.Eventos.clearCampos(self)  # Limpia los campos de la interfaz
                else:
                    # Si la modificación falla, muestra un mensaje de error
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Error al modificar los datos del cliente')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()  # Muestra el mensaje de error
            else:
                # Si el cliente no existe en la base de datos, muestra un mensaje de error
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('El cliente no existe en la base de datos')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()  # Muestra el mensaje de error

        except Exception as error:
            # En caso de error en la ejecución, se imprime el mensaje de error
            print("Error en modifiCliente: ", error)

    def bajaCliente(self):
        """
        Método que permite dar de baja a un cliente en la base de datos.

        Este método obtiene el DNI del cliente y la fecha de baja desde los campos de la interfaz de usuario, verifica si
        el cliente existe en la base de datos, y si es así, procede a darlo de baja. Si la baja es exitosa, muestra un mensaje
        de éxito y actualiza la tabla de clientes. En caso de error, muestra un mensaje indicando el fallo.

        :return: None
        :rtype: None
        """
        try:
            # Obtiene los datos (DNI y fecha de baja) desde la interfaz de usuario
            datos = [var.ui.txtBajaCli.text(), var.ui.txtDniCli.text()]

            # Verifica si el cliente con el DNI especificado existe en la base de datos
            if conexion.Conexion.checkUserInDb(datos[1]):
                # Si el cliente existe, se procede a darlo de baja
                if conexion.Conexion.bajaCliente(datos):
                    # Si la baja es exitosa, muestra un mensaje de éxito
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Cliente borrado')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()  # Muestra el mensaje de éxito
                    clientes.Clientes.cargaTablaClientes(self)  # Actualiza la tabla de clientes
                    eventos.Eventos.clearCampos(self)  # Limpia los campos de la interfaz
                else:
                    # Si la baja falla, muestra un mensaje de error
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QIcon('./img/logo.ico'))
                    mbox.setText('Error al dar de baja')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()  # Muestra el mensaje de error
            else:
                # Si el cliente no existe en la base de datos, muestra un mensaje de error
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('./img/logo.ico'))
                mbox.setText('El cliente no existe en la base de datos')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()  # Muestra el mensaje de error

        except Exception as error:
            # En caso de error en la ejecución, se imprime el mensaje de error
            print("Error en bajaCliente: ", error)

    def historicoCli(self):
        """
        Método que maneja la selección de la casilla de verificación (checkbox) para mostrar o no el historial de clientes.

        Este método comprueba si la casilla de verificación (chkHistoriaCli) está marcada o no. Dependiendo de su estado,
        cambia el valor de la variable `var.historico`, que se usa para filtrar si se deben mostrar solo clientes actuales
        o clientes con un historial. Posteriormente, actualiza la tabla de clientes según esta configuración.

        :return: None
        :rtype: None
        """
        try:
            # Verifica si la casilla de verificación para el historial de clientes está marcada
            if var.ui.chkHistoriaCli.isChecked():
                # Si está marcada, se configura var.historico en 0 (clientes actuales)
                var.historico = 0
            else:
                # Si no está marcada, se configura var.historico en 1 (clientes históricos)
                var.historico = 1

            # Actualiza la tabla de clientes según la nueva configuración del historial
            Clientes.cargaTablaClientes(self)

        except Exception as error:
            # En caso de error en la ejecución, se imprime el mensaje de error
            print("Error en historicoCli: ", error)

    def filtrarProp(self):
        """
        Método que maneja la acción del botón de búsqueda para filtrar los clientes según un criterio.

        Este método comprueba si el botón de búsqueda (`btnBuscarCli`) está seleccionado o no. Si está marcado, lo desmarca
        y si está desmarcado, lo marca. Después, se actualiza la tabla de clientes para reflejar el nuevo filtro de búsqueda.

        :return: None
        :rtype: None
        """
        try:
            # Comprueba si el botón de búsqueda está marcado (seleccionado)
            checkeado = var.ui.btnBuscarCli.isChecked()

            # Cambia el estado del botón de búsqueda (si estaba marcado, ahora se desmarca y viceversa)
            var.ui.btnBuscarCli.setChecked(not checkeado)

            # Actualiza la tabla de clientes según el nuevo estado del botón de búsqueda
            Clientes.cargaTablaClientes(self)

        except Exception as error:
            # En caso de error, se captura y se imprime el mensaje de error
            print("Error en filtrarProp: ", error)


