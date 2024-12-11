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
    def db_conexion(self):
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
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMuni(provincia):
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
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO  Vendedores(dniVendedor, nombreVendedor, movilVendedor, mailVendedor,delegacionVendedor,altaVendedor ) "
                "VALUES (:dniVen, :nomVen, :movilVen, :mailVen, :delegVen, :altaVen)")
            query.bindValue(":dniVen", str(nuevoVendedor[0]))
            query.bindValue(":nomVen", str(nuevoVendedor[1]))
            query.bindValue(":movilVen", str(nuevoVendedor[2]))
            query.bindValue(":mailVen", str(nuevoVendedor[3]))
            query.bindValue(":delegVen", str(nuevoVendedor[4]))
            query.bindValue(":altaVen", str(nuevoVendedor[5]))

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error altaCliente clase eventos", e)



    def listadoClientes(self):
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
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('SELECT * FROM Vendedores WHERE idVendedor = :idVend')
            query.bindValue(':idVend', str(id))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro

        except Exception as error:
            print("error en datosOneCliente ", error)

    def datosOnePropiedad(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('SELECT * FROM propiedades WHERE codigo = :codigo')
            query.bindValue(':codigo', str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro

        except Exception as error:
            print("error en datosOnePropiedad ", error)

    def modifCliente(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dnicli")
            query.bindValue(":dnicli", str(registro[0]))
            if query.exec():
                if query.next() and query.value(0)>0:
                    if query.exec():
                        query = QtSql.QSqlQuery()
                        query.prepare("UPDATE clientes SET altacli = :altacli , apelcli = :apelcli, nomecli = :nomecli, emailcli = :emailcli, movilcli = :movilcli, dircli = :dircli, provcli = :provcli, municli = :municli, bajacli = :bajacli WHERE dnicli = :dnicli")
                        query.bindValue(':dnicli', str(registro[0]))
                        query.bindValue(':altacli', str(registro[1]))
                        query.bindValue(':apelcli', str(registro[3]))
                        query.bindValue(':nomecli', str(registro[4]))
                        query.bindValue(':emailcli', str(registro[5]))
                        query.bindValue(':movilcli', str(registro[6]))
                        query.bindValue(':dircli', str(registro[7]))
                        query.bindValue(':provcli', str(registro[8]))
                        query.bindValue(':municli', str(registro[9]))
                        if registro[2] == "":
                            query.bindValue(":bajacli", QtCore.QVariant())
                        else:
                            query.bindValue(":bajacli", str(registro[2]))
                        if query.exec():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        except Exception as error:
            print("error modificar cliente", error)

    def modifVend(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from Vendedores where idVendedor = :idVendedor")
            query.bindValue(":idVendedor", str(registro[0]))
            if query.exec():
                if query.next() and query.value(0)>0:
                    if query.exec():
                        query = QtSql.QSqlQuery()
                        query.prepare("UPDATE Vendedores SET  nombreVendedor= :nombVend , altaVendedor = :altVen, movilVendedor = :movVend, mailVendedor = :emailVend, delegacionVendedor = :delegVend WHERE idVendedor = :idVend")
                        query.bindValue(':idVend', str(registro[0]))
                        query.bindValue(':nombVend', str(registro[2]))
                        query.bindValue(':altVen', str(registro[6]))
                        query.bindValue(':movVend', str(registro[3]))
                        query.bindValue(':emailVend', str(registro[4]))
                        query.bindValue(':delegVend', str(registro[5]))
                        if query.exec():
                            return True
                        else:
                            print("error1")
                            return False
                    else:
                        print("error2")
                        return False
                else:
                    print("error3")
                    return False
        except Exception as error:
            print("error modificar cliente", error)


    def modifPropiedad(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", str(registro[0]))
            if query.exec():
                if query.next() and query.value(0) > 0:
                    if query.exec():
                        query = QtSql.QSqlQuery()
                        query.prepare("UPDATE propiedades SET altaprop = :altaprop, bajaprop = :bajaprop, dirprop = :dirprop, provprop = :provprop, muniprop = :muniprop, tipoprop = :tipoprop, habprop = :habprop, banoprop = :banoprop, superprop = :superprop, precioventaprop = :precioventaprop, precioalquilerprop = :precioalquilerprop, cpprop = :cpprop, descriprop = :descriprop, tipoperprop = :tipoperprop, estadoprop = :estadoprop, nomeprop = :nomeprop, movilprop = :movilprop WHERE codigo = :codigo")
                        query.bindValue(':codigo', str(registro[0]))
                        query.bindValue(':altaprop', str(registro[1]))
                        query.bindValue(':dirprop', str(registro[3]))
                        query.bindValue(':provprop', str(registro[4]))
                        query.bindValue(':muniprop', str(registro[5]))
                        query.bindValue(':tipoprop', str(registro[6]))
                        query.bindValue(':habprop', int(registro[7]))
                        query.bindValue(':banoprop', int(registro[8]))
                        query.bindValue(':superprop', str(registro[9]))
                        query.bindValue(':precioventaprop', str(registro[10]))
                        query.bindValue(':precioalquilerprop', str(registro[11]))
                        query.bindValue(':cpprop', str(registro[12]))
                        query.bindValue(':descriprop', str(registro[13]))
                        query.bindValue(':tipoperprop', ",".join(registro[14]))
                        query.bindValue(':estadoprop', str(registro[15]))
                        query.bindValue(':nomeprop', str(registro[16]))
                        query.bindValue(':movilprop', str(registro[17]))
                        if registro[2] == "":
                            query.bindValue(":bajaprop", QtCore.QVariant())
                        else:
                            query.bindValue(":bajaprop", str(registro[2]))
                        if query.exec():
                            return True
        except Exception as error:
            print("error modificar propiedad", error)



    def bajaCliente(datos):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('UPDATE clientes SET bajacli = :bajacli WHERE dnicli = :dnicli')
            query.bindValue(':bajacli', datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(':dnicli', str(datos[1]))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error en bajaCliente ", error)

    def bajaVendedor(datos):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('UPDATE vendedores SET bajaVendedor = :bajaVendedor WHERE idVendedor = :idVend')
            query.bindValue(':bajaVendedor', datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(':idVend', str(datos[1]))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error en bajaCliente ", error)

    def checkUserInDb(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('SELECT * FROM clientes WHERE dnicli = :dnicli')
            query.bindValue(':dnicli', str(dni))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False
        except Exception as error:
            print("error en checkUserInDb ", error)

    def checkVendedorinDb(id):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('SELECT * FROM Vendedores WHERE idVendedor = :idVend')
            query.bindValue(':idVend', str(id))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False
        except Exception as error:
            print("error en checkVendedorinDb ", error)

    def checkDNIinDb(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('SELECT * FROM Vendedores WHERE dniVendedor = :dniVend')
            query.bindValue(':dniVend', str(dni))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False
        except Exception as error:
            print("error en checkVendedorinDb ", error)

    def altaTipoProp(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO tipopropiedad (tipo) VALUES (:tipo)")
            query.bindValue(":tipo", tipo)
            if query.exec():
                query = QtSql.QSqlQuery()
                query.prepare("SELECT tipo FROM tipopropiedad ORDER BY tipo ASC")
                if query.exec():
                    registro = []
                    while query.next():
                        registro.append(str(query.value(0)))
                    return registro
            else:
                return False
        except Exception as e:
            print("error altaTipoProp", e)

    def cargarTipoProp(self):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT tipo FROM tipopropiedad ORDER BY tipo ASC")
            if query.exec():
                registro = []
                while query.next():
                    registro.append(str(query.value(0)))
                return registro
        except Exception as e:
            print("error cargarTipoProp", e)

    def bajaTipoProp(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT COUNT(*) FROM tipopropiedad WHERE tipo = :tipo")
            query.bindValue(":tipo", tipo)
            if query.exec() and query.next() and query.value(0) > 0:
                query.prepare("DELETE FROM tipopropiedad WHERE tipo = :tipo")
                query.bindValue(":tipo", tipo)
                if query.exec():
                    eventos.Eventos.cargarTipoProp(tipo)
                    return True
                else:
                    eventos.Eventos.cargarTipoProp(tipo)
                    return False
            else:
                return False
        except Exception as e:
            print("error bajaTipoProp", e)
            return False

    @staticmethod
    def altaPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO propiedades (altaprop, dirprop, provprop, muniprop, tipoprop, habprop,"
                          "banoprop, superprop, precioventaprop, precioalquilerprop, cpprop,"
                          " descriprop, tipoperprop, estadoprop, nomeprop, movilprop ) "
                          "VALUES (:altaprop, :dirprop, :provprop, :muniprop, :tipoprop, :habprop,"
                          " :banoprop, :superprop, :precioventaprop, :precioalquilerprop, :cpprop,"
                          " :descriprop, :tipoperprop, :estadoprop, :nomeprop, :movilprop)")
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
            query.bindValue(":tipoperprop", ",".join((propiedad[12])))
            query.bindValue(":estadoprop", str(propiedad[13]))
            query.bindValue(":nomeprop", str(propiedad[14]))
            query.bindValue(":movilprop", str(propiedad[15]))
            if query.exec():
                return True
            else:
                print(query.lastError().text())
                return False
        except Exception as e:
            print("error altaProp", e)
            return False


    @staticmethod
    def bajaProp(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from Propiedades where codigo = :codigo")
            query.bindValue(":codigo", propiedad[0])
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:  # verificamos que solo nos devuelve un resultado a consulta, por tanto la propiedad existe.
                    query.prepare("update Propiedades set bajaprop =:baja, estadoprop =:estadoprop where codigo = :codigo ")
                    query.bindValue(":codigo", str(propiedad[0]))
                    query.bindValue(":baja", str(propiedad[2]))  # dejamos el segundo espacio del array para fecha de alta, y comprobar mas tarde que no sea posterior a fecha de baja
                    query.bindValue(":estadoprop", str(propiedad[3]))
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        except Exception as e:
            print("Error al dar de baja propiedad en conexión.", e)


    def listadoPropiedadesExport(self):
        listado = []
        query = QtSql.QSqlQuery()
        query.prepare(
            "SELECT * FROM PROPIEDADES where bajaprop is null or bajaprop is not null order by muniprop asc")
        if query.exec():
            while query.next():
                fila = [query.value(i) for i in range(query.record().count())]
                listado.append(fila)
        return listado

    def listadoClientesExport(self):
        listado = []
        query = QtSql.QSqlQuery()
        query.prepare(
            "SELECT * FROM CLIENTES where bajacli is null or bajacli is not null order by apelcli asc")
        if query.exec():
            while query.next():
                fila = [query.value(i) for i in range(query.record().count())]
                listado.append(fila)
        return listado

    def listadoVendedoresExport(self):
        listado = []
        query = QtSql.QSqlQuery()
        query.prepare(
            "SELECT * FROM vendedores where bajaVendedor is null or bajaVendedor is not null order by idVendedor asc")
        if query.exec():
            while query.next():
                fila = [query.value(i) for i in range(query.record().count())]
                listado.append(fila)
        return listado


