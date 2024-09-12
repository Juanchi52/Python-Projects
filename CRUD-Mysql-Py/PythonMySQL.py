import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from Clientes import *
from Conexion import *

class FormularioClientes:
    global base
    base = None

    global textBoxId
    textBoxId = None

    global textBoxNombre
    textBoxNombre = None

    global textBoxApellido
    textBoxApellido = None

    global groupBox
    groupBox = None

    global tree
    tree = None

    global combo
    combo = None


def guardarRegistros():
    global textBoxNombre, textBoxApellido, combo

    try:
        if textBoxNombre is None or textBoxApellido is None or combo is None:
            print("Los widgets no están inicializados")
            return

        # Ingresamos los datos a la base de datos
        nombres = textBoxNombre.get()
        apellidos = textBoxApellido.get()
        sexo = combo.get()

        CClientes.ingresarClientes(nombres, apellidos, sexo)
        messagebox.showinfo("Información", "Los datos fueron guardados")

        actualizarTreeView()

        # Limpiamos los campos
        textBoxNombre.delete(0, END)
        textBoxApellido.delete(0, END)
    except ValueError as error:
        print("Error al ingresar los datos {}".format(error))


def Formulario():
    global textBoxId
    global textBoxNombre
    global textBoxApellido
    global combo
    global base
    global groupBox
    global tree

    try:
        base = Tk()
        base.geometry("1200x300")
        base.title("CRUD made In Python")

        # genero el cuadrado donde van a estar todos los datos, el primero cuadrado de la izquierda de mi app
        groupBox = LabelFrame(base, text="Datos del Personal", padx=5, pady=5,)
        groupBox.grid(row=0, column=0, padx=10, pady=10)

        # Genero los textbox de cada columna de los datos
        labelId = Label(groupBox, text='Id', width=13, font=('arial', 12)).grid(row=0, column=0)
        textBoxId = Entry(groupBox)
        textBoxId.grid(row=0, column=1)

        labelNombre = Label(groupBox, text='Nombres:', width=13, font=('arial', 12)).grid(row=1, column=0)
        textBoxNombre = Entry(groupBox)
        textBoxNombre.grid(row=1, column=1)

        labelApellido = Label(groupBox, text='Apellidos:', width=13, font=('arial', 12)).grid(row=2, column=0)
        textBoxApellido = Entry(groupBox)
        textBoxApellido.grid(row=2, column=1)

        labelSexo = Label(groupBox, text='Sexo:', width=13, font=('arial', 12)).grid(row=3, column=0)
        seleccionSexo = tk.StringVar()
        combo = ttk.Combobox(groupBox, values=["Masculino", "Femenino"], textvariable=seleccionSexo)
        combo.grid(row=3, column=1)
        seleccionSexo.set("Masculino")

        Button(groupBox, text='Guardar', width=10, command=guardarRegistros).grid(row=4, column=0)
        Button(groupBox, text='Modificar', width=10, command=modificarRegistros).grid(row=4, column=1)
        Button(groupBox, text='Eliminar', width=10,command=eliminarRegistros).grid(row=4, column=2)

        groupBox = LabelFrame(base, text='Lista del Personal', padx=5, pady=5,)
        groupBox.grid(row=0, column=1, padx=5, pady=5)

        # Creamos el Treeview
        # Configurar las Columnas
        tree = ttk.Treeview(groupBox, columns=('Id', 'Nombres', 'Apellidos', 'Sexo'), show='headings', height=5,)
        tree.column('# 1', anchor=CENTER)
        tree.heading('# 1', text='Id')
        tree.column('# 2', anchor=CENTER)
        tree.heading('# 2', text='Nombre')
        tree.column('# 3', anchor=CENTER)
        tree.heading('# 3', text='Apellido')
        tree.column('# 4', anchor=CENTER)
        tree.heading('# 4', text='Sexo')

        #Agregar los datos a la tabla y mostramos la tabla
        for row in CClientes.mostrarClientes():
            tree.insert("","end",values=row)

        tree.bind("<<TreeviewSelect>>",seleccionarRegistro)

        tree.pack()

        base.mainloop()

    except ValueError as error:
        print("Error al mostrar la interfaz, error: {}".format(error))

def actualizarTreeView():
    global tree

    try:
      #borramos todos los elementos del treeview
      tree.delete(*tree.get_children())
      #Obtenemos los nuevos datos
      datos = CClientes.mostrarClientes()
      #Insertamos los nuevos datos en el TreeView

      for row in CClientes.mostrarClientes():
        tree.insert("","end",values=row)
        
    except ValueError as error:
      print("Error al actualizar la tabla {}".format(error))

def seleccionarRegistro(event):
    try:
        #Obtenemos el id del elemento seleccionado
        itemSeleccionado = tree.focus()

        if itemSeleccionado:
            #Obtenemos los valores por columna
            values = tree.item(itemSeleccionado)["values"]

            #Establecemos los valores en los widget Entry
            textBoxId.delete(0,END)
            textBoxId.insert(0,values[0])
            textBoxNombre.delete(0,END)
            textBoxNombre.insert(0,values[1])
            textBoxApellido.delete(0,END)
            textBoxApellido.insert(0,values[2])
            combo.set(values[3])

    except ValueError as error:
        print("Error al seleccionar el registro {}".format(error))

def modificarRegistros():
    global textBoxId, textBoxNombre, textBoxApellido, combo, groupBox

    try:
        if textBoxId is None or textBoxNombre is None or textBoxApellido is None or combo is None:
            print("Los widgets no están inicializados")
            return

        # Ingresamos los datos a la base de datos
        idUsuario = textBoxId.get()
        nombres = textBoxNombre.get()
        apellidos = textBoxApellido.get()
        sexo = combo.get()

        CClientes.modificarClientes(idUsuario, nombres, apellidos, sexo)
        messagebox.showinfo("Información", "Los datos fueron actualizados")

        actualizarTreeView()

        # Limpiamos los campos
        textBoxId.delete(0, END)
        textBoxNombre.delete(0, END)
        textBoxApellido.delete(0, END)
    except ValueError as error:
        print("Error al modificar los datos {}".format(error))

def eliminarRegistros():
    global textBoxId, textBoxNombre, textBoxApellido

    try:
        if textBoxId is None :
            print("Los widgets no están inicializados")
            return

        # Ingresamos los datos a la base de datos
        idUsuario = textBoxId.get()

        CClientes.eliminarClientes(idUsuario)
        messagebox.showinfo("Información", "Los datos fueron eliminados")

        actualizarTreeView()

        # Limpiamos los campos
        textBoxId.delete(0, END)
        textBoxNombre.delete(0, END)
        textBoxApellido.delete(0, END)
    except ValueError as error:
        print("Error al eliminar los datos {}".format(error))


Formulario()
