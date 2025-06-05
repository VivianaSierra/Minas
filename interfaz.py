import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Trabajadores import *

class Formulario:
    def __init__(self):
        try:
            self.base = tk.Tk()
            self.base.title("Formulario")
            self.base.geometry("1200x400")

            groupBox1 = tk.LabelFrame(self.base, text="Datos del personal", padx=15, pady=15)
            groupBox1.grid(row=0, column=0, padx=10, pady=10)

            # Se eliminó el campo Id de los datos personales

            tk.Label(groupBox1, text="Nombres:", width=10, font=("Arial", 12)).grid(row=0, column=0)
            self.texBoxNombre = tk.Entry(groupBox1, width=20, font=("Arial", 12))
            self.texBoxNombre.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(groupBox1, text="Apellidos:", width=10, font=("Arial", 12)).grid(row=1, column=0)
            self.texBoxApellidos = tk.Entry(groupBox1, width=20, font=("Arial", 12))
            self.texBoxApellidos.grid(row=1, column=1, padx=5, pady=5)

            tk.Label(groupBox1, text="CC:", width=10, font=("Arial", 12)).grid(row=2, column=0)
            self.texBoxcc = tk.Entry(groupBox1, width=20, font=("Arial", 12))
            self.texBoxcc.grid(row=2, column=1, padx=5, pady=5)

            tk.Label(groupBox1, text="Cargo:", width=10, font=("Arial", 12)).grid(row=3, column=0)
            self.seleccionCargo = tk.StringVar()
            self.combo = ttk.Combobox(groupBox1, values=["Malacatero", "Minero", "Administrativo"], textvariable=self.seleccionCargo, width=17, font=("Arial", 12))
            self.combo.grid(row=3, column=1)
            self.seleccionCargo.set("Seleccione un cargo")

            tk.Button(groupBox1, text="Guardar", width=10, font=("Arial", 12), command=self.Guardar_datos).grid(row=4, column=0)
            tk.Button(groupBox1, text="Modificar", width=10, font=("Arial", 12), command=self.Modificar_datos).grid(row=4, column=1)
            tk.Button(groupBox1, text="Eliminar", width=10, font=("Arial", 12), command=self.Eliminar_datos).grid(row=4, column=2)

            groupBox2 = tk.LabelFrame(self.base, text="Lista de personal", padx=5, pady=5)
            groupBox2.grid(row=0, column=1)

            self.tree = ttk.Treeview(groupBox2, columns=("id", "nombres", "apellidos", "cc", "cargo"), show="headings", height=15)
            self.tree.column("id", anchor="center", width=50)
            self.tree.heading("id", text="Id")
            self.tree.column("nombres", anchor="center", width=120)
            self.tree.heading("nombres", text="Nombres")
            self.tree.column("apellidos", anchor="center", width=120)
            self.tree.heading("apellidos", text="Apellidos")
            self.tree.column("cc", anchor="center", width=100)
            self.tree.heading("cc", text="CC")
            self.tree.column("cargo", anchor="center", width=120)
            self.tree.heading("cargo", text="Cargo")
            self.tree.pack()

            self.tree.bind("<<TreeviewSelect>>", self.cargar_datos_seleccion)

            self.mostrar_trabajadores()

            self.base.mainloop()

        except ValueError as e:
            messagebox.showerror("Error", "Por favor, ingrese un número válido.")

    def Guardar_datos(self):
        nombres = self.texBoxNombre.get()
        apellidos = self.texBoxApellidos.get()
        cc = self.texBoxcc.get()
        cargo = self.seleccionCargo.get()
        if nombres and apellidos and cc and cargo and cargo != "Seleccione un cargo":
            Trabajadores.ingresar_trabajador(nombres, apellidos, cc, cargo)
            messagebox.showinfo("Éxito", "Trabajador ingresado exitosamente")
            self.limpiar_campos()
            self.mostrar_trabajadores()
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

    def Modificar_datos(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para modificar.")
            return
        id = self.tree.item(selected, "values")[0]
        nombres = self.texBoxNombre.get()
        apellidos = self.texBoxApellidos.get()
        cc = self.texBoxcc.get()
        cargo = self.seleccionCargo.get()
        if nombres and apellidos and cc and cargo and cargo != "Seleccione un cargo":
            Trabajadores.modificar_trabajador(id, nombres, apellidos, cc, cargo)
            messagebox.showinfo("Éxito", "Trabajador modificado exitosamente")
            self.limpiar_campos()
            self.mostrar_trabajadores()
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

    def Eliminar_datos(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para eliminar.")
            return
        id = self.tree.item(selected, "values")[0]
        Trabajadores.eliminar_trabajador(id)
        messagebox.showinfo("Éxito", "Trabajador eliminado exitosamente")
        self.limpiar_campos()
        self.mostrar_trabajadores()

    def mostrar_trabajadores(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for trabajador in Trabajadores.obtener_todos():
            self.tree.insert("", "end", values=trabajador)

    def cargar_datos_seleccion(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.texBoxNombre.delete(0, tk.END)
            self.texBoxNombre.insert(0, values[1])
            self.texBoxApellidos.delete(0, tk.END)
            self.texBoxApellidos.insert(0, values[2])
            self.texBoxcc.delete(0, tk.END)
            self.texBoxcc.insert(0, values[3])
            self.seleccionCargo.set(values[4])

    def limpiar_campos(self):
        self.texBoxNombre.delete(0, tk.END)
        self.texBoxApellidos.delete(0, tk.END)
        self.texBoxcc.delete(0, tk.END)
        self.seleccionCargo.set("Seleccione un cargo")

Formulario()