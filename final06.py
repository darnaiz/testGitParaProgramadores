from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re


def conexion():
    con = sqlite3.connect("zona_caba.db")
    return con


def crear_tabla(con):
    con = conexion()
    cursor = con.cursor()
    sql = "CREATE TABLE solicitud (id INTEGER PRIMARY KEY AUTOINCREMENT, sucursal TEXT, codigo INT,descripcion TEXT, fecha_ingreso TEXT, fecha_realizacion TEXT, dias_atraso INT);"
    cursor.execute(sql)
    con.commit()


try:
    con = conexion()
    #crear_tabla(con)
except:
    print("La Base de Datos se encuentra creada")


def alta(sucursal, codigo, descripcion, fecha_ingreso, fecha_realizacion, dias_atraso, tree):
    cadena = sucursal
    patron = "^[A-Z0-9a-záéíóú\s]*$"  # regex para el campo cadena 
    if re.match(patron, cadena):
        print(sucursal, codigo, descripcion, fecha_ingreso, fecha_realizacion, dias_atraso)
        con = conexion()
        cursor = con.cursor()
        data = (
            sucursal,
            codigo,
            descripcion,
            fecha_ingreso,
            fecha_realizacion,
            dias_atraso,
        )
        sql = "INSERT INTO solicitud (sucursal, codigo, descripcion, fecha_ingreso, fecha_realizacion, dias_atraso) VALUES(?, ?, ?, ?, ?, ?);"
        cursor.execute(sql, data)
        con.commit()
        print("Alta efectuada correctamente")
        actualizar_treeview(tree)
    else:
        print("Error en alta de la solicitud")


def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM solicitud ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[4], fila[6]))

def seleccionar(tree):
    id = str(entradaId.get())
    suc = str(entrada1.get())
    cod = str(entrada2.get())
    desc = str(entrada3.get())
    fing = str(entrada4.get())
    frea = str(entrada5.get())
    dias = str(entrada6.get())

    sql = "SELECT id, sucursal, codigo, descripcion, fecha_ingreso, fecha_realizacion, dias_atraso FROM solicitud WHERE "
    sql = sql + " 1 = 1"

    if id != "":
        sql = sql + " AND ID="+id
    if suc != "":
        sql = sql + " AND sucursal LIKE '%"+suc+"%'"
    if cod != "":
        sql = sql + " AND codigo="+cod
    if desc != "":
        sql = sql + " AND descripcion LIKE '%"+desc+"%'"
    if fing != "":
        sql = sql + " AND fecha_ingreso='"+fing+"'"
    if frea != "":
        sql = sql + " AND fecha_realizacion='"+frea+"'"
    if dias != "":
        sql = sql + " AND dias_atraso="+dias

    print("Ingresando a buscar: ", sql) 
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    resultado = datos.fetchall()
    limpiarTree(tree)
    for fila in resultado:
        print(fila)
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[4], fila[6]))

def limpiarTree(tree):
   for item in tree.get_children():
      tree.delete(item)

def limpiar(tree):
    entrada1.delete(0, END)
    entrada2.delete(0, END)
    entrada3.delete(0, END)
    entrada4.delete(0, END)
    entrada5.delete(0, END)
    entrada6.delete(0, END)
    entradaId.delete(0, END)
    
def mostrar(tree):
    valor = tree.selection()
    print(valor) 
    item = tree.item(valor)
    print(item) 
    print(item["text"])
    mi_id = item["text"]
    con = conexion()
    cursor = con.cursor()        
    sql = "SELECT * FROM solicitud WHERE id = "+str(int(mi_id))+";"
    datos = cursor.execute(sql)    
    resultado = datos.fetchall()
    
    entrada1.delete(0, END)
    entrada2.delete(0, END)
    entrada3.delete(0, END)
    entrada4.delete(0, END)
    entrada5.delete(0, END)
    entrada6.delete(0, END)
    entradaId.delete(0, END)
    
    
    for fila in resultado:
        print(fila)
        entrada1.insert(0, str(fila[1]))
        entrada2.insert(0, str(fila[2]))
        entrada3.insert(0, str(fila[3]))
        entrada4.insert(0, str(fila[4]))
        entrada5.insert(0, str(fila[5]))
        entrada6.insert(0, str(fila[6]))
        entradaId.insert(0, str(fila[0]))
        
def borrar(tree):
    valor = tree.selection()
    print(valor)  # ('I005',)
    item = tree.item(valor)
    print(item)  # {'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
    print(item["text"])
    mi_id = item["text"]

    con = conexion()
    cursor = con.cursor()
    # mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM solicitud WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)


