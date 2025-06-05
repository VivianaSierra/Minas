from conexion import *

class Trabajadores:
    @staticmethod
    def ingresar_trabajador(nombres, apellidos, cc, cargo):
        """Registra un nuevo trabajador en la base de datos"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            sql = "INSERT INTO trabajador (nombres, apellidos, cc, cargo) VALUES (%s, %s, %s, %s)"
            valores = (nombres, apellidos, cc, cargo)
            cursor.execute(sql, valores)
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al ingresar trabajador: {str(e)}")
            return False
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def modificar_trabajador(id, nombres, apellidos, cc, cargo):
        """Actualiza los datos de un trabajador existente"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            
            # Primero verificamos si la cédula ha cambiado
            cursor.execute("SELECT cc FROM trabajador WHERE id = %s", (id,))
            cc_actual = cursor.fetchone()[0]
            
            if cc != cc_actual:
                # Verificamos si la cédula está siendo usada en la tabla ingreso
                cursor.execute("SELECT COUNT(*) FROM ingreso WHERE cc = %s", (cc_actual,))
                if cursor.fetchone()[0] > 0:
                    raise Exception("No se puede modificar la cédula porque tiene registros de entrada/salida asociados")
            
            # Si llegamos aquí, podemos actualizar
            sql = "UPDATE trabajador SET nombres=%s, apellidos=%s, cc=%s, cargo=%s WHERE id=%s"
            valores = (nombres, apellidos, cc, cargo, id)
            cursor.execute(sql, valores)
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al modificar trabajador: {str(e)}")
            raise  # Re-lanzamos la excepción para mostrarla en la interfaz
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_trabajador(id):
        """Elimina un trabajador si no tiene registros asociados"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            
            # Primero verificamos si tiene registros en ingreso
            cursor.execute("SELECT cc FROM trabajador WHERE id = %s", (id,))
            cc = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ingreso WHERE cc = %s", (cc,))
            if cursor.fetchone()[0] > 0:
                raise Exception("No se puede eliminar porque tiene registros de entrada/salida asociados")
            
            # Si llegamos aquí, podemos eliminar
            sql = "DELETE FROM trabajador WHERE id=%s"
            cursor.execute(sql, (id,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar trabajador: {str(e)}")
            raise  # Re-lanzamos la excepción para mostrarla en la interfaz
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def obtener_todos():
        """Obtiene todos los trabajadores registrados"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            sql = "SELECT id, nombres, apellidos, cc, cargo FROM trabajador"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener trabajadores: {str(e)}")
            return []
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()