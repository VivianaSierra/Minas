from conexion import *

class Inventario:
    @staticmethod
    def actualizar_insumo(insumo, cantidad):
        """Actualiza la cantidad de un insumo específico en el inventario"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            
            # Verificar si existe registro en inventario
            cursor.execute("SELECT COUNT(*) FROM inventario")
            if cursor.fetchone()[0] == 0:
                # Crear registro inicial con valores en cero
                cursor.execute("""
                    INSERT INTO inventario (n_Botas, n_Cascos, n_Picos, n_lamparas)
                    VALUES (0, 0, 0, 0)
                """)
                conexion.commit()

            # Verificar si hay suficiente inventario al decrementar
            if cantidad < 0:
                cursor.execute(f"SELECT n_{insumo} FROM inventario LIMIT 1")
                actual = cursor.fetchone()[0]
                if actual + cantidad < 0:
                    raise Exception(f"No hay suficiente inventario de {insumo}")

            # Actualizar cantidad del insumo
            sql = f"""
                UPDATE inventario 
                SET n_{insumo} = n_{insumo} + %s 
                WHERE id = (SELECT id FROM (SELECT id FROM inventario LIMIT 1) AS temp)
            """
            cursor.execute(sql, (cantidad,))
            conexion.commit()
            return True

        except Exception as e:
            print(f"Error al actualizar inventario: {str(e)}")
            raise  # Re-lanzamos la excepción para mostrarla en la interfaz
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def obtener_inventario():
        """Obtiene las cantidades actuales del inventario"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT n_Botas, n_Cascos, n_Picos, n_lamparas 
                FROM inventario LIMIT 1
            """)
            return cursor.fetchone()

        except Exception as e:
            print(f"Error al obtener inventario: {str(e)}")
            return None
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()