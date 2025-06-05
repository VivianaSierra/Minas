from conexion import *
from datetime import datetime

class Ingreso:
    @staticmethod
    def obtener_entrada_pendiente(cc):
        """Verifica si existe una entrada sin salida para la cédula"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            sql = """
                SELECT id FROM ingreso 
                WHERE cc = %s AND hora_de_salida IS NULL 
                AND DATE(hora_de_entrada) = CURDATE()
            """
            cursor.execute(sql, (cc,))
            resultado = cursor.fetchone()
            return resultado

        except Exception as e:
            print(f"Error al verificar entrada pendiente: {str(e)}")
            return None
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def registrar_entrada(cc, hora_de_entrada, insumos, observaciones):
        """Registra una nueva entrada"""
        print(f"Registrando entrada: CC={cc}, Hora de entrada={hora_de_entrada}, Insumos={insumos}, Observaciones={observaciones}")
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            sql = """
                INSERT INTO ingreso (cc, hora_de_entrada, insumos, observaciones, hora_de_salida)
                VALUES (%s, %s, %s, %s, NULL)
            """
            valores = (cc, hora_de_entrada, insumos, observaciones)
            cursor.execute(sql, valores)
            conexion.commit()
            return True

        except Exception as e:
            print(f"Error al registrar entrada: {str(e)}")
            return False
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def registrar_salida(id, hora_de_salida):
        """Registra la salida actualizando el registro existente"""
        try:
            if not id:
                raise ValueError("ID no válido")
                
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            sql = """
                UPDATE ingreso
                SET hora_de_salida = %s
                WHERE id = %s
            """
            valores = (hora_de_salida, id)
            cursor.execute(sql, valores)
            conexion.commit()
            return True

        except Exception as e:
            print(f"Error al registrar salida: {str(e)}")
            return False
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def obtener_todos():
        """Obtiene todos los registros de ingreso, incluyendo observaciones"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            sql = """
                SELECT id, cc, hora_de_entrada, hora_de_salida, insumos, observaciones
                FROM ingreso 
                ORDER BY hora_de_entrada DESC
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return resultados

        except Exception as e:
            print(f"Error al obtener registros: {str(e)}")
            return []
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()