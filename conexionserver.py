import mysql.connector
from mysql.connector import Error
import os
from PyQt6 import QtSql, QtWidgets

class ConexionServer():
    def crear_conexion(self):

        try:
            conexion = mysql.connector.connect(
            host='192.168.10.66', # Cambia esto a la IP de tu servidor user='dam', # Usuario creado
            user='dam',
            password='dam2425',
            database='bbdd'
            # Contraseña del usuario database='bbdd' # Nombre de la base de datos
            )
            if conexion.is_connected():
                pass
                #print("Conexión exitosa a la base de datos")
            return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return None

    @staticmethod
    def listaProv(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()

        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    def listadoClientes(self):
        try:
            conexion = ConexionServer().crear_conexion()
            listadoclientes = []
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC")
            resultados = cursor.fetchall()
            # Procesar cada fila de los resultados
            for fila in resultados:
                # Crear una lista con los valores de la fila
                listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes

            # Cerrar el cursor y la conexión si no los necesitas más
            cursor.close()
            conexion.close()
            # print(listadoclientes)
            return listadoclientes
        except Exception as e:
            print("error listado en conexion", e)

    def altaCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO clientes (dnicli, altacli, apelcli, nomecli, dircli, emailcli, movilcli, provcli, municli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, cliente)  # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    def datosOneCliente(dni):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT * FROM clientes WHERE dnicli = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (dni,))  # Pasar 'dni' como una tupla
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
            return registro

        except Exception as e:
            print("Error al obtener datos de un cliente:", e)
            return None  # Devolver None en caso de error



    def modificarCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de actualización
                query = """
                UPDATE clientes
                SET altacli = %s, apelcli = %s, nomecli = %s, dircli = %s, emailcli = %s, movilcli = %s, provcli = %s, municli = %s, bajacli = %s
                WHERE dnicli = %s
                """
                cursor.execute(query, cliente)  # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al modificar el cliente: {e}")


    def bajaCliente(fecha, dni):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                datos=(fecha, dni)
                cursor = conexion.cursor()
                query = '''UPDATE clientes SET bajacli = %s WHERE dnicli = %s'''
                cursor.execute(query, datos)  # Pasar 'dni' como una tupla
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al eliminar el cliente: {e}")
            return False