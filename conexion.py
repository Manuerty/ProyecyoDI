import os
from PyQt6 import QtSql, QtWidgets, QtCore
from PyQt6 import QtGui

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
            query.bindValue(':bajacli', str(datos[0]))
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