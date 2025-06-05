import mysql.connector


class Conexion:

    def conectar():
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="2003",
                database="Proyecto1", 
                port="3306"
            )
            print("Conexión exitosa a la base de datos")
            return conexion
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None  

# Llamar al método para probar la conexión
Conexion.conectar()