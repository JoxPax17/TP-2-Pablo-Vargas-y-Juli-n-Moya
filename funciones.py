#Elaborado por Pablo Vargas y Julian Moya
#Fecha de creacion 23-05-26 6:00 pm
#Ultima modificacion 25-05-26
#Version: 3.14.4

#Definicion de funciones
import re
import tkinter as tk
from tkinter import ttk, messagebox

def validarCedula(cedula):
    """
    Funcionalidad: Valida que la cedula tenga el formato #-####-#### y que el primer digito no sea 0.
    Entrada: cedula (str)
    Salida: True si es valida, False si no
    """
    patron = r'^[1-9]-\d{4}-\d{4}$'
    if re.match(patron, cedula):
        return True
    return False

def validarFecha(fecha):
    """
    Funcionalidad: Valida que la fecha tenga el formato DD/MM/AAAA y que los valores sean coherentes.
    Entrada: fecha (str)
    Salida: True si es valida, False si no
    """
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(patron, fecha):
        return False
    partes = fecha.split("/")
    dd = int(partes[0])
    mm = int(partes[1])
    aaaa = int(partes[2])
    if mm < 1 or mm > 12:
        return False
    if dd < 1 or dd > 31:
        return False
    if aaaa < 1900 or aaaa > 2026:
        return False
    return True

def validarCorreo(correo):
    """
    Funcionalidad: Valida que el correo tenga un formato valido y pertenezca a uno de los dominios permitidos.
    Entrada: correo (str)
    Salida: True si es valido, False si no
    """
    patron = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\.){1,2}[a-zA-Z]{2,}$'
    dominiosValidos = ["costarricense.cr", "racsa.go.cr", "ccss.sa.cr", "gmail.com"]
    if not re.match(patron, correo):
        return False
    dominio = correo.split("@")[1]
    if dominio in dominiosValidos:
        return True
    return False

def validarTelefono(telefono):
    """
    Funcionalidad: Valida que el telefono tenga el formato ####-#### y que el primer digito no sea 0, 1, 3 ni 5.
    Entrada: telefono (str)
    Salida: True si es valido, False si no
    """
    patron = r'^[246789]\d{3}-\d{4}$'
    if re.match(patron, telefono):
        return True
    return False

def validarPeso(peso):
    """
    Funcionalidad: Valida que el peso sea mayor a 50 y menor a 120 kg.
    Entrada: peso (str o numero)
    Salida: True si es valido, False si no
    """
    try:
        p = float(peso)
        if p > 50 and p < 120:
            return True
        return False
    except:
        return False

def validarNombre(nombre):
    """
    Funcionalidad: Valida que el nombre no este vacio y solo contenga letras y espacios.
    Entrada: nombre (str)
    Salida: True si es valido, False si no
    """
    patron = r'^[A-Za-z ]+$'
    if re.match(patron, nombre.strip()) and nombre.strip() != "":
        return True
    return False

def registrar():
    """
    Funcionalidad: Valida todos los campos del formulario y registra al donador si son correctos.
    Entrada: ninguna (lee los widgets globales)
    Salida: ninguna
    """
    cedula = entryCedula.get().strip() # .get() extrae el texto que el usuario escribio
    nombre = entryNombre.get().strip()
    fecha = entryFecha.get().strip()
    tipoSangre = comboSangre.get().strip() # en el combobox .get() trae la opcion que el usuario selecciono
    sexo = varSexo.get() # varSexo es una variable especial de tkinter, .get() trae el valor del radio button seleccionado (1 o 2)
    peso = entryPeso.get().strip()
    telefono = entryTelefono.get().strip()
    correo = entryCorreo.get().strip()
    if cedula == "" or nombre == "" or fecha == "" or tipoSangre == "" or peso == "" or telefono == "" or correo == "":
        messagebox.showerror("Error", "Todos los campos son requeridos.")   # showerror muestra un popup rojo de error con el mensaje
        return
    if validarCedula(cedula)==False:
        messagebox.showerror("Error", "Cedula invalida. Use el formato #-####-####\nEl primer digito no puede ser 0.")
        entryCedula.focus() # .focus() mueve el cursor al campo que tiene el error para que el usuario lo corrija directo
        return
    if validarNombre(nombre)==False:
        messagebox.showerror("Error", "Nombre invalido. Solo se permiten letras y espacios.")
        entryNombre.focus()
        return
    if validarFecha(fecha)==False:
        messagebox.showerror("Error", "Fecha invalida. Use el formato DD/MM/AAAA\nVerifique que el dia, mes y anno sean correctos.")
        entryFecha.focus()
        return
    if validarPeso(peso)==False:
        messagebox.showerror("Error", "Peso invalido. Debe ser mayor a 50 y menor a 120 kg.")
        entryPeso.focus()
        return
    if validarTelefono(telefono)==False:
        messagebox.showerror("Error", "Telefono invalido. Use el formato ####-####\nEl primer digito no puede ser 0, 1, 3 ni 5.")
        entryTelefono.focus()
        return
    if validarCorreo(correo)==False:
        messagebox.showerror("Error", "Correo invalido. Debe pertenecer a uno de los dominios:\ncostarricense.cr, racsa.go.cr, ccss.sa.cr, gmail.com")
        entryCorreo.focus()
        return
    if sexo == 1:
        textoSexo= "Masculino"
    else:
        textoSexo= "Femenino"

    mensaje = ("Donador registrado exitosamente:\n\n"
        "Cedula: " + cedula + "\n"
        "Nombre: " + nombre + "\n"
        "Fecha de nacimiento: " + fecha + "\n"
        "Tipo sangre: " + tipoSangre + "\n"
        "Sexo: " + textoSexo + "\n"
        "Peso: " + peso + " kg\n"
        "Telefono: " + telefono + "\n"
        "Correo: " + correo)
    messagebox.showinfo("Registro exitoso", mensaje) #showinfo muestra un popup normal (sin icono de error)
    limpiar()
    
