from conexion import Conexion

class Union:
    @staticmethod
    def obtener_registros_completos():
        """Obtiene todos los registros con datos completos del trabajador y su ingreso"""
        try:
            conexion = Conexion.conectar()
            if not conexion:
                raise Exception("No se pudo conectar a la base de datos")
            cursor = conexion.cursor()
            sql = """
                SELECT 
                    i.id,
                    i.cc,
                    t.nombres,
                    t.apellidos,
                    t.cargo,
                    i.hora_de_entrada,
                    i.hora_de_salida,
                    i.insumos,
                    i.observaciones
                FROM ingreso i
                INNER JOIN trabajador t ON i.cc = t.cc
                ORDER BY i.hora_de_entrada DESC
            """
            cursor.execute(sql)
            registros = cursor.fetchall()
            datos_formateados = []
            for registro in registros:
                # hora_de_entrada y hora_de_salida pueden ser datetime, timedelta o None
                def format_time(val):
                    if val is None:
                        return ""
                    # Si es timedelta (campo TIME), conviértelo a HH:MM:SS
                    if hasattr(val, "seconds"):
                        total_seconds = int(val.total_seconds())
                        horas = total_seconds // 3600
                        minutos = (total_seconds % 3600) // 60
                        segundos = total_seconds % 60
                        return f"{horas:02}:{minutos:02}:{segundos:02}"
                    return str(val)
                hora_entrada = format_time(registro[5])
                hora_salida = format_time(registro[6]) if registro[6] else "Pendiente"
                datos_formateados.append({
                    'id': registro[0],
                    'cedula': registro[1],
                    'nombres': registro[2],
                    'apellidos': registro[3],
                    'cargo': registro[4],
                    'hora_entrada': hora_entrada,
                    'hora_salida': hora_salida,
                    'insumos': registro[7] if registro[7] else "",
                    'observaciones': registro[8] if registro[8] else ""
                })
            return datos_formateados
        except Exception as e:
            print(f"Error al obtener registros completos: {str(e)}")
            return []
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de ingresos y salidas"""
        try:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            # Total de entradas del día
            sql_entradas = """
                SELECT COUNT(*) 
                FROM ingreso 
                WHERE DATE(hora_de_entrada) = CURDATE()
            """
            cursor.execute(sql_entradas)
            total_entradas = cursor.fetchone()[0]
            # Total de salidas pendientes
            sql_pendientes = """
                SELECT COUNT(*) 
                FROM ingreso 
                WHERE hora_de_salida IS NULL
            """
            cursor.execute(sql_pendientes)
            pendientes = cursor.fetchone()[0]
            return {
                'entradas_hoy': total_entradas,
                'salidas_pendientes': pendientes
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {str(e)}")
            return {
                'entradas_hoy': 0,
                'salidas_pendientes': 0
            }
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()