def modificar(tree):  
    
    id = str(entradaId.get())
    suc = str(entrada1.get())
    cod = str(entrada2.get())
    desc = str(entrada3.get())
    fing = str(entrada4.get())
    frea = str(entrada5.get())
    dias = str(entrada6.get())

    print("Ingresando a modificar: ", id)    
    con=conexion()
    cursor=con.cursor()

    sql = "UPDATE solicitud SET sucursal='"+suc+"', codigo="+cod+", descripcion='"+desc+"', fecha_ingreso='"+fing+"', fecha_realizacion='"+frea+"', dias_atraso="+dias+" WHERE id="+id+";"
    print("sql: ", sql)
    
    cursor.execute(sql)
    con.commit()
    actualizar_treeview(tree)

# ##############################################
# Controladpr - VISTA
# ##############################################

root = Tk()
root.title("Solicitudes zona CABA")

titulo = Label(
    root, text="Ingrese sus datos", bg="#0373fc", fg="white", height=2, width=90
)
titulo.grid(row=0, column=0, columnspan=7, padx=1, pady=1, sticky=W + E)

sucursal = Label(root, text="Sucursal")
sucursal.grid(row=1, column=0, sticky=W)
codigo = Label(root, text="Codigo")
codigo.grid(row=2, column=0, sticky=W)
solicitud = Label(root, text="Descripcion")
solicitud.grid(row=3, column=0, sticky=W)
fecha_ingreso = Label(root, text="fecha_ingreso")
fecha_ingreso.grid(row=4, column=0, sticky=W)
fecha_realizacion = Label(root, text="fecha_realizacion")
fecha_realizacion.grid(row=5, column=0, sticky=W)
dias_atraso = Label(root, text="dias_atraso")
dias_atraso.grid(row=6, column=0, sticky=W)
id = Label(root, text="ID")
id.grid(row=1, column=2, sticky=W)


# Defino variables para tomar valores de campos de entrada
a_val, b_val, c_val, d_val, e_val, f_val, g_val, h_val = (
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar()
)
w_ancho = 20

entrada1 = Entry(root, textvariable=a_val, width=w_ancho)
entrada1.grid(row=1, column=1)
entrada2 = Entry(root, textvariable=b_val, width=w_ancho)
entrada2.grid(row=2, column=1)
entrada3 = Entry(root, textvariable=c_val, width=w_ancho)
entrada3.grid(row=3, column=1)
entrada4 = Entry(root, textvariable=d_val, width=w_ancho)
entrada4.grid(row=4, column=1)
entrada5 = Entry(root, textvariable=e_val, width=w_ancho)
entrada5.grid(row=5, column=1)
entrada6 = Entry(root, textvariable=f_val, width=w_ancho)
entrada6.grid(row=6, column=1)

entradaId = Entry(root, textvariable=g_val, width=w_ancho)
entradaId.grid(row=1, column=3)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.column("col5", width=200, minwidth=80)
tree.column("col6", width=200, minwidth=80)


tree.heading("#0", text="ID")
tree.heading("col1", text="Sucursal")
tree.heading("col2", text="Codigo")
tree.heading("col3", text="descripcion")
tree.heading("col4", text="fecha_ingreso")
tree.heading("col5", text="fecha_realizacion")
tree.heading("col6", text="dias_atraso")

tree.grid(row=10, column=0, columnspan=7)

boton_alta = Button(
    root,
    text="Alta",
    command=lambda: alta(
        a_val.get(),
        b_val.get(),
        c_val.get(),
        d_val.get(),
        e_val.get(),
        f_val.get(),
        tree,
    ),
)
boton_alta.grid(row=7, column=0)

boton_borrar = Button(root, text="Borrar", command=lambda: borrar(tree))
boton_borrar.grid(row=7, column=1)

boton_modificar = Button(root, text="Modificar", command=lambda: modificar(tree))
boton_modificar.grid(row=7, column=2)

boton_selecionar = Button(root, text="Buscar", command=lambda: seleccionar(tree))
boton_selecionar.grid(row=7, column=3)

boton_mostrar = Button(root, text="Mostrar", command=lambda: mostrar(tree))
boton_mostrar.grid(row=7, column=4)

boton_limpiar = Button(root, text="Limpiar campos", command=lambda: limpiar(tree))
boton_limpiar.grid(row=7, column=5)

boton_limpiar = Button(root, text="Limpiar grilla", command=lambda: limpiarTree(tree))
boton_limpiar.grid(row=7, column=6)


actualizar_treeview(tree)

root.mainloop()