def limpiar():
    """
    Funcionalidad: Limpia todos los campos del formulario y restablece los valores
    Entrada: ninguna
    Salida: ninguna
    """
    entryCedula.delete(0, tk.END) #delete(0, tk.END) borra todo el texto del campo, desde el caracter 0 hasta el final
    entryNombre.delete(0, tk.END)
    entryFecha.delete(0, tk.END)
    comboSangre.set("") #en el combobox .set("") limpia la seleccion actual
    varSexo.set(1) #resetea el radio button a Masculino (valor 1)
    entryPeso.delete(0, tk.END)
    entryTelefono.delete(0, tk.END)
    entryCorreo.delete(0, tk.END)
    entryCedula.focus() #devuelve el cursor al primer campo

def regresar():
    """
    Funcionalidad: Cierra la ventana del formulario.
    Entrada: ninguna
    Salida: ninguna
    """
    ventana.destroy()   #destroy() cierra y destruye la ventana completamente
ventana = tk.Tk() #Tk() crea la ventana principal, siempre debe haber una sola
ventana.title("Insertar Donador") #titulo que aparece en la barra de la ventana
ventana.resizable(False, False) #False, False significa que no se puede cambiar el tamanno (ni ancho ni alto)
# esto es para hacer el marco principal
marco = tk.Frame(ventana, padx=20, pady=15) #Frame es un contenedor invisible para organizar los widgets adentro, padx/pady son los margenes internos
marco.pack() #pack() coloca el marco dentro de la ventana (lo hace visible)
#esto para hacer el titulo
tk.Label(marco, text="Insertar Donador", font=("Arial", 14, "bold")).grid(  # Label es texto estatico, font define fuente/tamanno/estilo
    row=0, column=0, columnspan=3, pady=(0, 12))                            # grid lo posiciona en fila 0, columnspan=3 hace que ocupe 3 columnas, pady=(0,12) es margen abajo
