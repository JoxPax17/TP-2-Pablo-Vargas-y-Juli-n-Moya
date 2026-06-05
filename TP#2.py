#Elaborado por Pablo Vargas y Julian Moya
#Fecha de creacion 23-05-26 6:00 pm
#Ultima modificacion 04-06-26 11:10
#Version: 3.14.3

import tkinter as tk
from tkinter import messagebox, ttk
import funciones

baseDatos = []
hayBaseDatos= False

def cargarDatos():
    """
    Funcionalidad: Intenta cargar la BD y los lugares desde disco al iniciar. Si existen archivos activa todos los botones; si no, solo 1, 2, 5 y 7.
    Entrada: ninguna
    Salida: ninguna
    """
    global baseDatos, hayBaseDatos
    bdCargada = funciones.cargarBD()        #retorna lista si existe el archivo, None si no
    if bdCargada != None:
        baseDatos = bdCargada
        hayBaseDatos = True
    lugaresCargados = funciones.cargarLugares()  #retorna dict si existe, None si no
    if lugaresCargados != None:
        funciones.provinciasDonacion = lugaresCargados   #actualiza el diccionario global del modulo

def actualizarBotones():
    """
    Funcionalidad: Habilita o deshabilita los botones del menu segun si hay BD cargada.
    Entrada: ninguna
    Salida: ninguna
    """
    if hayBaseDatos:
        estadoRestringido = "normal"
    else:
        estadoRestringido = "disabled"  #disabled bloquea el boton visualmente y no responde a clics
    btnActualizar.config(state=estadoRestringido)
    btnEliminar.config(state=estadoRestringido)
    btnReportes.config(state=estadoRestringido)

def accionInsertar():
    """
    Funcionalidad: Abre el formulario de insercion y actualiza la BD en RAM y en disco.
    Entrada: ninguna
    Salida: ninguna
    """
    global baseDatos, hayBaseDatos
    baseDatos = funciones.abrirVentanaInsertar(baseDatos)
    hayBaseDatos = len(baseDatos) > 0   #si se registro al menos un donador se activan los demas botones
    funciones.guardarBD(baseDatos)      #BD actualizada en disco
    funciones.guardarLugares(funciones.provinciasDonacion)
    actualizarBotones()

def accionGenerar():
    """
    Funcionalidad: Abre la ventana de generacion aleatoria de donadores.
    Entrada: ninguna
    Salida: ninguna
    """
    global baseDatos, hayBaseDatos
    baseDatos = funciones.generarDonadores(baseDatos)
    hayBaseDatos = len(baseDatos) > 0
    funciones.guardarBD(baseDatos)
    actualizarBotones()

def accionActualizar():
    """
    Funcionalidad: Abre la ventana de actualizacion de datos del donador.
    Entrada: ninguna
    Salida: ninguna
    """
    global baseDatos
    baseDatos = funciones.actualizarDonador(baseDatos)

def accionEliminar():
    """
    Funcionalidad: Abre la ventana de eliminacion (borrado virtual) del donador.
    Entrada: ninguna
    Salida: ninguna
    """
    global baseDatos
    baseDatos = funciones.eliminarDonador(baseDatos)

def accionInsertarLugar():
    """
    Funcionalidad: Abre la ventana para insertar un nuevo lugar de donacion por provincia.
    Entrada: ninguna
    Salida: ninguna
    """
    funciones.insertarLugarDonacion()
    funciones.guardarLugares(funciones.provinciasDonacion)  #Diccionario actualizado

def accionReportes():
    """
    Funcionalidad: Abre una ventana secundaria con los botones de todos los reportes disponibles.
    Entrada: ninguna
    Salida: ninguna
    """
    ventanaReportes = tk.Toplevel(ventana)
    ventanaReportes.title("Reportes")
    ventanaReportes.resizable(False, False)
    marcoRep = tk.Frame(ventanaReportes, padx=25, pady=20)
    marcoRep.pack()
    tk.Label(marcoRep, text="Reportes", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 12))
    opcionesReportes = [
        ("Donantes por provincia",       lambda: funciones.reporteDonantePorProvincia(baseDatos)),
        ("Por rango de edad",            lambda: funciones.reportePorRangoEdad(baseDatos)),
        ("Por tipo de sangre y provincia", lambda: funciones.reportePorTipoSangreProvincia(baseDatos)),
        ("Lista completa de donadores",  lambda: funciones.reporteListaCompleta(baseDatos)),
        ("Mujeres donantes O-",          lambda: funciones.reporteMujeresONegativo(baseDatos)),
        ("A quien puede donar",          lambda: funciones.reporteAQuienPuedeDona(baseDatos)),
        ("De quien puede recibir",       lambda: funciones.reporteDeQuienPuedeRecibir(baseDatos)),
        ("Donantes no activos",          lambda: funciones.reporteDonantesNoActivos(baseDatos)),
        ("Lugares de donacion",          lambda: funciones.reporteLugaresDonacion(baseDatos)),
    ]
    for i, (texto, comando) in enumerate(opcionesReportes):   #enumerate da el indice y el valor a la vez
        tk.Button(marcoRep, text=texto, width=30, command=comando).grid(row=i + 1, column=0, pady=3)
    tk.Button(marcoRep, text="Regresar", width=30,command=ventanaReportes.destroy).grid(row=len(opcionesReportes) + 1, column=0, pady=(10, 0))

def accionSalir():
    """
    Funcionalidad: Muestra el mensaje de despedida y cierra la aplicacion.
    Entrada: ninguna
    Salida: ninguna
    """
    messagebox.showinfo("Hasta pronto", "Donar sangre, es donar vida")
    ventana.destroy()   #destroy() cierra la ventana principal y termina el mainloop

ventana = tk.Tk()
ventana.title("Banco de Sangre - Menu Principal")
ventana.resizable(False, False)
marco = tk.Frame(ventana, padx=30, pady=25)
marco.pack()

tk.Label(marco, text="Banco de Sangre", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(0, 4))
tk.Label(marco, text="Sistema de Informacion", font=("Arial", 10)).grid(row=1, column=0, pady=(0, 14))
tk.Frame(marco, height=2, bd=1, relief="sunken").grid(row=2, column=0, sticky="ew", pady=(0, 10))

opcionesMenu = [("1. Insertar donador",accionInsertar),
    ("2. Generar donadores",accionGenerar),
    ("3. Actualizar datos del donador",accionActualizar),
    ("4. Eliminar donador",accionEliminar),
    ("5. Insertar lugar de donacion",accionInsertarLugar),
    ("6. Reportes",accionReportes),
    ("7. Salir",accionSalir),]

botonesMenu = []    #lista para poder acceder a cada boton despues y cambiar su estado
for i, (texto, comando) in enumerate(opcionesMenu):
    btn = tk.Button(marco, text=texto, width=32, anchor="w", padx=8, command=comando)
    btn.grid(row=i + 3, column=0, pady=3)
    botonesMenu.append(btn)

btnActualizar = botonesMenu[2]  #boton 3 
btnEliminar   = botonesMenu[3]  #boton 4 
btnReportes   = botonesMenu[5]  #boton 6 
cargarDatos()
actualizarBotones()
ventana.mainloop()  #arranca el loop de eventos; sin esto la ventana se cierra de inmediato
