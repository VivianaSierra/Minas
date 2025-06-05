import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Union import Union
from datetime import datetime

class RegistroIngresos:
    def __init__(self):
        try:
            self.base = tk.Tk()
            self.base.title("Registro de Entradas y Salidas")
            self.base.geometry("1300x600")

            # Frame para estadísticas
            frame_stats = tk.LabelFrame(self.base, text="Estadísticas", padx=5, pady=5)
            frame_stats.pack(fill="x", padx=10, pady=5)
            
            self.label_entradas = tk.Label(frame_stats, text="Entradas hoy: 0", font=("Arial", 10))
            self.label_entradas.pack(side="left", padx=10)
            
            self.label_pendientes = tk.Label(frame_stats, text="Salidas pendientes: 0", font=("Arial", 10))
            self.label_pendientes.pack(side="left", padx=10)

            # Frame para la tabla
            frame_tabla = tk.LabelFrame(self.base, text="Historial de Entradas y Salidas", padx=5, pady=5)
            frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

            # Crear tabla
            self.tree = ttk.Treeview(frame_tabla, columns=(
                "id", "cc", "nombres", "apellidos", "cargo",
                "hora_entrada", "hora_salida", "insumos", "observaciones"
            ), show="headings", height=20)
            
            # Definir columnas
            self.tree.column("id", anchor="center", width=50)
            self.tree.heading("id", text="ID")
            
            self.tree.column("cc", anchor="center", width=100)
            self.tree.heading("cc", text="Cédula")
            
            self.tree.column("nombres", anchor="w", width=150)
            self.tree.heading("nombres", text="Nombres")
            
            self.tree.column("apellidos", anchor="w", width=150)
            self.tree.heading("apellidos", text="Apellidos")
            
            self.tree.column("cargo", anchor="w", width=100)
            self.tree.heading("cargo", text="Cargo")
            
            self.tree.column("hora_entrada", anchor="center", width=150)
            self.tree.heading("hora_entrada", text="Hora Entrada")
            
            self.tree.column("hora_salida", anchor="center", width=150)
            self.tree.heading("hora_salida", text="Hora Salida")
            
            self.tree.column("insumos", anchor="w", width=200)
            self.tree.heading("insumos", text="Insumos")
            
            self.tree.column("observaciones", anchor="w", width=150)
            self.tree.heading("observaciones", text="Observaciones")

            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            self.tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Frame para botones
            frame_botones = tk.Frame(self.base)
            frame_botones.pack(pady=10)

            # Botón solo para actualizar
            tk.Button(frame_botones, text="Actualizar", font=("Arial", 12),
                     command=self.actualizar_registros).pack(side="left", padx=5)

            # Cargar datos iniciales
            self.actualizar_registros()

            self.base.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar la interfaz: {str(e)}")

    def actualizar_registros(self):
        """Actualiza la tabla con los registros más recientes"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtener registros usando la clase Union
            registros = Union.obtener_registros_completos()

            # Insertar registros en la tabla
            for registro in registros:
                self.tree.insert("", "end", values=(
                    registro['id'],
                    registro['cedula'],
                    registro['nombres'],
                    registro['apellidos'],
                    registro['cargo'],
                    registro['hora_entrada'],
                    registro['hora_salida'],
                    registro['insumos'],
                    registro['observaciones']
                ))

            # Actualizar estadísticas
            stats = Union.obtener_estadisticas()
            self.label_entradas.config(text=f"Entradas hoy: {stats['entradas_hoy']}")
            self.label_pendientes.config(text=f"Salidas pendientes: {stats['salidas_pendientes']}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar registros: {str(e)}")


RegistroIngresos()