#Fila de cedula
tk.Label(marco, text="Cedula", anchor="w", width=18).grid(row=1, column=0, sticky="w", pady=4)  # anchor="w" alinea el texto a la izquierda (west), sticky="w" hace lo mismo en el grid
entryCedula = tk.Entry(marco, width=20) #Entry es la cajita donde el usuario escribe texto
entryCedula.grid(row=1, column=1, sticky="w", pady=4) #grid(row, column) define en que celda de la cuadricula va el widget
tk.Label(marco, text="Ej: 1-2345-6789", fg="gray").grid(row=1, column=2, sticky="w", padx=8) #fg="gray" es el color del texto (foreground)
#Fila de nombre
tk.Label(marco, text="Nombre Completo", anchor="w", width=18).grid(row=2, column=0, sticky="w", pady=4)
entryNombre = tk.Entry(marco, width=30)
entryNombre.grid(row=2, column=1, columnspan=2, sticky="w", pady=4) #columnspan=2 hace que este entry ocupe dos columnas para que sea mas ancho
#Fila de fecha de nacimiento
tk.Label(marco, text="Fecha de nacimiento", anchor="w", width=18).grid(row=3, column=0, sticky="w", pady=4)
entryFecha = tk.Entry(marco, width=20)
entryFecha.grid(row=3, column=1, sticky="w", pady=4)
tk.Label(marco, text="Ej: 15/06/1990", fg="gray").grid(row=3, column=2, sticky="w", padx=8)
#Fila de tipo de sangre
tiposSangre = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]      # lista con las opciones del combobox
tk.Label(marco, text="Tipo de sangre", anchor="w", width=18).grid(row=4, column=0, sticky="w", pady=4)
comboSangre = ttk.Combobox(marco, values=tiposSangre, state="readonly", width=8)   # Combobox es el dropdown, state="readonly" impide que el usuario escriba a mano (solo puede elegir)
comboSangre.grid(row=4, column=1, sticky="w", pady=4)
tk.Label(marco, text="Con las opciones: O+, O-, A+, A-, B+, B-, AB+, AB-", fg="gray").grid(row=4, column=2, sticky="w", padx=8)
#Fila de indicar sexo
varSexo = tk.IntVar() #IntVar es una variable especial de tkinter que guarda un entero y esta enlazada a los radio buttons
varSexo.set(1) #se inicializa en 1 para que Masculino quede marcado por omision
tk.Label(marco, text="Sexo", anchor="w", width=18).grid(row=5, column=0, sticky="w", pady=4)
marcoSexo = tk.Frame(marco) #Frame extra para agrupar los dos radio buttons juntos en la misma celda
marcoSexo.grid(row=5, column=1, sticky="w")
tk.Radiobutton(marcoSexo, text="Masculino", variable=varSexo, value=1).pack(anchor="w") #Radiobutton es el circulo de seleccion, variable=varSexo los enlaza entre si para que solo uno pueda estar activo
tk.Radiobutton(marcoSexo, text="Femenino",  variable=varSexo, value=2).pack(anchor="w") #cuando se elige este, varSexo pasa a valer 2
tk.Label(marco, text="Marcado por omision.", fg="gray").grid(row=5, column=2, sticky="nw", padx=8, pady=4)  #sticky="nw" ancla el texto arriba a la izquierda (north-west)
#Fila de peso
tk.Label(marco, text="Peso", anchor="w", width=18).grid(row=6, column=0, sticky="w", pady=4)
entryPeso = tk.Entry(marco, width=10)
entryPeso.grid(row=6, column=1, sticky="w", pady=4)
tk.Label(marco, text="En kg. Mayor a 50, menor a 120", fg="gray").grid(row=6, column=2, sticky="w", padx=8)
#Fila de telefono
tk.Label(marco, text="Telefono", anchor="w", width=18).grid(row=7, column=0, sticky="w", pady=4)
entryTelefono = tk.Entry(marco, width=20)
entryTelefono.grid(row=7, column=1, sticky="w", pady=4)
tk.Label(marco, text="Ej: 8765-4321", fg="gray").grid(row=7, column=2, sticky="w", padx=8)
#Fila de correo
tk.Label(marco, text="Correo", anchor="w", width=18).grid(row=8, column=0, sticky="w", pady=4)
entryCorreo = tk.Entry(marco, width=30)
entryCorreo.grid(row=8, column=1, columnspan=2, sticky="w", pady=4)
#Fila de separador
tk.Frame(marco, height=2, bd=1, relief="sunken").grid(row=9, column=0, columnspan=3, sticky="ew", pady=10) # Frame con height=2 y relief="sunken" crea una linea horizontal decorativasticky="ew" la estira de lado a lado (east-west)
#Fila de botones
marcoBotones = tk.Frame(marco) #otro Frame para agrupar los tres botones en una sola fila
marcoBotones.grid(row=10, column=0, columnspan=3, pady=5)
tk.Button(marcoBotones, text="Registrar", width=12, command=registrar).pack(side="left", padx=6) #command=registrar enlaza el boton a la funcion, se pasa sin parentesis porque no se llama aqui sino cuando se haga clic
tk.Button(marcoBotones, text="Limpiar",   width=12, command=limpiar).pack(side="left", padx=6) #side="left" los acomoda de izquierda a derecha dentro del frame
tk.Button(marcoBotones, text="Regresar",  width=12, command=regresar).pack(side="left", padx=6)
# Foco inicial en el primer campo
entryCedula.focus()
ventana.mainloop()  # mainloop() arranca el "loop" de la ventana, sin esto la ventana se abre y se cierra inmediatamente, este loop espera eventos del usuario (clics, teclas, etc.)
