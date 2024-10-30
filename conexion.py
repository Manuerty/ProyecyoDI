import os
from datetime import datetime

from PyQt6 import QtSql, QtWidgets, QtCore
from PyQt6 import QtGui

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

            # NO ENTRA EN EL IF
            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("error altaCliente", e)


    def listadoClientes(self):
        try:
            listado = []
            if var.historico == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE bajacli is NULL ORDER BY apelcli, nomecli ASC ")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            elif var.historico == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC ")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error listado en conexion", e)


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
                        query.bindValue(':apelcli', str(registro[2]))
                        query.bindValue(':nomecli', str(registro[3]))
                        query.bindValue(':emailcli', str(registro[4]))
                        query.bindValue(':movilcli', str(registro[5]))
                        query.bindValue(':dircli', str(registro[6]))
                        query.bindValue(':provcli', str(registro[7]))
                        query.bindValue(':municli', str(registro[8]))
                        if registro[9] == "":
                            query.bindValue(":bajacli", QtCore.QVariant())
                        else:
                            query.bindValue(":bajacli", str(registro[9]))
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

    def altaPropiedad(propiedad ):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO propiedades (altaprop, dirprop, provprop, muniprop, tipoprop, habprop"
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
            query.bindValue(":habprop", str(propiedad[5]))
            query.bindValue(":banoprop", str(propiedad[6]))
            query.bindValue(":superprop", str(propiedad[7]))
            query.bindValue(":precioventaprop", str(propiedad[8]))
            query.bindValue(":precioalquilerprop", str(propiedad[9]))
            query.bindValue(":cpprop", str(propiedad[10]))
            query.bindValue(":descriprop", str(propiedad[11]))
            query.bindValue(":tipoperprop", str(propiedad[12]))
            query.bindValue(":estadoprop", str(propiedad[13]))
            query.bindValue(":nomeprop", str(propiedad[14]))
            query.bindValue(":movilprop", str(propiedad[15]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error altaProp", e)
            return False