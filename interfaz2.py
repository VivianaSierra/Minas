import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk 
from Entrada import Ingreso
from inventario import Inventario
from datetime import datetime
from conexion import *

class Trabajador:
    def __init__(self):
        try:
            self.base = tk.Tk()
            self.base.title("Control de Entrada/Salida")
            self.base.geometry("1200x400")

            self.insumos_seleccionados = {
                "Pico": False,
                "Linterna": False,
                "Casco": False,
                "Botas": False
            }
            self.cedula_verificada = False

            # Grupo 1: Ingreso de cédula
            groupBox1 = tk.LabelFrame(self.base, text="Ingreso de cedula de ciudadania", padx=15, pady=15)
            groupBox1.grid(row=0, column=0, padx=10, pady=10)

            labelcc = tk.Label(groupBox1, text="CC:", width=10, font=("Arial", 12))
            labelcc.grid(row=0, column=0)
            self.texBoxcc = tk.Entry(groupBox1, width=20, font=("Arial", 12))
            self.texBoxcc.grid(row=0, column=1, padx=5, pady=5)

            btnVerificar = tk.Button(groupBox1, text="Verificar CC", font=("Arial", 12), command=self.verificar_cedula)
            btnVerificar.grid(row=0, column=2, padx=5, pady=5)

            # Grupo 2: Observaciones
            groupBox = tk.LabelFrame(self.base, text="Observaciones", padx=15, pady=15)
            groupBox.grid(row=1, column=0, padx=10, pady=10)

            labelObservaciones = tk.Label(groupBox, text="Observaciones sobre los Insumos:", font=("Arial", 12))
            labelObservaciones.grid(row=0, column=0, sticky="w")

            self.texBoxtext = tk.Text(groupBox, width=50, height=5, font=("Arial", 12))
            self.texBoxtext.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="w")

            # Botón Enviar
            btnEnviar = tk.Button(self.base, text="Registrar", font=("Arial", 12), command=self.enviar_datos)
            btnEnviar.grid(row=1, column=1, pady=10, padx=10, sticky="w")

            # Grupo 3: Insumos
            groupBoxButtons = tk.LabelFrame(self.base, text="Inventario", padx=15, pady=15)
            groupBoxButtons.grid(row=0, column=1, padx=10, pady=10)

            # Cargar imágenes
            try:
                img1 = ImageTk.PhotoImage(Image.open(r"C:\Users\sergi\OneDrive - UNIVERSIDAD DE CUNDINAMARCA\Escritorio\P_minas\Imagenes\pico.png").resize((50, 50)))
                img2 = ImageTk.PhotoImage(Image.open(r"C:\Users\sergi\OneDrive - UNIVERSIDAD DE CUNDINAMARCA\Escritorio\P_minas\Imagenes\linterna.png").resize((50, 50)))
                img3 = ImageTk.PhotoImage(Image.open(r"C:\Users\sergi\OneDrive - UNIVERSIDAD DE CUNDINAMARCA\Escritorio\P_minas\Imagenes\casco-de-construccion.png").resize((50, 50)))
                img4 = ImageTk.PhotoImage(Image.open(r"C:\Users\sergi\OneDrive - UNIVERSIDAD DE CUNDINAMARCA\Escritorio\P_minas\Imagenes\bota-de-senderismo.png").resize((50, 50)))
                self.img1, self.img2, self.img3, self.img4 = img1, img2, img3, img4
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar las imágenes: {e}")
                return

            # Crear botones con imágenes
            self.btn1 = tk.Button(groupBoxButtons, image=img1, text="Pico", compound="top", width=80, height=80,
                                command=lambda: self.toggle_insumo("Pico", self.btn1))
            self.btn1.grid(row=0, column=0, padx=10, pady=10)

            self.btn2 = tk.Button(groupBoxButtons, image=img2, text="Linterna", compound="top", width=80, height=80,
                                command=lambda: self.toggle_insumo("Linterna", self.btn2))
            self.btn2.grid(row=0, column=1, padx=10, pady=10)

            self.btn3 = tk.Button(groupBoxButtons, image=img3, text="Casco", compound="top", width=80, height=80,
                                command=lambda: self.toggle_insumo("Casco", self.btn3))
            self.btn3.grid(row=0, column=2, padx=10, pady=10)

            self.btn4 = tk.Button(groupBoxButtons, image=img4, text="Botas", compound="top", width=80, height=80,
                                command=lambda: self.toggle_insumo("Botas", self.btn4))
            self.btn4.grid(row=0, column=3, padx=10, pady=10)

            # Lista de botones para fácil acceso
            self.botones_insumos = [self.btn1, self.btn2, self.btn3, self.btn4]

            self.base.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al inicializar la interfaz: {e}")

    def activar_botones_insumos(self, estado):
        """Activa o desactiva los botones de insumos"""
        for boton in self.botones_insumos:
            boton.configure(state='normal' if estado else 'disabled')
            if not estado:
                boton.configure(bg='SystemButtonFace')
        
        if not estado:
            for insumo in self.insumos_seleccionados:
                self.insumos_seleccionados[insumo] = False

    def verificar_cedula(self):
        """Verifica si la cédula existe y su estado de entrada/salida"""
        try:
            cc = self.texBoxcc.get().strip()
            if not cc:
                messagebox.showwarning("Advertencia", "Por favor ingrese la cédula")
                self.cedula_verificada = False
                return

            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM trabajador WHERE cc = %s", (cc,))
            
            if cursor.fetchone()[0] > 0:
                entrada_pendiente = Ingreso.obtener_entrada_pendiente(cc)
                self.cedula_verificada = True
                
                if entrada_pendiente:
                    self.activar_botones_insumos(False)
                    messagebox.showinfo("Información", "El trabajador tiene una entrada pendiente. Solo puede registrar salida.")
                else:
                    self.activar_botones_insumos(True)
                    messagebox.showinfo("Éxito", "Cédula verificada correctamente. Puede seleccionar insumos.")
            else:
                self.cedula_verificada = False
                self.activar_botones_insumos(False)
                messagebox.showerror("Error", "La cédula no está registrada en el sistema")
                self.texBoxcc.delete(0, tk.END)

        except Exception as e:
            self.cedula_verificada = False
            messagebox.showerror("Error", f"Error al verificar cédula: {str(e)}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def toggle_insumo(self, insumo, boton):
        """Cambia el estado del insumo seleccionado"""
        if not self.cedula_verificada:
            messagebox.showwarning("Advertencia", "Primero debe verificar la cédula")
            return
            
        try:
            self.insumos_seleccionados[insumo] = not self.insumos_seleccionados[insumo]
            insumo_map = {
                "Botas": "Botas",
                "Casco": "Cascos",
                "Pico": "Picos",
                "Linterna": "lamparas"
            }
            
            if self.insumos_seleccionados[insumo]:
                boton.configure(bg='#87CEFA')
                Inventario.actualizar_insumo(insumo_map[insumo], 1)
            else:
                boton.configure(bg='SystemButtonFace')
                Inventario.actualizar_insumo(insumo_map[insumo], -1)
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar inventario: {str(e)}")

    def enviar_datos(self):
        """Registra la entrada o salida del trabajador"""
        try:
            if not self.cedula_verificada:
                messagebox.showwarning("Advertencia", "Primero debe verificar la cédula")
                return

            cc = self.texBoxcc.get().strip()
            hora_actual = datetime.now().strftime('%H:%M:%S')
            entrada_pendiente = Ingreso.obtener_entrada_pendiente(cc)

            if entrada_pendiente:
                if Ingreso.registrar_salida(entrada_pendiente[0], hora_actual):
                    messagebox.showinfo("Éxito", f"Salida registrada exitosamente a las {hora_actual}")
                    self.activar_botones_insumos(True)
            else:
                insumos_activos = [k for k, v in self.insumos_seleccionados.items() if v]
                if not insumos_activos:
                    messagebox.showwarning("Advertencia", "Debe seleccionar al menos un insumo")
                    return
                    
                insumos_str = ", ".join(insumos_activos)
                observaciones = self.texBoxtext.get("1.0", tk.END).strip()
                
                if Ingreso.registrar_entrada(cc, hora_actual, insumos_str, observaciones):
                    messagebox.showinfo("Éxito", f"Entrada registrada exitosamente a las {hora_actual}")
                    self.activar_botones_insumos(False)

            # Limpiar campos
            self.texBoxcc.delete(0, tk.END)
            self.texBoxtext.delete("1.0", tk.END)
            self.cedula_verificada = False

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar los datos: {str(e)}")

Trabajador()