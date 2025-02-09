import os
from datetime import datetime

from PyQt6 import QtSql, QtWidgets, QtCore


import eventos
import var



class Conexion:

    '''

    método de una clase que no depende de una instancia específica de esa clase.
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase.
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.

    '''

    @staticmethod
    def db_conexion(self = None):
        """

        :param self: None
        :type self:  None
        :return: False or True
        :rtype: Booleano

        Modulo para establecer la conexion  a la base de datos
        Si exito devuelve True, si no, False
        """
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                               QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False



    @staticmethod
    def listaProv(self):
        """

        :param self:  None
        :type self:  None
        :return: lista proivincias
        :rtype: bytearray

        Modulo para obtener la lista de provincias
        """
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMuni(provincia):
        """

        :param provincia: nombre provincia
        :type provincia: bytearray
        :return: lista municipios
        :rtype: bytearray

        Modulo que devuelve listao de municipios de una provincia
        """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM municipios"
                      " WHERE fk_idprov = (SELECT idprov FROM provincias WHERE provincia = :provincia)")
        query.bindValue(":provincia", provincia)
        listaprov = []
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def altaCliente(nuevocli):
        """

        :param nuevocli: array con datos clientes
        :type nuevocli: lista
        :return: true o false
        :rtype:  booleano

        Metodo que inserta datos de un cliente en la BBDD
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO CLIENTES (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli) "
                "VALUES (:dnicli, :altacli, :apelcli, :nomecli, :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevocli[0]))
            query.bindValue(":altacli", str(nuevocli[1]))
            query.bindValue(":apelcli", str(nuevocli[2]))
            query.bindValue(":nomecli", str(nuevocli[3]))
            query.bindValue(":emailcli", str(nuevocli[4]))
            query.bindValue(":movilcli", str(nuevocli[5]))
            query.bindValue(":dircli", str(nuevocli[6]))
            query.bindValue(":provcli", str(nuevocli[7]))
            query.bindValue(":municli", str(nuevocli[8]))


            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("error altaCliente", e)

    @staticmethod
    def altaVendedor(nuevoVendedor):
        """
        :param nuevoVendedor: array con los datos del vendedor
        :type nuevoVendedor: lista
        :return: true o false, dependiendo de si la inserción fue exitosa
        :rtype: booleano

        Método que inserta los datos de un nuevo vendedor en la base de datos.
        """
        try:
            # Crear un objeto de tipo QSqlQuery para preparar la consulta SQL
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL de inserción
            query.prepare(
                "INSERT INTO  Vendedores(dniVendedor, nombreVendedor, movilVendedor, mailVendedor,delegacionVendedor,altaVendedor ) "
                "VALUES (:dniVen, :nomVen, :movilVen, :mailVen, :delegVen, :altaVen)"
            )

            # Asociar los valores de la lista 'nuevoVendedor' con los parámetros de la consulta SQL
            query.bindValue(":dniVen", str(nuevoVendedor[0]))  # DNI del vendedor
            query.bindValue(":nomVen", str(nuevoVendedor[1]))  # Nombre del vendedor
            query.bindValue(":movilVen", str(nuevoVendedor[2]))  # Teléfono móvil del vendedor
            query.bindValue(":mailVen", str(nuevoVendedor[3]))  # Correo electrónico del vendedor
            query.bindValue(":delegVen", str(nuevoVendedor[4]))  # Delegación del vendedor
            query.bindValue(":altaVen", str(nuevoVendedor[5]))  # Fecha de alta del vendedor

            # Ejecutar la consulta y devolver True si la inserción fue exitosa
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error altaCliente clase eventos", e)

    def listadoClientes(self):
        """

        :return: devuelve listado de clientes
        :rtype: list

        Metodo que devuelve todos los clientes ordenados por apellidos y nombres
        """
        try:
            listado = []
            historico = var.ui.chkHistoriaCli.isChecked()
            filtrado = var.ui.btnBuscarCli.isChecked()
            DniSeleccionado = var.ui.txtDniCli.text()
            if not historico and not filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE bajacli is NULL ORDER BY apelcli, nomecli ASC ")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

            elif historico and not filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC ")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

            elif historico and filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE dnicli = :dnicli ORDER BY apelcli, nomecli ASC ")
                query.bindValue(":dnicli", DniSeleccionado)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

            elif not historico and filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE dnicli = :dnicli AND bajacli is NULL  ORDER BY apelcli, nomecli ASC ")
                query.bindValue(":dnicli", DniSeleccionado)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

        except Exception as e:
            print("Error listado en conexion", e)

    def listadoVendedores(self):
        """

                :return: devuelve listado de vendedores
                :rtype: list

                Metodo que devuelve todos los vendedores ordenados por id
                """
        try:
            listado = []
            historico = var.ui.chkHistoricoVen.isChecked()
            filtrado = var.ui.btnBuscarCli.isChecked()
            movilSeleccionado = var.ui.txtMovilVen.text()
            if not historico and not filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM Vendedores WHERE bajaVendedor is NULL ORDER BY idVendedor ASC ")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

            elif historico and not filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM Vendedores ORDER BY idVendedor ASC ")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

            elif historico and filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM Vendedores WHERE movilVendedor = :movilVen ORDER BY idVendedor ASC ")
                query.bindValue(":movilVen", movilSeleccionado)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

            elif not historico and filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM Vendedores WHERE movilVendedor = :movilVen AND bajaVendedor is NULL  ORDER BY idVendedor ASC ")
                query.bindValue(":movilVen", movilSeleccionado)
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

        except Exception as e:
            print("Error listado en conexion", e)



    def listadoPropiedades(self):
        """

                :return: devuelve listado de propiedades
                :rtype: list

                Metodo que devuelve todos las propiedades ordenadas por municipio
                """
        try:
            listado = []
            historico = var.ui.chkHistoriaProp.isChecked()
            municipio = var.ui.cmbMuniProp.currentText()
            filtrado = var.ui.btnBuscarTipoProp.isChecked()
            tipoSeleccionado = var.ui.cmbTipoProp.currentText()
            if not historico and filtrado:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT * FROM PROPIEDADES where bajaprop is null and estadoprop = 'Disponible' and tipoprop = :tipo_propiedad  and muniprop = :municipio order by muniprop asc")
                query.bindValue(":tipo_propiedad", str(tipoSeleccionado))
                query.bindValue(":municipio", str(municipio))
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            elif historico and not filtrado:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades ORDER BY muniprop ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            elif historico and filtrado:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT * FROM PROPIEDADES where estadoprop = 'Disponible' and tipoprop = :tipo_propiedad and muniprop = :municipio order by muniprop asc")
                query.bindValue(":tipo_propiedad", str(tipoSeleccionado))
                query.bindValue(":municipio", str(municipio))
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades where bajaprop is null ORDER BY muniprop ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            return listado

        except Exception as e:
            print("Error al listar propiedades en listadoPropiedades", e)


    def datosOneCliente(dni):
        """
        :param dni: String con el dni del cliente
        :type dni: string
        :return: retorna una lista con los datos del cliente
        :rtype: list

        Metodo que devuelve una lista con los datos de un cliente de la base de datosç

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('SELECT * FROM CLIENTES WHERE dnicli = :dnicli')
            query.bindValue(':dnicli', str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro

        except Exception as error:
            print("error en datosOneCliente ", error)

    def datosOneVendedor(id):
        """
        :param id: ID del vendedor que se desea consultar
        :type id: entero o cadena
        :return: Lista con los datos del vendedor encontrado, o una lista vacía si no se encuentra
        :rtype: lista

        Método que obtiene los datos de un vendedor específico a partir de su ID desde la base de datos.
        """
        try:
            # Inicializar una lista vacía para almacenar los datos del vendedor
            registro = []

            # Crear un objeto de tipo QSqlQuery para realizar la consulta SQL
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para obtener los datos del vendedor con el ID especificado
            query.prepare('SELECT * FROM Vendedores WHERE idVendedor = :idVend')

            # Asociar el valor del ID del vendedor con el parámetro de la consulta SQL
            query.bindValue(':idVend', str(id))

            # Ejecutar la consulta y procesar los resultados si es exitosa
            if query.exec():
                # Iterar sobre los registros devueltos por la consulta
                while query.next():
                    # Iterar sobre todas las columnas del registro y agregar los valores a la lista 'registro'
                    for i in range(query.record().count()):
                        registro.append(query.value(i))

            # Retornar la lista con los datos del vendedor
            return registro

        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error en datosOneCliente ", error)

    def datosOnePropiedad(codigo):
        """
        :param codigo: Código de la propiedad que se desea consultar
        :type codigo: entero o cadena
        :return: Lista con los datos de la propiedad encontrada, o una lista vacía si no se encuentra
        :rtype: lista

        Método que obtiene los datos de una propiedad específica a partir de su código desde la base de datos.
        """
        try:
            # Inicializar una lista vacía para almacenar los datos de la propiedad
            registro = []

            # Crear un objeto de tipo QSqlQuery para realizar la consulta SQL
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para obtener los datos de la propiedad con el código especificado
            query.prepare('SELECT * FROM propiedades WHERE codigo = :codigo')

            # Asociar el valor del código de la propiedad con el parámetro de la consulta SQL
            query.bindValue(':codigo', str(codigo))

            # Ejecutar la consulta y procesar los resultados si es exitosa
            if query.exec():
                # Iterar sobre los registros devueltos por la consulta
                while query.next():
                    # Iterar sobre todas las columnas del registro y agregar los valores a la lista 'registro'
                    for i in range(query.record().count()):
                        registro.append(query.value(i))

            # Retornar la lista con los datos de la propiedad
            return registro

        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error en datosOnePropiedad ", error)

    def modifCliente(registro):
        """
        :param registro: array con los datos del cliente a modificar
        :type registro: lista
        :return: True si la modificación fue exitosa, False si ocurrió un error o no se encontró el cliente
        :rtype: booleano

        Método que actualiza los datos de un cliente existente en la base de datos, basado en su DNI.
        """
        try:
            # Crear un objeto QSqlQuery para verificar si el cliente con el DNI especificado ya existe en la base de datos
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dnicli")
            query.bindValue(":dnicli", str(registro[0]))

            # Ejecutar la consulta y verificar si el cliente existe
            if query.exec():
                if query.next() and query.value(0) > 0:

                    # Si el cliente existe, proceder a actualizar sus datos
                    query = QtSql.QSqlQuery()
                    query.prepare(
                        "UPDATE clientes SET altacli = :altacli , apelcli = :apelcli, nomecli = :nomecli, emailcli = :emailcli, movilcli = :movilcli, dircli = :dircli, provcli = :provcli, municli = :municli, bajacli = :bajacli WHERE dnicli = :dnicli")

                    # Asociar los valores del array 'registro' a los parámetros de la consulta SQL
                    query.bindValue(':dnicli', str(registro[0]))
                    query.bindValue(':altacli', str(registro[1]))
                    query.bindValue(':apelcli', str(registro[3]))
                    query.bindValue(':nomecli', str(registro[4]))
                    query.bindValue(':emailcli', str(registro[5]))
                    query.bindValue(':movilcli', str(registro[6]))
                    query.bindValue(':dircli', str(registro[7]))
                    query.bindValue(':provcli', str(registro[8]))
                    query.bindValue(':municli', str(registro[9]))

                    # Comprobar si la fecha de baja está vacía, si lo está, no se asigna valor
                    if registro[2] == "":
                        query.bindValue(":bajacli", QtCore.QVariant())
                    else:
                        query.bindValue(":bajacli", str(registro[2]))

                    # Ejecutar la actualización y devolver True si la operación fue exitosa
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    # Si el cliente no existe en la base de datos, retornar False
                    return False
            else:
                # Si hubo un error en la consulta de verificación, retornar False
                return False

        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error modificar cliente", error)

    def modifVend(registro):
        """
        :param registro: array con los datos del vendedor a modificar
        :type registro: lista
        :return: True si la modificación fue exitosa, False si ocurrió un error o no se encontró el vendedor
        :rtype: booleano

        Método que actualiza los datos de un vendedor existente en la base de datos, basado en su ID.
        """
        try:
            # Crear un objeto QSqlQuery para verificar si el vendedor con el ID especificado ya existe en la base de datos
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from Vendedores where idVendedor = :idVendedor")
            query.bindValue(":idVendedor", str(registro[0]))

            # Ejecutar la consulta y verificar si el vendedor existe
            if query.exec():
                if query.next() and query.value(0) > 0:

                    # Si el vendedor existe, proceder a actualizar sus datos
                    query = QtSql.QSqlQuery()
                    query.prepare(
                        "UPDATE Vendedores SET  nombreVendedor= :nombVend , altaVendedor = :altVen, movilVendedor = :movVend, mailVendedor = :emailVend, delegacionVendedor = :delegVend WHERE idVendedor = :idVend")

                    # Asociar los valores del array 'registro' a los parámetros de la consulta SQL
                    query.bindValue(':idVend', str(registro[0]))
                    query.bindValue(':nombVend', str(registro[2]))
                    query.bindValue(':altVen', str(registro[6]))
                    query.bindValue(':movVend', str(registro[3]))
                    query.bindValue(':emailVend', str(registro[4]))
                    query.bindValue(':delegVend', str(registro[5]))

                    # Ejecutar la actualización y devolver True si la operación fue exitosa
                    if query.exec():
                        return True
                    else:
                        # Si la ejecución de la actualización falla, mostrar un mensaje de error y retornar False
                        print("error1")
                        return False
                else:
                    # Si el vendedor no existe en la base de datos, mostrar un mensaje de error y retornar False
                    print("error3")
                    return False
            else:
                # Si hubo un error en la consulta de verificación, mostrar un mensaje de error y retornar False
                print("error2")
                return False

        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error modificar cliente", error)

    def modifPropiedad(registro):
        """
        :param registro: array con los datos de la propiedad a modificar
        :type registro: lista
        :return: True si la modificación fue exitosa, False si ocurrió un error o no se encontró la propiedad
        :rtype: booleano

        Método que actualiza los datos de una propiedad existente en la base de datos, basado en su código.
        """
        try:
            # Crear un objeto QSqlQuery para verificar si la propiedad con el código especificado ya existe en la base de datos
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", str(registro[0]))

            # Ejecutar la consulta y verificar si la propiedad existe
            if query.exec():
                if query.next() and query.value(0) > 0:

                    # Si la propiedad existe, proceder a actualizar sus datos
                    query = QtSql.QSqlQuery()
                    query.prepare(
                        "UPDATE propiedades SET altaprop = :altaprop, bajaprop = :bajaprop, dirprop = :dirprop, provprop = :provprop, muniprop = :muniprop, tipoprop = :tipoprop, habprop = :habprop, banoprop = :banoprop, superprop = :superprop, precioventaprop = :precioventaprop, precioalquilerprop = :precioalquilerprop, cpprop = :cpprop, descriprop = :descriprop, tipoperprop = :tipoperprop, estadoprop = :estadoprop, nomeprop = :nomeprop, movilprop = :movilprop WHERE codigo = :codigo")

                    # Asociar los valores del array 'registro' a los parámetros de la consulta SQL
                    query.bindValue(':codigo', str(registro[0]))
                    query.bindValue(':altaprop', str(registro[1]))
                    query.bindValue(':dirprop', str(registro[3]))
                    query.bindValue(':provprop', str(registro[4]))
                    query.bindValue(':muniprop', str(registro[5]))
                    query.bindValue(':tipoprop', str(registro[6]))
                    query.bindValue(':habprop', int(registro[7]))  # Se espera un valor entero
                    query.bindValue(':banoprop', int(registro[8]))  # Se espera un valor entero
                    query.bindValue(':superprop', str(registro[9]))
                    query.bindValue(':precioventaprop', str(registro[10]))
                    query.bindValue(':precioalquilerprop', str(registro[11]))
                    query.bindValue(':cpprop', str(registro[12]))
                    query.bindValue(':descriprop', str(registro[13]))
                    query.bindValue(':tipoperprop', ",".join(registro[14]))  # Unir lista de tipos de operación
                    query.bindValue(':estadoprop', str(registro[15]))
                    query.bindValue(':nomeprop', str(registro[16]))
                    query.bindValue(':movilprop', str(registro[17]))

                    # Comprobar si la fecha de baja está vacía, si lo está, no se asigna valor
                    if registro[2] == "":
                        query.bindValue(":bajaprop", QtCore.QVariant())
                    else:
                        query.bindValue(":bajaprop", str(registro[2]))

                    # Ejecutar la actualización y devolver True si la operación fue exitosa
                    if query.exec():
                        return True
            # Si no se encontró la propiedad, o si ocurre un error en la consulta, no se realiza la actualización
        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error modificar propiedad", error)

    def bajaCliente(datos):
        """
        :param datos: array con los datos del cliente, incluyendo el DNI
        :type datos: lista
        :return: True si la baja fue exitosa, False si ocurrió un error
        :rtype: booleano

        Método que marca a un cliente como dado de baja en la base de datos, asignando la fecha actual a su campo 'bajacli'.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL de actualización
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para actualizar la fecha de baja del cliente
            query.prepare('UPDATE clientes SET bajacli = :bajacli WHERE dnicli = :dnicli')

            # Asociar la fecha actual a la columna 'bajacli' usando el formato dd/mm/yyyy
            query.bindValue(':bajacli', datetime.now().strftime("%d/%m/%Y"))

            # Asociar el DNI del cliente al parámetro correspondiente de la consulta SQL
            query.bindValue(':dnicli', str(datos[1]))

            # Ejecutar la consulta de actualización y devolver True si fue exitosa
            if query.exec():
                return True
            else:
                # Si la ejecución de la consulta falla, retornar False
                return False
        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error en bajaCliente ", error)

    def bajaVendedor(datos):
        """
        :param datos: array con los datos del vendedor, incluyendo el ID del vendedor
        :type datos: lista
        :return: True si la baja fue exitosa, False si ocurrió un error
        :rtype: booleano

        Método que marca a un vendedor como dado de baja en la base de datos, asignando la fecha actual a su campo 'bajaVendedor'.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL de actualización
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para actualizar la fecha de baja del vendedor
            query.prepare('UPDATE vendedores SET bajaVendedor = :bajaVendedor WHERE idVendedor = :idVend')

            # Asociar la fecha actual a la columna 'bajaVendedor' usando el formato dd/mm/yyyy
            query.bindValue(':bajaVendedor', datetime.now().strftime("%d/%m/%Y"))

            # Asociar el ID del vendedor al parámetro correspondiente de la consulta SQL
            query.bindValue(':idVend', str(datos[1]))

            # Ejecutar la consulta de actualización y devolver True si fue exitosa
            if query.exec():
                return True
            else:
                # Si la ejecución de la consulta falla, retornar False
                return False
        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error en bajaCliente ", error)

    def checkUserInDb(dni):
        """
        :param dni: El DNI del cliente que se va a buscar en la base de datos
        :type dni: str
        :return: True si el cliente existe en la base de datos, False si no existe o ocurrió un error
        :rtype: booleano

        Método que verifica si un cliente con el DNI especificado ya existe en la base de datos.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para buscar un cliente con el DNI especificado
            query.prepare('SELECT * FROM clientes WHERE dnicli = :dnicli')

            # Asociar el DNI proporcionado al parámetro correspondiente de la consulta SQL
            query.bindValue(':dnicli', str(dni))

            # Ejecutar la consulta y verificar si hay algún resultado
            if query.exec():
                # Si hay un registro que coincide, devolver True
                if query.next():
                    return True
                else:
                    # Si no se encuentra ningún cliente con el DNI dado, devolver False
                    return False
        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error en checkUserInDb ", error)

    def checkVendedorinDb(id):
        """
        :param id: El ID del vendedor que se va a buscar en la base de datos
        :type id: str
        :return: True si el vendedor existe en la base de datos, False si no existe o ocurrió un error
        :rtype: booleano

        Método que verifica si un vendedor con el ID especificado ya existe en la base de datos.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para buscar un vendedor con el ID especificado
            query.prepare('SELECT * FROM Vendedores WHERE idVendedor = :idVend')

            # Asociar el ID proporcionado al parámetro correspondiente de la consulta SQL
            query.bindValue(':idVend', str(id))

            # Ejecutar la consulta y verificar si hay algún resultado
            if query.exec():
                # Si hay un registro que coincide, devolver True
                if query.next():
                    return True
                else:
                    # Si no se encuentra ningún vendedor con el ID dado, devolver False
                    return False
        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error en checkVendedorinDb ", error)

    def checkDNIinDb(dni):
        """
        :param dni: El DNI o ID del vendedor que se va a buscar en la base de datos
        :type dni: str
        :return: True si el vendedor con ese DNI existe en la base de datos, False si no existe o ocurrió un error
        :rtype: booleano

        Método que verifica si un vendedor con el DNI especificado ya existe en la base de datos.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para buscar un vendedor con el ID especificado
            query.prepare('SELECT * FROM Vendedores WHERE idVendedor = :idVend')

            # Asociar el DNI proporcionado al parámetro correspondiente de la consulta SQL
            query.bindValue(':idVend', str(dni))

            # Ejecutar la consulta y verificar si hay algún resultado
            if query.exec():
                # Si hay un registro que coincide, devolver True
                if query.next():
                    return True
                else:
                    # Si no se encuentra ningún vendedor con el DNI dado, devolver False
                    return False
        except Exception as error:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error en checkVendedorinDb ", error)

    def altaTipoProp(tipo):
        """
        :param tipo: El tipo de propiedad que se va a insertar en la base de datos
        :type tipo: str
        :return: Una lista con todos los tipos de propiedad ordenados alfabéticamente si la inserción es exitosa,
                 False si ocurre un error al insertar
        :rtype: lista o booleano

        Método que inserta un nuevo tipo de propiedad en la base de datos y devuelve la lista de tipos de propiedad ordenada.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL de inserción
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para insertar el nuevo tipo de propiedad en la base de datos
            query.prepare("INSERT INTO tipopropiedad (tipo) VALUES (:tipo)")

            # Asociar el valor del parámetro 'tipo' a la consulta SQL
            query.bindValue(":tipo", tipo)

            # Ejecutar la consulta de inserción
            if query.exec():
                # Si la inserción es exitosa, realizar otra consulta para obtener todos los tipos de propiedad
                query = QtSql.QSqlQuery()
                query.prepare("SELECT tipo FROM tipopropiedad ORDER BY tipo ASC")

                # Ejecutar la consulta de selección
                if query.exec():
                    registro = []
                    # Iterar sobre los resultados y añadirlos a la lista 'registro'
                    while query.next():
                        registro.append(str(query.value(0)))
                    # Devolver la lista de tipos de propiedad ordenados alfabéticamente
                    return registro
            else:
                # Si la inserción falla, devolver False
                return False
        except Exception as e:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error altaTipoProp", e)

    def cargarTipoProp(self):
        """
        :return: Una lista con todos los tipos de propiedad ordenados alfabéticamente, o None si ocurre un error
        :rtype: lista o None

        Método que carga y devuelve todos los tipos de propiedad desde la base de datos, ordenados alfabéticamente.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL de selección
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para obtener los tipos de propiedad ordenados alfabéticamente
            query.prepare("SELECT tipo FROM tipopropiedad ORDER BY tipo ASC")

            # Ejecutar la consulta SQL
            if query.exec():
                registro = []
                # Iterar sobre los resultados de la consulta y agregarlos a la lista 'registro'
                while query.next():
                    registro.append(str(query.value(0)))
                # Devolver la lista de tipos de propiedad
                return registro
        except Exception as e:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error cargarTipoProp", e)

    def bajaTipoProp(tipo):
        """
        :param tipo: El tipo de propiedad que se desea eliminar de la base de datos
        :type tipo: str
        :return: True si el tipo de propiedad fue eliminado correctamente, False si no se encontró o ocurrió un error
        :rtype: booleano

        Método que elimina un tipo de propiedad de la base de datos si existe.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL de verificación
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para verificar si el tipo de propiedad existe en la base de datos
            query.prepare("SELECT COUNT(*) FROM tipopropiedad WHERE tipo = :tipo")

            # Asociar el valor del parámetro 'tipo' a la consulta SQL
            query.bindValue(":tipo", tipo)

            # Ejecutar la consulta de verificación
            if query.exec() and query.next() and query.value(0) > 0:
                # Si el tipo de propiedad existe, preparar la consulta para eliminarlo
                query.prepare("DELETE FROM tipopropiedad WHERE tipo = :tipo")

                # Volver a asociar el valor del parámetro 'tipo'
                query.bindValue(":tipo", tipo)

                # Ejecutar la consulta de eliminación
                if query.exec():
                    # Si la eliminación es exitosa, recargar los tipos de propiedad y devolver True
                    eventos.Eventos.cargarTipoProp(tipo)
                    return True
                else:
                    # Si ocurre un error en la eliminación, recargar los tipos de propiedad y devolver False
                    eventos.Eventos.cargarTipoProp(tipo)
                    return False
            else:
                # Si el tipo no existe, devolver False
                return False
        except Exception as e:
            # Capturar y mostrar cualquier error que ocurra durante la ejecución
            print("error bajaTipoProp", e)
            return False

    @staticmethod
    def altaPropiedad(propiedad):
        """
        :param propiedad: Una lista que contiene los datos de la propiedad a insertar en la base de datos
        :type propiedad: lista
        :return: True si la propiedad se inserta correctamente, False si ocurre un error
        :rtype: booleano

        Método que inserta una nueva propiedad en la base de datos.
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL de inserción
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para insertar los valores de la propiedad en la tabla 'propiedades'
            query.prepare(
                "INSERT INTO propiedades (altaprop, dirprop, provprop, muniprop, tipoprop, habprop,"
                " banoprop, superprop, precioventaprop, precioalquilerprop, cpprop,"
                " descriprop, tipoperprop, estadoprop, nomeprop, movilprop ) "
                "VALUES (:altaprop, :dirprop, :provprop, :muniprop, :tipoprop, :habprop,"
                " :banoprop, :superprop, :precioventaprop, :precioalquilerprop, :cpprop,"
                " :descriprop, :tipoperprop, :estadoprop, :nomeprop, :movilprop)"
            )

            # Asociar cada parámetro de la consulta con los valores proporcionados en la lista 'propiedad'
            query.bindValue(":altaprop", str(propiedad[0]))
            query.bindValue(":dirprop", str(propiedad[1]))
            query.bindValue(":provprop", str(propiedad[2]))
            query.bindValue(":muniprop", str(propiedad[3]))
            query.bindValue(":tipoprop", str(propiedad[4]))
            query.bindValue(":habprop", int(propiedad[5]))
            query.bindValue(":banoprop", int(propiedad[6]))
            query.bindValue(":superprop", str(propiedad[7]))
            query.bindValue(":precioventaprop", str(propiedad[8]))
            query.bindValue(":precioalquilerprop", str(propiedad[9]))
            query.bindValue(":cpprop", str(propiedad[10]))
            query.bindValue(":descriprop", str(propiedad[11]))
            query.bindValue(":tipoperprop", ",".join((propiedad[12])))  # Convertir lista a string separada por comas
            query.bindValue(":estadoprop", str(propiedad[13]))
            query.bindValue(":nomeprop", str(propiedad[14]))
            query.bindValue(":movilprop", str(propiedad[15]))

            # Ejecutar la consulta para insertar los datos en la base de datos
            if query.exec():
                return True  # Si la inserción es exitosa, devolver True
            else:
                # Si ocurre un error, imprimir el mensaje de error y devolver False
                print(query.lastError().text())
                return False
        except Exception as e:
            # Capturar cualquier excepción y mostrar el error
            print("error altaProp", e)
            return False

    @staticmethod
    def bajaProp(propiedad):
        """
        :param propiedad: Lista que contiene los datos necesarios para dar de baja una propiedad
        :type propiedad: lista
        :return: True si la propiedad se da de baja correctamente, False en caso contrario
        :rtype: booleano

        Método que marca una propiedad como dada de baja en la base de datos.
        Actualiza los campos 'bajaprop' (fecha de baja) y 'estadoprop' (estado de la propiedad).
        """
        try:
            # Crear un objeto QSqlQuery para realizar la consulta SQL
            query = QtSql.QSqlQuery()

            # Comprobar si la propiedad existe en la base de datos mediante el código
            query.prepare("select count(*) from Propiedades where codigo = :codigo")
            query.bindValue(":codigo", propiedad[0])  # Se asume que el primer valor en 'propiedad' es el código
            if query.exec() and query.next():  # Ejecuta la consulta y comprueba si hay resultados
                count = query.value(0)
                if count == 1:  # Si solo se encuentra una propiedad con ese código, significa que existe
                    # Preparar la consulta para actualizar la propiedad (marcar como dada de baja)
                    query.prepare(
                        "update Propiedades set bajaprop =:baja, estadoprop =:estadoprop where codigo = :codigo")
                    query.bindValue(":codigo", str(propiedad[0]))  # Código de la propiedad
                    query.bindValue(":baja", str(
                        propiedad[2]))  # Fecha de baja (proporcionada en el tercer espacio del array 'propiedad')
                    query.bindValue(":estadoprop",
                                    str(propiedad[3]))  # Estado de la propiedad (proporcionado en el cuarto espacio)

                    # Ejecutar la consulta para actualizar la propiedad
                    if query.exec():
                        return True  # Si la consulta se ejecuta correctamente, la propiedad fue dada de baja
                    else:
                        return False  # Si no se puede ejecutar la consulta, devolver False
                else:
                    return False  # Si la propiedad no existe en la base de datos, devolver False
            else:
                return False  # Si la consulta no se puede ejecutar, devolver False

        except Exception as e:
            # Capturar cualquier excepción que ocurra durante el proceso y mostrar el error
            print("Error al dar de baja propiedad en conexión.", e)
            return False  # En caso de error, devolver False

    def listadoPropiedadesExport(self):
        """
        :return: Una lista con todos los registros de propiedades de la base de datos, ordenados por municipio
        :rtype: list

        Método que obtiene un listado de todas las propiedades de la base de datos, sin filtrar por baja
        (es decir, incluirá tanto las propiedades dadas de baja como las activas) y las ordena por municipio.
        """
        listado = []  # Inicializa una lista vacía para almacenar los resultados de la consulta

        # Crear un objeto QSqlQuery para realizar la consulta SQL
        query = QtSql.QSqlQuery()

        # Preparar la consulta SQL para seleccionar todas las propiedades, tanto activas como dadas de baja
        query.prepare(
            "SELECT * FROM PROPIEDADES where bajaprop is null or bajaprop is not null order by muniprop asc")

        # Ejecutar la consulta
        if query.exec():
            # Si la consulta se ejecuta correctamente, recorrer todos los resultados
            while query.next():
                # Para cada fila, crear una lista de los valores de las columnas y agregarla a 'listado'
                fila = [query.value(i) for i in range(query.record().count())]
                listado.append(fila)

        # Devolver la lista con los resultados
        return listado

    def listadoClientesExport(self):
        """
        :return: Una lista con todos los registros de clientes de la base de datos, ordenados por apellido.
        :rtype: list

        Método que obtiene un listado de todos los clientes de la base de datos, sin filtrar por baja
        (es decir, incluirá tanto los clientes dados de baja como los activos) y los ordena por apellido.
        """
        listado = []  # Inicializa una lista vacía para almacenar los resultados de la consulta.

        # Crear un objeto QSqlQuery para realizar la consulta SQL.
        query = QtSql.QSqlQuery()

        # Preparar la consulta SQL para seleccionar todos los clientes, tanto activos como dados de baja.
        query.prepare(
            "SELECT * FROM CLIENTES where bajacli is null or bajacli is not null order by apelcli asc")

        # Ejecutar la consulta.
        if query.exec():
            # Si la consulta se ejecuta correctamente, recorrer todos los resultados.
            while query.next():
                # Para cada fila, crear una lista de los valores de las columnas y agregarla a 'listado'.
                fila = [query.value(i) for i in range(query.record().count())]
                listado.append(fila)

        # Devolver la lista con los resultados.
        return listado

    def listadoVendedoresExport(self):
        """
        :return: Una lista con todos los registros de vendedores de la base de datos, ordenados por ID de vendedor.
        :rtype: list

        Método que obtiene un listado de todos los vendedores de la base de datos, sin filtrar por baja
        (es decir, incluirá tanto los vendedores dados de baja como los activos) y los ordena por el ID de vendedor.
        """
        listado = []  # Inicializa una lista vacía para almacenar los resultados de la consulta.

        # Crear un objeto QSqlQuery para realizar la consulta SQL.
        query = QtSql.QSqlQuery()

        # Preparar la consulta SQL para seleccionar todos los vendedores, tanto activos como dados de baja.
        query.prepare(
            "SELECT * FROM vendedores where bajaVendedor is null or bajaVendedor is not null order by idVendedor asc")

        # Ejecutar la consulta.
        if query.exec():
            # Si la consulta se ejecuta correctamente, recorrer todos los resultados.
            while query.next():
                # Para cada fila, crear una lista de los valores de las columnas y agregarla a 'listado'.
                fila = [query.value(i) for i in range(query.record().count())]
                listado.append(fila)

        # Devolver la lista con los resultados.
        return listado

    @staticmethod
    def altaFactura(registro):
        """
        :param registro: Una lista con los datos necesarios para crear una nueva factura.
        :type registro: list
        :return: True si la factura se inserta correctamente, False en caso contrario.
        :rtype: bool

        Método que da de alta una nueva factura en la base de datos. La factura contiene la fecha y el DNI del cliente.
        """
        try:
            # Crear un objeto QSqlQuery para ejecutar la consulta SQL.
            query = QtSql.QSqlQuery()

            # Preparar la consulta SQL para insertar una nueva factura en la tabla FACTURAS.
            query.prepare("INSERT INTO FACTURAS (fechafac, dnifac) VALUES (:fechafac, :dnifac)")

            # Vincular los valores de los parámetros de la consulta con los valores del registro.
            query.bindValue(":fechafac", registro[0])  # Fecha de la factura.
            query.bindValue(":dnifac", registro[1])  # DNI del cliente.

            # Ejecutar la consulta.
            if query.exec():
                # Si la consulta se ejecuta correctamente, devolver True.
                return True
            else:
                # Si hubo un error al ejecutar la consulta, devolver False.
                return False
        except Exception as e:
            # Si ocurre una excepción (error en la ejecución), imprimir el error y devolver False.
            print("Error al dar de alta factura en conexion:", e)
            return False

    @staticmethod
    def listadoFacturas():
        """
        :return: Una lista con los registros de las facturas, donde cada factura es representada
                 por una lista que contiene el id, el DNI del cliente y la fecha de la factura.
        :rtype: list

        Método que consulta todas las facturas en la base de datos y devuelve una lista con los resultados.
        Cada factura en la lista estará representada por el id, el dni del cliente y la fecha de la factura.
        """
        try:
            # Inicializamos la lista donde almacenaremos las facturas.
            listado = []

            # Creamos un objeto QSqlQuery para ejecutar la consulta SQL.
            query = QtSql.QSqlQuery()

            # Preparamos la consulta SQL para seleccionar el id, dnifac y fechafac de todas las facturas.
            query.prepare("SELECT id, dnifac, fechafac FROM facturas")

            # Ejecutamos la consulta SQL.
            if query.exec():
                # Si la consulta se ejecuta correctamente, iteramos sobre los resultados.
                while query.next():
                    # Para cada registro de la consulta, agregamos los valores de cada campo en una lista.
                    fila = [query.value(i) for i in range(query.record().count())]
                    # Añadimos la fila con los datos a la lista de resultados.
                    listado.append(fila)

            # Devolvemos la lista con todas las facturas obtenidas de la base de datos.
            return listado
        except Exception as e:
            # Si ocurre un error en la ejecución de la consulta, lo capturamos y lo imprimimos.
            print("Error listando facturas en listadoFacturas - conexión", e)

    @staticmethod
    def bajaFactura(idFactura):
        """
        :param idFactura: El ID de la factura que se desea eliminar.
        :type idFactura: str

        :return: True si la factura fue eliminada correctamente, False si hubo algún error.
        :rtype: bool

        Método para dar de baja una factura de la base de datos. Si la factura no está asociada
        a ninguna venta, se elimina. Si está asociada a ventas, no se elimina y se muestra un mensaje de error.
        """
        try:
            # Creamos una consulta para comprobar si la factura está asociada a alguna venta.
            query1 = QtSql.QSqlQuery()
            query1.prepare("Select count(*) from ventas where facventa = :facventa")
            query1.bindValue(":facventa", str(idFactura))

            # Ejecutamos la consulta.
            if query1.exec() and query1.next() and query1.value(0) == 0:
                # Si la factura no está asociada a ninguna venta, procedemos a eliminarla.
                query = QtSql.QSqlQuery()
                query.prepare("DELETE FROM facturas WHERE id = :id")
                query.bindValue(":id", str(idFactura))

                # Ejecutamos la eliminación de la factura.
                if query.exec():
                    return True  # La factura fue eliminada exitosamente.
                else:
                    # Si hubo un error en la ejecución de la eliminación, mostramos el error.
                    error = query.lastError()
                    if error is not None:
                        print("Error en la ejecución de la consulta:", error.text())
                    return False  # La eliminación falló.
            else:
                # Si la factura está asociada a una venta, mostramos un mensaje de error.
                eventos.Eventos.crearMensajeError("Error baja factura",
                                                  "No se puede eliminar la factura porque tiene ventas asociadas")
        except Exception as e:
            # Si ocurre un error durante la ejecución de la función, lo capturamos y lo imprimimos.
            print("Error eliminando factura en bajaFactura - conexión:", e)
            return False

    @staticmethod
    def cargaOneFactura(idFactura):
        """
        :param idFactura: El ID de la factura que se desea cargar.
        :type idFactura: str

        :return: Una lista con los datos de la factura si la consulta es exitosa, o una lista vacía si no se encuentra la factura.
        :rtype: list

        Método para cargar los detalles de una factura de la base de datos según el ID. Si se encuentra la factura,
        devuelve los detalles en una lista. En caso de error o si no se encuentra la factura, retorna una lista vacía.
        """
        try:
            # Inicializamos la lista que almacenará los datos de la factura.
            registro = []

            # Preparamos la consulta SQL para obtener los detalles de la factura.
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas WHERE id = :id")
            query.bindValue(":id", idFactura)  # Vinculamos el parámetro idFactura a la consulta.

            # Ejecutamos la consulta.
            if query.exec():
                # Si la consulta se ejecuta correctamente, recorremos los resultados.
                while query.next():
                    # Añadimos los valores de cada columna en la fila actual a la lista 'registro'.
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))  # Guardamos cada valor de columna como string.

            # Retornamos la lista de resultados.
            return registro
        except Exception as e:
            # Si ocurre un error, lo capturamos y mostramos el mensaje de error.
            print("Error cargando factura en cargaOneFactura - conexión", e)
            return []  # Retornamos una lista vacía en caso de error.

    @staticmethod
    def altaVenta(registro):
        """
        :param registro: Lista con los valores necesarios para registrar una venta.
                        [facventa, codprop, agente]
        :type registro: list

        :return: True si la venta se inserta correctamente en la base de datos, False si hay algún error.
        :rtype: bool

        Método para insertar un nuevo registro de venta en la base de datos. Si la consulta es exitosa, retorna True.
        Si ocurre algún error, imprime un mensaje y retorna False.
        """
        try:
            # Preparamos la consulta SQL para insertar una nueva venta.
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO ventas (facventa, codprop, agente) VALUES (:facventa, :codprop, :agente)")

            # Vinculamos los valores de la venta con los parámetros de la consulta.
            query.bindValue(":facventa", str(registro[0]))  # ID de la factura
            query.bindValue(":codprop", str(registro[1]))  # Código de la propiedad
            query.bindValue(":agente", str(registro[2]))  # Agente asociado a la venta

            # Ejecutamos la consulta.
            if query.exec():
                return True
            else:
                # Si hay un error, mostramos el mensaje de error de la consulta.
                print("Error en la ejecución de la consulta:", query.lastError().text())
                return False
        except Exception as e:
            # Si ocurre una excepción, la capturamos y mostramos el mensaje de error.
            print("Error al dar de alta venta en conexión:", e)
            return False

    @staticmethod
    def listadoVentas(idFactura):
        """
        :param idFactura: ID de la factura para la cual se desean listar las ventas asociadas.
        :type idFactura: str

        :return: Una lista de ventas asociadas a la factura. Cada venta incluye información de la propiedad.
        :rtype: list

        Método para obtener el listado de ventas asociadas a una factura. Realiza una consulta SQL para obtener la información
        de las ventas junto con los detalles de la propiedad (dirección, municipio, tipo, precio de venta).
        """
        try:
            # Inicializamos una lista vacía para almacenar los resultados de la consulta.
            listado = []

            # Preparamos la consulta SQL que obtiene las ventas y la información de la propiedad asociada.
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT v.idven, v.codprop, p.dirprop, p.muniprop, p.tipoprop, "
                "p.precioventaprop FROM ventas AS v "
                "INNER JOIN propiedades AS p ON v.codprop = p.codigo "
                "WHERE v.facventa = :facventa"
            )

            # Vinculamos el valor de la factura al parámetro de la consulta SQL.
            query.bindValue(":facventa", str(idFactura))

            # Ejecutamos la consulta.
            if query.exec():
                # Si la consulta se ejecuta con éxito, recorremos los resultados.
                while query.next():
                    # Creamos una lista de resultados de la fila actual.
                    fila = [query.value(i) for i in range(query.record().count())]
                    # Añadimos la fila al listado de resultados.
                    listado.append(fila)

            # Retornamos el listado de resultados.
            return listado

        except Exception as e:
            # Si ocurre un error, imprimimos el mensaje de error.
            print("Error listando ventas en listadoVentas - conexión", e)
            return []

    @staticmethod
    def datosOneVenta(idVenta):
        """
        :param idVenta: ID de la venta de la cual se desean obtener los detalles.
        :type idVenta: str

        :return: Una lista con los detalles de la venta, incluyendo el agente, el código de la propiedad,
                 tipo de propiedad, precio de venta, municipio y dirección.
        :rtype: list

        Método para obtener los detalles de una venta específica, incluyendo la información de la propiedad asociada.
        Realiza una consulta SQL con un INNER JOIN entre las tablas `ventas` y `propiedades`.
        """
        try:
            # Inicializamos una lista vacía para almacenar los resultados.
            registro = []

            # Preparamos la consulta SQL que obtiene los detalles de la venta junto con la información de la propiedad.
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT v.agente, v.codprop, p.tipoprop, p.precioventaprop, "
                "p.muniprop, p.dirprop FROM ventas AS v "
                "INNER JOIN propiedades AS p ON v.codprop = p.codigo WHERE v.idven = :idventa"
            )

            # Vinculamos el valor de la venta al parámetro de la consulta SQL.
            query.bindValue(":idventa", str(idVenta))

            # Ejecutamos la consulta.
            if query.exec():
                # Si la consulta se ejecuta con éxito, recorremos los resultados.
                while query.next():
                    # Para cada fila, agregamos los valores de las columnas a la lista `registro`.
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())

            # Retornamos la lista con los detalles de la venta.
            return registro

        except Exception as e:
            # Si ocurre un error, imprimimos el mensaje de error.
            print("Error en datosOneVenta en conexión", e)
            return []

    @staticmethod
    def actualizaPropiedadVenta(codigoPropiedad):
        """
        :param codigoPropiedad: Código de la propiedad que se va a marcar como vendida.
        :type codigoPropiedad: str

        :return: True si la propiedad fue actualizada correctamente, False en caso de error.
        :rtype: bool

        Método para actualizar el estado de una propiedad, cambiando su estado a "Vendido" y registrando la fecha de baja.
        """
        try:
            # Inicializamos la consulta SQL.
            query = QtSql.QSqlQuery()

            # Preparamos la consulta para actualizar el estado de la propiedad a "Vendido" y establecer la fecha de baja.
            query.prepare(
                "UPDATE propiedades SET estadoprop = 'Vendido', bajaprop = :fechaBaja WHERE codigo = :codigo"
            )

            # Vinculamos el código de la propiedad y la fecha de baja (fecha actual) a los parámetros de la consulta.
            query.bindValue(":codigo", str(codigoPropiedad))
            query.bindValue(":fechaBaja", datetime.now().strftime("%d/%m/%Y"))  # Fecha en formato dd/mm/yyyy

            # Ejecutamos la consulta.
            if query.exec():
                return True  # Si la consulta se ejecuta con éxito, retornamos True.
            else:
                return False  # Si la consulta falla, retornamos False.

        except Exception as e:
            # Si ocurre un error, imprimimos el mensaje de error.
            print("Error al vender una Propiedad en conexion.", e)
            return False

    def bajaVenta(idVenta):
        """
        :param idVenta: ID de la venta que se va a eliminar.
        :type idVenta: str

        :return: True si la venta fue eliminada correctamente, False en caso de error.
        :rtype: bool

        Método para eliminar una venta de la base de datos.
        Realiza una consulta SQL para eliminar el registro de la venta con el ID especificado.
        """
        try:
            # Inicializamos la consulta SQL para eliminar una venta.
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM ventas WHERE idven = :idventa")

            # Vinculamos el valor del ID de la venta a eliminar.
            query.bindValue(":idventa", str(idVenta))

            # Ejecutamos la consulta SQL.
            if query.exec():
                return True  # Si la consulta se ejecuta con éxito, retornamos True.
            else:
                return False  # Si la consulta falla, retornamos False.

        except Exception as e:
            # Si ocurre un error, imprimimos el mensaje de error.
            print("Error al eliminar una venta en conexion.", e)
            return False

            return False

    @staticmethod
    def altaPropiedadVenta(codigoPropiedad):
        """
        Actualiza el estado de una propiedad a 'Disponible' y borra la fecha de baja.

        :param codigoPropiedad: Código de la propiedad que se va a actualizar.
        :type codigoPropiedad: str

        :return: True si la propiedad fue actualizada correctamente, False en caso de error.
        :rtype: bool
        """
        try:
            # Inicializamos la consulta SQL para actualizar la propiedad.
            query = QtSql.QSqlQuery()

            # Preparamos la consulta SQL con los valores a actualizar.
            query.prepare(
                "UPDATE propiedades SET estadoprop = 'Disponible', bajaprop = :fechaBaja WHERE codigo = :codigo"
            )

            # Vinculamos los valores: el código de la propiedad y la fecha de baja (vacía).
            query.bindValue(":codigo", str(codigoPropiedad))

            # Aquí asignamos None si queremos limpiar la fecha de baja.
            # `QtCore.QVariant()` no es adecuado para vaciar campos de fecha, ya que esto no se reconoce como una fecha nula.
            query.bindValue(":fechaBaja", None)

            # Ejecutamos la consulta SQL.
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            # Si ocurre un error, imprimimos el mensaje de error.
            print("Error al vender una Propiedad en conexion.", e)
            return False




