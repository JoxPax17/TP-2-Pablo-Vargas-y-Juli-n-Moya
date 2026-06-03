#Elaborado por Pablo Vargas y Julian Moya
#Fecha de creacion 23-05-26 6:00 pm
#Ultima modificacion 01-06-26
#Version: 3.14.5

#Definicion de funciones
import re
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import random

provinciasDonacion = { "1": ["San José Centro", "Clínica Marcial Fallas", "Hospital México", "Hospital San Juan de Dios"], #diccionario lugares de donacion
                       "2": ["Hospital Calderón Guardia", "Clínica Moravia", "Clínica Clorito Picado"],
                       "3": ["Hospital San Rafael de Alajuela", "Clínica Carlos Durán"],
                       "4": ["Hospital de Heredia", "Clínica Central de Heredia"],
                       "5": ["Hospital Tony Facio - Limón", "Clínica Batan"],
                       "6": ["Hospital Max Peralta - Cartago", "Clínica de Cartago"],
                       "7": ["Hospital de Puntarenas", "Clínica de Puntarenas"],
                       "8": ["Hospital de Liberia", "Hospital de La Anexión - Nicoya"],
                       "9": ["Hospital de Ciudad Neily", "Clínica Corredores"],}

compatibilidadSangre = {"O+":  "Puede donar a: O+, A+, B+, AB+.\nPuede recibir de: O+, O-.",
                        "O-":  "Puede donar a: todos los tipos (donador universal).\nPuede recibir de: O-.",
                        "A+":  "Puede donar a: A+, AB+.\nPuede recibir de: A+, A-, O+, O-.",
                        "A-":  "Puede donar a: A+, A-, AB+, AB-.\nPuede recibir de: A-, O-.",
                        "B+":  "Puede donar a: B+, AB+.\nPuede recibir de: B+, B-, O+, O-.",
                        "B-":  "Puede donar a: B+, B-, AB+, AB-.\nPuede recibir de: B-, O-.",
                        "AB+": "Puede donar a: AB+.\nPuede recibir de: todos los tipos (receptor universal).",
                        "AB-": "Puede donar a: AB+, AB-.\nPuede recibir de: AB-, A-, B-, O-.",}

tiposSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

justificacionesEliminacion = {
    1: "Enfermedades Infecciosas o Cronicas: Portador de VIH, Hepatitis B o C, sifilis, tuberculosis, diabetes insulinodependiente, o afecciones graves de corazon, rinon o pulmon.",
    2: "Conductas de Riesgo: Nueva pareja sexual o mas de una pareja en los ultimos 3 meses, o relaciones sexuales por dinero o drogas.",
    3: "Factores de Salud Fisica: Hemoglobina o hematocrito bajo o alto, presion arterial inestable, fiebre, o infecciones recientes.",
    4: "Procedimientos Medicos Recientes: Ha recibido transfusiones, trasplantes, cirugias mayores, tatuajes, piercing o endoscopias recientemente.",
    5: "Uso de Medicamentos: Consumo de farmacos inyectables sin receta o ciertos medicamentos restringidos.",
    6: "Estilo de Vida y Viajes: Uso de drogas recreativas, consumo de alcohol en las ultimas 24 horas, o viajes recientes a zonas endemicas de malaria o dengue.",
    7: "Situaciones Especificas: Embarazo, lactancia o menstruacion (se evalua cada caso individualmente).",}

nombresProvincia = {"1": "San Jose", "2": "Alajuela", "3": "Cartago", "4": "Heredia", "5": "Guanacaste", "6": "Puntarenas", "7": "Limon", "8": "San Jose (Naturalizados)",}

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

def esMayorDeEdad(fecha):
    """
    Funcionalidad: Verifica si la persona es mayor de edad (18 anos) comparando mes y anno exactos.
    Entrada: fecha (str) en formato DD/MM/AAAA
    Salida: True si es mayor de edad, False si no
    """
    partes = fecha.split("/")
    dd   = int(partes[0])
    mm   = int(partes[1])
    aaaa = int(partes[2])
    hoy  = datetime.date.today()        # trae la fecha actual del sistema (anno, mes, dia)
    annos = hoy.year - aaaa             # diferencia de annos entre hoy y el nacimiento
    if annos > 18:
        return True
    if annos == 18:
        if mm < hoy.month:              # ya paso el mes del cumpleanos este anno
            return True
        if mm == hoy.month and dd <= hoy.day:   # mismo mes, ya llego o paso el dia
            return True
    return False

def obtenerLugaresDonacion(cedula):
    """
    Funcionalidad: Extrae el primer digito de la cedula y retorna la lista de centros donde puede donar.
    Entrada: cedula (str) en formato #-####-####
    Salida: lista de strings con los lugares de donacion
    """
    codigoProvincia = cedula[0]     #el primer caracter de la cedula es el codigo de provincia
    if codigoProvincia in provinciasDonacion:
        return provinciasDonacion[codigoProvincia]
    return ["Lugar de donacion no identificado"]

def mensajePeso(peso):
    """
    Funcionalidad: Retorna el mensaje y color correspondiente segun el peso del donador (3 casos posibles).
    Entrada: peso (str o float)
    Salida: mensaje (str), color (str)
    """
    p = float(peso)
    if p <= 50:
        return "Usted debe pesar mas de 50 kgms para poder ser donador.", "red"
    if p < 120:
        return "Usted posee un peso adecuado, correcto para ser donador de sangre.", "green"
    return "Dado su sobre peso, no es posible donar sangre.", "red"

def generarDonador():
    """
    Funcionalidad: Genera los datos completos de un donador de forma aleatoria.
    Entrada: ninguna
    Salida: diccionario con todos los datos del donador generado
    """
    nombres   = ["Julian", "Pablo", "Jose", "Ana", "Luis", "Laura", "Diego", "Sofia",
                 "Andres", "Valeria", "Roberto", "Gabriela", "Fernando", "Isabella"]
    apellidos = ["Vargas", "Moya", "Aguilar", "Mora", "Jimenez", "Perez",
                 "Lopez", "Garcia", "Fernandez", "Castro", "Quesada", "Salas"]
    dominios  = ["gmail.com", "hotmail.com", "estudiantec.cr"]
    primerosDigitosTel = [2, 4, 6, 7, 8, 9]
    provincia = str(random.randint(1, 9))       # Cedula aleatoria valida
    parte2    = str(random.randint(1000, 9999))
    parte3    = str(random.randint(1000, 9999))
    cedula    = provincia + "-" + parte2 + "-" + parte3
    nombre    = nombres[random.randint(0, len(nombres) - 1)]    # Nombre completo aleatorio
    apellido1 = apellidos[random.randint(0, len(apellidos) - 1)]
    apellido2 = apellidos[random.randint(0, len(apellidos) - 1)]
    nombreCompleto = nombre + " " + apellido1 + " " + apellido2
    anno = random.randint(1950, 2010)   #Fecha de nacimiento entre 1950 y 2010 para tener variedad de edades
    mes  = random.randint(1, 12)
    dia  = random.randint(1, 28)        #puse 28 para evitar problemas con meses cortos como febrero
    if dia < 10:
        diaStr = "0" + str(dia)
    else:
        diaStr = str(dia)
    if mes < 10:
        mesStr = "0" + str(mes)
    else:
        mesStr = str(mes)
    fecha      = diaStr + "/" + mesStr + "/" + str(anno)
    tipoSangre = tiposSangre[random.randint(0, len(tiposSangre) - 1)]
    if random.randint(0, 1) == 1:
        sexo = "Masculino"
    else:
        sexo = "Femenino"
    peso     = round(random.randint(40, 130) + random.random(), 1)
    primero  = primerosDigitosTel[random.randint(0, len(primerosDigitosTel) - 1)]
    resto    = str(random.randint(1000000, 9999999))
    telefono = str(primero) + resto[0:3] + "-" + resto[3:7]
    dominio  = dominios[random.randint(0, len(dominios) - 1)]
    correo   = nombre.lower() + str(random.randint(10, 99)) + "@" + dominio
    donador  = {"cedula": cedula, "nombre": nombreCompleto, "fecha": fecha,
                "tipoSangre": tipoSangre, "sexo": sexo, "peso": peso,
                "telefono": telefono, "correo": correo}
    return donador

def generarDonadores(baseDatos):
    """
    Funcionalidad: Abre una ventana grafica que solicita la cantidad de donadores a generar,
                   los genera aleatoriamente, los agrega a la base de datos y realimenta al usuario.
    Entrada: baseDatos (lista de diccionarios)
    Salida: baseDatos actualizada con los nuevos donadores
    """
    resultado = {"bd": baseDatos}   #diccionario para poder modificar baseDatos desde la funcion interna
    ventanaGenerar = tk.Toplevel()
    ventanaGenerar.title("Generar Donadores")
    ventanaGenerar.resizable(False, False)
    marcoGenerar = tk.Frame(ventanaGenerar, padx=25, pady=20)
    marcoGenerar.pack()
    tk.Label(marcoGenerar, text="Generar Donadores", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=3, pady=(0, 12))
    tk.Label(marcoGenerar, text="Cantidad a generar", anchor="w", width=20).grid(
        row=1, column=0, sticky="w", pady=4)
    entryCantidad = tk.Entry(marcoGenerar, width=10)
    entryCantidad.grid(row=1, column=1, sticky="w", pady=4)
    tk.Label(marcoGenerar, text="Ej: 10  (minimo 1)", fg="gray").grid(
        row=1, column=2, sticky="w", padx=8)
    tk.Frame(marcoGenerar, height=1, bg="lightgray").grid(
        row=2, column=0, columnspan=3, sticky="ew", pady=8)
    labelEstado = tk.Label(marcoGenerar, text="", font=("Arial", 10), wraplength=380, justify="left")
    labelEstado.grid(row=3, column=0, columnspan=3, sticky="w", pady=(4, 0))

    def generar():
        """
        Funcionalidad: Valida la cantidad, genera los donadores y actualiza el estado en pantalla.
        Entrada: ninguna (lee entryCantidad)
        Salida: ninguna
        """
        cantidadStr = entryCantidad.get().strip()
        if cantidadStr == "":
            messagebox.showerror("Error", "Debe ingresar una cantidad.")
            entryCantidad.focus()
            return
        try:
            cantidad = int(cantidadStr)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un numero entero.")
            entryCantidad.focus()
            return
        if cantidad < 1:
            messagebox.showerror("Error", "La cantidad debe ser al menos 1.")
            entryCantidad.focus()
            return
        registrosAntes = len(resultado["bd"])
        for i in range(cantidad):   #genera y mete cada donador uno por uno
            resultado["bd"].append(generarDonador())
        registrosDespues = len(resultado["bd"])
        labelEstado.config(
            text="Proceso finalizado exitosamente.\n"
                 "Donadores generados: " + str(cantidad) + "\n"
                 "Registros antes:     " + str(registrosAntes) + "\n"
                 "Registros ahora:     " + str(registrosDespues),
            fg="green")
        entryCantidad.delete(0, tk.END)
        entryCantidad.focus()

    def regresarGenerar():
        """
        Funcionalidad: Cierra la ventana y devuelve el control al menu principal.
        Entrada: ninguna
        Salida: ninguna
        """
        ventanaGenerar.destroy()

    marcoBotonesGenerar = tk.Frame(marcoGenerar)
    marcoBotonesGenerar.grid(row=4, column=0, columnspan=3, pady=10)
    tk.Button(marcoBotonesGenerar, text="Generar", width=12, command=generar).pack(side="left", padx=6)
    tk.Button(marcoBotonesGenerar, text="Regresar", width=12, command=regresarGenerar).pack(side="left", padx=6)
    entryCantidad.focus()
    ventanaGenerar.wait_window()    #espera a que esta ventana se cierre antes de continuar con el codigo del menu principal
    return resultado["bd"]

def mostrarInfoDonador(cedula, fecha, tipoSangre, peso):
    """
    Funcionalidad: Abre una ventana secundaria con el analisis del donador recien registrado:
                   mayoria de edad, lugar de donacion, validacion de peso, compatibilidad
                   de sangre y recomendacion especial si es tipo A+ o A-.
    Entrada: cedula (str), fecha (str), tipoSangre (str), peso (str)
    Salida: ninguna
    """
    ventanaInfo = tk.Toplevel()     #Toplevel() abre una ventana secundaria SIN cerrar la principal
    ventanaInfo.title("Informacion del donador")
    ventanaInfo.resizable(False, False)
    marcoInfo = tk.Frame(ventanaInfo, padx=25, pady=20)     #contenedor con margenes internos
    marcoInfo.pack()
    tk.Label(marcoInfo, text="Analisis de su registro", font=("Arial", 13, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(0, 14))
    fila = 1    #variable contadora de fila, la voy sumando de a 1 para no escribir el numero a mano en cada grid()
    #Seccion de mayoria de edad
    tk.Label(marcoInfo, text="1. Edad:", font=("Arial", 10, "bold"), anchor="w").grid(
        row=fila, column=0, columnspan=2, sticky="w", pady=(4, 0))
    fila += 1
    if esMayorDeEdad(fecha):
        msgEdad   = "Dado su fecha de nacimiento usted ya puede ser donador."
        colorEdad = "green"
    else:
        msgEdad   = "Dado su fecha de nacimiento usted aun no puede ser donador."
        colorEdad = "red"
    tk.Label(marcoInfo, text=msgEdad, fg=colorEdad, wraplength=400, justify="left").grid(   #wraplength=400 hace salto de linea automatico si el texto es largo
        row=fila, column=0, columnspan=2, sticky="w", padx=10)
    fila += 1
    tk.Frame(marcoInfo, height=1, bg="lightgray").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=6)   #linea separadora gris
    fila += 1
    #Seccion de lugar de donacion
    tk.Label(marcoInfo, text="2. Lugar de donacion:", font=("Arial", 10, "bold"), anchor="w").grid(
        row=fila, column=0, columnspan=2, sticky="w", pady=(4, 0))
    fila += 1
    lugaresLista = obtenerLugaresDonacion(cedula)   #retorna la lista de centros segun la provincia
    lugaresTexto = ", ".join(lugaresLista)          #.join() une la lista en un solo string separado por ", "
    msgProvincia = ("Dado que usted nacio en la provincia de: " + cedula[0] + ", usted podria donar en: " + lugaresTexto + ".")
    tk.Label(marcoInfo, text=msgProvincia, wraplength=400, justify="left").grid(
        row=fila, column=0, columnspan=2, sticky="w", padx=10)
    fila += 1
    tk.Frame(marcoInfo, height=1, bg="lightgray").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=6)
    fila += 1
    #Seccion de validacion de peso
    tk.Label(marcoInfo, text="3. Validacion del peso:", font=("Arial", 10, "bold"), anchor="w").grid(
        row=fila, column=0, columnspan=2, sticky="w", pady=(4, 0))
    fila += 1
    msgPeso, colorPeso = mensajePeso(peso)  #la funcion retorna dos valores a la vez: el mensaje y el color
    tk.Label(marcoInfo, text=msgPeso, fg=colorPeso, wraplength=400, justify="left").grid(
        row=fila, column=0, columnspan=2, sticky="w", padx=10)
    fila += 1
    tk.Frame(marcoInfo, height=1, bg="lightgray").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=6)
    fila += 1
    #Seccion de compatibilidad de sangre
    tk.Label(marcoInfo, text="4. Su tipo de sangre " + tipoSangre + ":", font=("Arial", 10, "bold"), anchor="w").grid(
        row=fila, column=0, columnspan=2, sticky="w", pady=(4, 0))
    fila += 1
    if tipoSangre in compatibilidadSangre:
        msgSangre = compatibilidadSangre[tipoSangre]
    else:
        msgSangre = "Informacion no disponible para este tipo de sangre."
    tk.Label(marcoInfo, text=msgSangre, wraplength=400, justify="left").grid(
        row=fila, column=0, columnspan=2, sticky="w", padx=10)
    fila += 1
    #Seccion de recomendacion especial solo si es tipo A+ o A-
    if tipoSangre == "A+" or tipoSangre == "A-":
        tk.Frame(marcoInfo, height=1, bg="lightgray").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=6)
        fila += 1
        tk.Label(marcoInfo, text="5. Recomendacion especial:", font=("Arial", 10, "bold"), anchor="w").grid(
            row=fila, column=0, columnspan=2, sticky="w", pady=(4, 0))
        fila += 1
        msgVideo = ("Por tener sangre tipo " + tipoSangre + ", le recomendamos ver el video:\n"
                    "\"Particularidades de la sangre tipo A: Responde diferente al estres segun la ciencia\".")
        tk.Label(marcoInfo, text=msgVideo, fg="blue", wraplength=400, justify="left").grid(
            row=fila, column=0, columnspan=2, sticky="w", padx=10)
        fila += 1
    #Boton para cerrar esta ventana y volver al formulario principal
    tk.Frame(marcoInfo, height=1, bg="lightgray").grid(row=fila, column=0, columnspan=2, sticky="ew", pady=8)
    fila += 1
    tk.Button(marcoInfo, text="Regresar", width=12, command=ventanaInfo.destroy).grid(  #ventanaInfo.destroy cierra solo esta ventana secundaria, no la principal
        row=fila, column=0, columnspan=2, pady=4)

def eliminarDonador(baseDatos):
    """
    Funcionalidad: Abre una ventana que solicita la cedula del donador a eliminar.
                   Si no existe muestra un mensaje. Si existe muestra sus datos y
                   solicita una justificacion via combobox antes de confirmar.
                   El borrado es virtual: cambia el estado a 0 (inactivo).
    Entrada: baseDatos (lista de diccionarios)
    Salida: baseDatos actualizada
    """
    resultado = {"bd": baseDatos}   #diccionario para poder modificar baseDatos desde las funciones internas

    ventanaEliminar = tk.Toplevel()     #Toplevel() abre ventana secundaria sin cerrar la principal
    ventanaEliminar.title("Eliminar Donador")
    ventanaEliminar.resizable(False, False)
    marcoEliminar = tk.Frame(ventanaEliminar, padx=20, pady=15)
    marcoEliminar.pack()

    tk.Label(marcoEliminar, text="Eliminar Donador", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=3, pady=(0, 12))

    #Fila de cedula para buscar
    tk.Label(marcoEliminar, text="Cedula", anchor="w", width=18).grid(row=1, column=0, sticky="w", pady=4)
    entryCedulaElim = tk.Entry(marcoEliminar, width=20)
    entryCedulaElim.grid(row=1, column=1, sticky="w", pady=4)
    tk.Label(marcoEliminar, text="Ej: 1-2345-6789", fg="gray").grid(row=1, column=2, sticky="w", padx=8)
    tk.Button(marcoEliminar, text="Buscar", width=10,
              command=lambda: buscarParaEliminar()).grid(row=1, column=3, padx=8)    #lambda para poder llamar la funcion sin argumentos

    tk.Frame(marcoEliminar, height=2, bd=1, relief="sunken").grid(
        row=2, column=0, columnspan=4, sticky="ew", pady=8)

    #Marco donde aparece la info del donador y la justificacion despues de buscar
    marcoDetalle = tk.Frame(marcoEliminar)
    marcoDetalle.grid(row=3, column=0, columnspan=4, sticky="w")

    def buscarParaEliminar():
        """
        Funcionalidad: Valida la cedula, verifica que exista en la BD y muestra los datos
                       del donador junto con el combobox de justificacion.
        Entrada: ninguna (lee entryCedulaElim)
        Salida: ninguna
        """
        cedula = entryCedulaElim.get().strip()
        if validarCedula(cedula) == False:
            messagebox.showerror("Error", "Cedula invalida. Use el formato #-####-####")
            return
        #Buscar la cedula en la lista de diccionarios
        donadorEncontrado = None
        for donador in resultado["bd"]:
            if donador["cedula"] == cedula:
                donadorEncontrado = donador
                break   #break detiene el loop en cuanto encuentra la cedula
        if donadorEncontrado == None:
            messagebox.showinfo("No encontrado",
                "La persona con el numero de cedula: " + cedula +
                " no esta registrado en la base de datos del Banco de Sangre aun.")
            return
        mostrarDetalleEliminar(donadorEncontrado)

    def mostrarDetalleEliminar(donador):
        """
        Funcionalidad: Muestra los datos del donador encontrado y el combobox de justificacion.
        Entrada: donador (dict) con los datos del donador
        Salida: ninguna
        """
        for widget in marcoDetalle.winfo_children():    #limpia el marco antes de mostrar los nuevos datos
            widget.destroy()
        #Mostrar datos del donador en modo lectura
        tk.Label(marcoDetalle, text="Datos del donador:", font=("Arial", 10, "bold"), anchor="w").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(4, 2))
        tk.Label(marcoDetalle, text="Cedula   : " + donador["cedula"], anchor="w").grid(
            row=1, column=0, columnspan=2, sticky="w", padx=10)
        tk.Label(marcoDetalle, text="Nombre   : " + donador["nombre"], anchor="w").grid(
            row=2, column=0, columnspan=2, sticky="w", padx=10)
        tk.Label(marcoDetalle, text="Tipo sangre: " + donador["tipoSangre"], anchor="w").grid(
            row=3, column=0, columnspan=2, sticky="w", padx=10)
        tk.Frame(marcoDetalle, height=1, bg="lightgray").grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=6)
        #Combobox de justificacion con las 7 razones de GEMINI
        tk.Label(marcoDetalle, text="Justificacion:", anchor="w", width=18).grid(
            row=5, column=0, sticky="w", pady=4)
        listaJustificaciones = []
        for num in justificacionesEliminacion:                          #construye la lista de opciones del combobox
            listaJustificaciones.append(str(num) + ". " + justificacionesEliminacion[num][:60] + "...")    #muestra los primeros 60 caracteres para que quepa en el combobox
        comboJustificacion = ttk.Combobox(marcoDetalle, values=listaJustificaciones,
                                          state="readonly", width=55)   #state="readonly" para que solo pueda elegir de la lista
        comboJustificacion.grid(row=5, column=1, sticky="w", pady=4)
        tk.Frame(marcoDetalle, height=1, bg="lightgray").grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=8)
        #Botones de confirmar y regresar
        marcoBotonesElim = tk.Frame(marcoDetalle)
        marcoBotonesElim.grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(marcoBotonesElim, text="Confirmar", width=12,
                  command=lambda: confirmarEliminacion(donador, comboJustificacion)).pack(side="left", padx=6)  #lambda pasa el donador y el combobox como argumentos
        tk.Button(marcoBotonesElim, text="Regresar", width=12,
                  command=ventanaEliminar.destroy).pack(side="left", padx=6)

    def confirmarEliminacion(donador, comboJustificacion):
        """
        Funcionalidad: Verifica que se haya elegido una justificacion, pide confirmacion
                       y si el usuario acepta cambia el estado a 0 (borrado virtual).
                       Si rechaza muestra mensaje y se mantiene en la ventana.
        Entrada: donador (dict), comboJustificacion (widget Combobox)
        Salida: ninguna
        """
        seleccion = comboJustificacion.get().strip()
        if seleccion == "":
            messagebox.showerror("Error", "Debe seleccionar una justificacion para eliminar al donador.")
            return
        numJustificacion = int(seleccion[0])    #seleccion[0] es el primer caracter del string, que es el numero
        if not messagebox.askyesno("Confirmar", "Desea eliminar al donador " + donador["nombre"] + "?"):   #askyesno retorna True si confirma, False si no
            messagebox.showinfo("Sin cambios", "Donador NO eliminado.")
            return  #se mantiene en la misma ventana
        #Borrado virtual: se cambia el estado a 0 y se guarda la justificacion
        donador["estado"]        = 0                #0 = inactivo segun la estructura de la BD
        donador["justificacion"] = numJustificacion #se guarda el numero de 1 a 7
        #guardarBD(resultado["bd"])    #descomentar cuando tengan lista la funcion de archivos
        messagebox.showinfo("Exito", "Donador eliminado satisfactoriamente.")
        ventanaEliminar.destroy()   #cierra la ventana y regresa al menu principal

    entryCedulaElim.focus()
    ventanaEliminar.wait_window()   #espera a que esta ventana se cierre antes de continuar
    return resultado["bd"]

def insertarLugarDonacion():
    """
    Funcionalidad: Abre una ventana que permite insertar un nuevo lugar de donacion
                   para una provincia seleccionada. Antes de insertar verifica que
                   el lugar no este ya registrado en esa provincia.
                   Los datos se leen y modifican del diccionario global provinciasDonacion.
    Entrada: ninguna
    Salida: ninguna
    """
    #Nombres de provincia para mostrar en el combobox, ordenados segun el Registro Civil
    nombresProvincia = {
        "1": "San Jose",
        "2": "Alajuela",
        "3": "Cartago",
        "4": "Heredia",
        "5": "Guanacaste",
        "6": "Puntarenas",
        "7": "Limon",
        "8": "San Jose (Naturalizados)",
        "9": "Sin asignacion oficial",}

    ventanaLugar = tk.Toplevel()    #Toplevel() abre ventana secundaria sin cerrar la principal
    ventanaLugar.title("Insertar lugar de donacion")
    ventanaLugar.resizable(False, False)
    marcoLugar = tk.Frame(ventanaLugar, padx=20, pady=15)
    marcoLugar.pack()

    tk.Label(marcoLugar, text="Insertar Lugar de Donacion", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(0, 12))

    #Combobox de provincia, se llena con los nombres leidos del diccionario global
    tk.Label(marcoLugar, text="Provincia:", anchor="w", width=18).grid(row=1, column=0, sticky="w", pady=4)
    listaNombresProvincia = []
    for codigo in nombresProvincia:                                     #construye la lista de opciones del combobox
        listaNombresProvincia.append(codigo + " - " + nombresProvincia[codigo])
    comboProvincia = ttk.Combobox(marcoLugar, values=listaNombresProvincia,
                                  state="readonly", width=30)           #state="readonly" para que solo pueda elegir de la lista
    comboProvincia.grid(row=1, column=1, sticky="w", pady=4)

    tk.Frame(marcoLugar, height=1, bg="lightgray").grid(row=2, column=0, columnspan=2, sticky="ew", pady=8)

    #Label que muestra los lugares ya registrados para la provincia seleccionada
    tk.Label(marcoLugar, text="Lugares actuales:", anchor="w", font=("Arial", 9, "bold")).grid(
        row=3, column=0, sticky="nw", pady=4)
    labelLugares = tk.Label(marcoLugar, text="(seleccione una provincia)", fg="gray",
                            wraplength=300, justify="left", anchor="w")
    labelLugares.grid(row=3, column=1, sticky="w", pady=4)  #este label se actualiza cuando el usuario elige provincia

    #Area de texto para ingresar el nuevo lugar
    tk.Label(marcoLugar, text="Nuevo lugar:", anchor="w", width=18).grid(row=4, column=0, sticky="nw", pady=4)
    areaLugar = tk.Text(marcoLugar, width=35, height=3)     #Text es el area de texto de varias lineas, height=3 filas de alto
    areaLugar.grid(row=4, column=1, sticky="w", pady=4)
    tk.Label(marcoLugar, text="Ej: Hospital Mexico", fg="gray").grid(
        row=5, column=1, sticky="w", padx=2)

    def actualizarLugares(evento):
        """
        Funcionalidad: Actualiza el label de lugares actuales cuando el usuario cambia la provincia.
        Entrada: evento (objeto que genera el combobox al cambiar, requerido por tkinter)
        Salida: ninguna
        """
        seleccion = comboProvincia.get()
        if seleccion == "":
            return
        codigo = seleccion[0]   #el primer caracter del string seleccionado es el codigo de provincia
        if codigo in provinciasDonacion and len(provinciasDonacion[codigo]) > 0:
            textoLugares = ""
            for lugar in provinciasDonacion[codigo]:
                textoLugares = textoLugares + "- " + lugar + "\n"   #construye el texto con cada lugar en una linea
            labelLugares.config(text=textoLugares.strip(), fg="black")
        else:
            labelLugares.config(text="(No hay lugares registrados)", fg="gray")

    comboProvincia.bind("<<ComboboxSelected>>", actualizarLugares)  #bind conecta el evento de seleccion del combobox con la funcion actualizarLugares, <<ComboboxSelected>> es el nombre del evento que dispara tkinter cuando el usuario elige una opcion

    tk.Frame(marcoLugar, height=2, bd=1, relief="sunken").grid(
        row=6, column=0, columnspan=2, sticky="ew", pady=10)

    def insertarLugar():
        """
        Funcionalidad: Lee la provincia y el nuevo lugar, verifica que no este repetido
                       y lo agrega al diccionario global provinciasDonacion.
        Entrada: ninguna (lee comboProvincia y areaLugar)
        Salida: ninguna
        """
        seleccion = comboProvincia.get().strip()
        if seleccion == "":
            messagebox.showerror("Error", "Debe seleccionar una provincia.")
            return
        nuevoLugar = areaLugar.get("1.0", tk.END).strip()  #get("1.0", tk.END) lee todo el texto del area desde la linea 1 caracter 0 hasta el final
        if nuevoLugar == "":
            messagebox.showerror("Error", "Debe ingresar el nombre del nuevo lugar.")
            return
        codigo = seleccion[0]   #codigo de provincia (primer caracter del string seleccionado)
        #Verificar que el lugar no este ya registrado en esa provincia
        if codigo in provinciasDonacion:
            for lugarExistente in provinciasDonacion[codigo]:
                if lugarExistente.lower() == nuevoLugar.lower():    #.lower() compara sin importar mayusculas o minusculas
                    messagebox.showwarning("Duplicado",
                        "El lugar \"" + nuevoLugar + "\" ya esta registrado en esa provincia.")
                    return
        #Agregar el nuevo lugar a la lista de la provincia
        if codigo in provinciasDonacion:
            provinciasDonacion[codigo].append(nuevoLugar)   #.append() agrega el elemento al final de la lista
        else:
            provinciasDonacion[codigo] = [nuevoLugar]       #si la provincia no existe en el diccionario se crea con una lista nueva
        #guardarLugares(provinciasDonacion)    #descomentar cuando tengan lista la funcion de archivos
        messagebox.showinfo("Exito", "Lugar agregado correctamente a la provincia seleccionada.")
        areaLugar.delete("1.0", tk.END)     #limpia el area de texto despues de insertar
        actualizarLugares(None)             #actualiza el label de lugares actuales pasando None como evento porque no hay evento real

    #Botones
    marcoBotonesLugar = tk.Frame(marcoLugar)
    marcoBotonesLugar.grid(row=7, column=0, columnspan=2, pady=5)
    tk.Button(marcoBotonesLugar, text="Insertar", width=12, command=insertarLugar).pack(side="left", padx=6)    #command llama insertarLugar al hacer clic
    tk.Button(marcoBotonesLugar, text="Salir", width=12, command=ventanaLugar.destroy).pack(side="left", padx=6)    #Salir cierra la ventana y devuelve al menu inicial

def calcularEdad(fecha):
    """
    Funcionalidad: Calcula la edad en anos de una persona a partir de su fecha de nacimiento.
    Entrada: fecha (str) en formato DD/MM/AAAA
    Salida: edad en anos (int)
    """
    partes = fecha.split("/")
    dd   = int(partes[0])
    mm   = int(partes[1])
    aaaa = int(partes[2])
    hoy  = datetime.date.today()        #fecha actual del sistema
    edad = hoy.year - aaaa
    if mm > hoy.month:                  #todavia no ha cumplido anos este anno
        edad -= 1
    elif mm == hoy.month and dd > hoy.day:
        edad -= 1
    return edad

def generarPlantillaHTML(titulo, filas, columnas):
    """
    Funcionalidad: Genera el contenido HTML5 completo de un reporte de donadores.
    Entrada: titulo (str) titulo del reporte,
             filas (lista de listas) cada sublista es una fila de datos,
             columnas (lista de str) nombres de las columnas de la tabla
    Salida: string con el HTML completo
    """
    ahora = datetime.datetime.now()                 #datetime.datetime.now() trae fecha y hora actual del sistema
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S") #strftime formatea la fecha/hora como string con el patron indicad
    filasHTML = "" # para las filas de la tabla
    for fila in filas:
        filasHTML = filasHTML + "        <tr>\n"
        for celda in fila:
            filasHTML = filasHTML + "            <td>" + str(celda) + "</td>\n"
        filasHTML = filasHTML + "        </tr>\n"
      encabezadosHTML = ""
    for col in columnas:
        encabezadosHTML = encabezadosHTML + "            <th>" + col + "</th>\n" #para encabezadfos
    html = ("<!DOCTYPE html>\n"
            "<html lang=\"es\">\n"
            "<head>\n"
            "    <meta charset=\"utf-8\" />\n"
            "    <title>" + titulo + "</title>\n"
            "    <style>\n"
            "        body { font-family: Arial, sans-serif; margin: 30px; }\n"
            "        h1 { color: #8B0000; }\n"
            "        p { color: #555; }\n"
            "        table { border-collapse: collapse; width: 100%; margin-top: 20px; }\n"
            "        th { background-color: #8B0000; color: white; padding: 10px; text-align: left; }\n"
            "        td { padding: 8px 10px; border-bottom: 1px solid #ddd; }\n"
            "        tr:nth-child(even) { background-color: #f9f9f9; }\n"  #nth-child(even) colorea filas pares
            "    </style>\n"
            "</head>\n"
            "<body>\n"
            "    <h1>" + titulo + "</h1>\n"
            "    <p>Fecha y hora del sistema: " + fechaHora + "</p>\n"
            "    <table>\n"
            "        <thead>\n"
            "            <tr>\n"
            + encabezadosHTML +
            "            </tr>\n"
            "        </thead>\n"
            "        <tbody>\n"
            + filasHTML +
            "        </tbody>\n"
            "    </table>\n"
            "</body>\n"
            "</html>\n")
    return html

def guardarHTML(contenidoHTML, nombreArchivo):
    """
    Funcionalidad: Guarda el contenido HTML en un archivo en la misma carpeta del programa.
    Entrada: contenidoHTML (str), nombreArchivo (str) nombre del archivo sin extension
    Salida: ruta del archivo creado (str) o None si hubo error
    """
    try:
        ruta = nombreArchivo + ".html"
        archivo = open(ruta, "w", encoding="utf-8")     #se abre en modo "w" (write) para escribir, encoding utf-8 para las tildes
        archivo.write(contenidoHTML)
        archivo.close()
        return ruta
    except:
        return None

def reporteDonantePorProvincia(baseDatos):
    """
    Funcionalidad: Abre una ventana con un combobox de provincia. Al generar el reporte,
                   filtra los donantes activos de esa provincia (segun el primer digito de
                   la cedula), los ordena por nombre completo y genera un archivo HTML5.
    Entrada: baseDatos (lista de diccionarios)
    Salida: ninguna
    """
    ventanaReporte = tk.Toplevel()      #Toplevel() abre ventana secundaria sin cerrar la principal
    ventanaReporte.title("Reporte: Donantes por provincia")
    ventanaReporte.resizable(False, False)
    marcoReporte = tk.Frame(ventanaReporte, padx=20, pady=15)
    marcoReporte.pack()
 
    tk.Label(marcoReporte, text="Donantes por Provincia", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(0, 12))
 
    #Combobox de provincia leido del diccionario global nombresProvincia
    tk.Label(marcoReporte, text="Provincia:", anchor="w", width=18).grid(row=1, column=0, sticky="w", pady=4)
    listaOpciones = []
    for codigo in nombresProvincia:
        listaOpciones.append(codigo + " - " + nombresProvincia[codigo])
    comboProv = ttk.Combobox(marcoReporte, values=listaOpciones, state="readonly", width=28)    #state="readonly" para que solo pueda elegir de la lista
    comboProv.grid(row=1, column=1, sticky="w", pady=4)
 
    tk.Frame(marcoReporte, height=2, bd=1, relief="sunken").grid(
        row=2, column=0, columnspan=2, sticky="ew", pady=10)
 
    labelResultado = tk.Label(marcoReporte, text="", wraplength=380, justify="left")
    labelResultado.grid(row=3, column=0, columnspan=2, sticky="w", pady=4)
 
    def generarReporte():
        """
        Funcionalidad: Filtra los donantes activos de la provincia seleccionada,
                       los ordena por nombre y genera el HTML.
        Entrada: ninguna (lee comboProv)
        Salida: ninguna
        """
        seleccion = comboProv.get().strip()
        if seleccion == "":
            messagebox.showerror("Error", "Debe seleccionar una provincia.")
            return
        codigoProv = seleccion[0]   #primer caracter = codigo de provincia
 
        #Filtrar donantes activos de esa provincia
        donantes = []
        for d in baseDatos:
            if d.get("cedula", "")[0] == codigoProv and d.get("estado", 1) == 1:   #.get() con valor por defecto evita KeyError si el campo no existe
                donantes.append(d)
 
        #Ordenar por nombre completo usando bubble sort para no usar sorted()
        i = 0
        while i < len(donantes) - 1:
            j = 0
            while j < len(donantes) - 1 - i:
                if donantes[j]["nombre"] > donantes[j + 1]["nombre"]:   #comparacion de strings alfabetica
                    temp = donantes[j]
                    donantes[j] = donantes[j + 1]
                    donantes[j + 1] = temp
                j += 1
            i += 1
 
        #Construir filas para el HTML
        filas = []
        for d in donantes:
            filas.append([d["cedula"], d["nombre"], d["fecha"], d["telefono"], d["correo"]])
 
        columnas = ["Cedula", "Nombre Completo", "Fecha de Nacimiento", "Telefono", "Correo"]
        titulo   = "Donantes por provincia: " + nombresProvincia.get(codigoProv, codigoProv)
        html     = generarPlantillaHTML(titulo, filas, columnas)
        ruta     = guardarHTML(html, "donantes_provincia_" + codigoProv)
 
        if ruta != None:
            labelResultado.config(text="Reporte creado satisfactoriamente.\nArchivo: " + ruta, fg="green")
        else:
            labelResultado.config(text="Reporte no creado.", fg="red")
 
    #Botones
    marcoBotones = tk.Frame(marcoReporte)
    marcoBotones.grid(row=4, column=0, columnspan=2, pady=8)
    tk.Button(marcoBotones, text="Generar reporte", width=16, command=generarReporte).pack(side="left", padx=6)     #command llama generarReporte al hacer clic
    tk.Button(marcoBotones, text="Regresar", width=12, command=ventanaReporte.destroy).pack(side="left", padx=6)    #cierra esta ventana y vuelve al submenu de reportes
 
def reportePorRangoEdad(baseDatos):
    """
    Funcionalidad: Abre una ventana con dos cajas de texto para edad inicial y final.
                   La segunda caja se activa solo si la primera tiene un valor valido.
                   Filtra donantes activos dentro del rango (18-65 anos) y genera HTML5.
    Entrada: baseDatos (lista de diccionarios)
    Salida: ninguna
    """
    ventanaReporte = tk.Toplevel()
    ventanaReporte.title("Reporte: Por rango de edad")
    ventanaReporte.resizable(False, False)
    marcoReporte = tk.Frame(ventanaReporte, padx=20, pady=15)
    marcoReporte.pack()
 
    tk.Label(marcoReporte, text="Reporte por Rango de Edad", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=3, pady=(0, 12))
 
    #Edad inicial
    tk.Label(marcoReporte, text="Edad inicial:", anchor="w", width=14).grid(row=1, column=0, sticky="w", pady=4)
    entryEdadInicial = tk.Entry(marcoReporte, width=8)
    entryEdadInicial.grid(row=1, column=1, sticky="w", pady=4)
    tk.Label(marcoReporte, text="(18 a 65)", fg="gray").grid(row=1, column=2, sticky="w", padx=6)
 
    #Edad final, empieza deshabilitada hasta que la inicial sea valida
    tk.Label(marcoReporte, text="Edad final:", anchor="w", width=14).grid(row=2, column=0, sticky="w", pady=4)
    entryEdadFinal = tk.Entry(marcoReporte, width=8, state="disabled")  #state="disabled" deshabilita el campo
    entryEdadFinal.grid(row=2, column=1, sticky="w", pady=4)
    tk.Label(marcoReporte, text="(18 a 65)", fg="gray").grid(row=2, column=2, sticky="w", padx=6)
 
    tk.Frame(marcoReporte, height=2, bd=1, relief="sunken").grid(
        row=3, column=0, columnspan=3, sticky="ew", pady=10)
 
    labelResultado = tk.Label(marcoReporte, text="", wraplength=380, justify="left")
    labelResultado.grid(row=4, column=0, columnspan=3, sticky="w", pady=4)
 
    def validarEdadInicial(evento):
        """
        Funcionalidad: Se ejecuta cada vez que el usuario sale del campo edad inicial.
                       Si el valor es valido habilita la caja de edad final.
        Entrada: evento (requerido por tkinter para el bind)
        Salida: ninguna
        """
        texto = entryEdadInicial.get().strip()
        if re.match(r'^\d+$', texto): #verifica que solo tenga digitos
            edad = int(texto)
            if edad >= 18 and edad <= 65:
                entryEdadFinal.config(state="normal") #state="normal" habilita el campo
                entryEdadFinal.focus()
                return
        entryEdadFinal.config(state="disabled") #si no es valido se deshabilita de nuevo
        entryEdadFinal.delete(0, tk.END)
 
    entryEdadInicial.bind("<FocusOut>", validarEdadInicial) #FocusOut usa la funcion cuando el usuario sale del campo
def reportePorTipoSangreProvincia(baseDatos):
    """
    Funcionalidad: Abre una ventana con un combobox de tipo de sangre y otro de provincia. Al generar el reporte, filtra los donantes activos que coincidan con ambos criterios y genera un archivo HTML5.
    Entrada: baseDatos (lista de diccionarios)
    Salida: ninguna
    """
    ventanaReporte = tk.Toplevel() #Toplevel() abre ventana secundaria sin cerrar la principal
    ventanaReporte.title("Reporte: Por tipo de sangre y provincia")
    ventanaReporte.resizable(False, False)
    marcoReporte = tk.Frame(ventanaReporte, padx=20, pady=15)
    marcoReporte.pack()

    tk.Label(marcoReporte, text="Por Tipo de Sangre y Provincia",font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 12))

    #Tipo de sangre leido desde la tupla global tiposSangre
    tk.Label(marcoReporte, text="Tipo de sangre:", anchor="w", width=18).grid(row=1, column=0, sticky="w", pady=4)
    comboSangre = ttk.Combobox(marcoReporte, values=list(tiposSangre), state="readonly", width=10) #list() convierte la tupla en lista para el combobox
    comboSangre.grid(row=1, column=1, sticky="w", pady=4)

    #provincia leido del diccionario global nombresProvincia
    tk.Label(marcoReporte, text="Provincia:", anchor="w", width=18).grid(row=2, column=0, sticky="w", pady=4)
    listaOpciones = []
    for codigo in nombresProvincia:
        listaOpciones.append(codigo + " - " + nombresProvincia[codigo])
    comboProv = ttk.Combobox(marcoReporte, values=listaOpciones,state="readonly", width=28)
    comboProv.grid(row=2, column=1, sticky="w", pady=4)

    tk.Frame(marcoReporte, height=2, bd=1, relief="sunken").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

    labelResultado = tk.Label(marcoReporte, text="", wraplength=380, justify="left")
    labelResultado.grid(row=4, column=0, columnspan=2, sticky="w", pady=4)

    def generarReporte():
        """
        Funcionalidad: Valida que se hayan seleccionado ambos filtros, filtra los donantes activos por tipo de sangre y provincia, y genera el HTML.
        Entrada: ninguna (lee comboSangre y comboProv)
        Salida: ninguna
        """
        tipoSeleccionado = comboSangre.get().strip()
        seleccionProv = comboProv.get().strip()
        if tipoSeleccionado == "" or seleccionProv == "":
            messagebox.showerror("Error", "Debe seleccionar tipo de sangre y provincia.")
            return
        codigoProv = seleccionProv[0] #primer caracter del string = codigo de provincia
        donantes = []
        for d in baseDatos:
            if (d.get("cedula", "")[0] == codigoProv 
                    and d.get("estado", 1) == 1        #1 = activo segun la estructura de la BD
                    and d.get("tipoSangre", "") == tipoSeleccionado):
                donantes.append(d)
#Aqui hace las filas del HTML con los datos de los donantes filtrados
        filas = []
        for d in donantes:
            filas.append([d["cedula"], d["nombre"], d["fecha"],
                          d["telefono"], d["correo"]])
        columnas = ["Cedula", "Nombre Completo", "Fecha de Nacimiento", "Telefono", "Correo"]
        titulo = ("Donantes tipo " + tipoSeleccionado + " en "
                  + nombresProvincia.get(codigoProv, codigoProv)) #.get() por si el codigo no esta en el diccionario
        html = generarPlantillaHTML(titulo, filas, columnas)
        ruta = guardarHTML(html, "donantes_sangre_"
                           + tipoSeleccionado.replace("+", "pos").replace("-", "neg") #el nombre del archivo reemplaza + y - para evitar caracteres especiales
                           + "_prov" + codigoProv)
        if ruta != None:
            labelResultado.config(
                text="Reporte creado satisfactoriamente.\nArchivo: " + ruta, fg="green")
        else:
            labelResultado.config(text="Reporte no creado.", fg="red")
    marcoBotones = tk.Frame(marcoReporte)
    marcoBotones.grid(row=5, column=0, columnspan=2, pady=8)
    tk.Button(marcoBotones, text="Generar reporte", width=16,
              command=generarReporte).pack(side="left", padx=6) #command llama generarReporte al hacer clic
    tk.Button(marcoBotones, text="Regresar", width=12,
              command=ventanaReporte.destroy).pack(side="left", padx=6) #cierra ventana y vuelve al submenu

def reporteListaCompleta(baseDatos):
    """
    Funcionalidad: Genera automaticamente el reporte de todos los donantes activos al abrir la ventana, ordenados por provincia ascendentemente. Todos los 14 de junio se usa para mandar mensajes de agradecimiento.
    Entrada: baseDatos (lista de diccionarios)
    Salida: ninguna
    """
    ventanaReporte = tk.Toplevel()
    ventanaReporte.title("Reporte: Lista completa de donadores")
    ventanaReporte.resizable(False, False)
    marcoReporte = tk.Frame(ventanaReporte, padx=20, pady=15)
    marcoReporte.pack()
    tk.Label(marcoReporte, text="Lista Completa de Donadores",
             font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 12))
    labelResultado = tk.Label(marcoReporte, text="", wraplength=380, justify="left")
    labelResultado.grid(row=1, column=0, sticky="w", pady=4)

    def generarReporte():
        """
        Funcionalidad: Filtra todos los donantes activos, los ordena por provincia con bubble sort y genera el archivo HTML5.
        Entrada: ninguna
        Salida: ninguna
        """
        #Filtrar solo donantes activos
        donantes = []
        for d in baseDatos:
            if d.get("estado", 1) == 1:
                donantes.append(d)
        #Ordenar por provincia (primer digito de la cedula)
        i = 0
        while i < len(donantes) - 1:
            j = 0
            while j < len(donantes) - 1 - i:
                if donantes[j]["cedula"][0] > donantes[j + 1]["cedula"][0]: #comparacion de codigos de provincia
                    temp = donantes[j]
                    donantes[j] = donantes[j + 1]
                    donantes[j + 1] = temp
                j += 1
            i += 1
        filas = []
        for d in donantes:
            sexoTexto = "Masculino" if d.get("sexo", "Masculino") == "Masculino" else "Femenino"
            filas.append([d["cedula"], d["nombre"], d.get("tipoSangre", ""),
                          d["fecha"], d.get("peso", ""), sexoTexto,
                          d["telefono"], d["correo"]])
        columnas = ["Cedula", "Nombre Completo", "Tipo de Sangre",
                    "Fecha de Nacimiento", "Peso", "Sexo", "Telefono", "Correo"]
        html = generarPlantillaHTML("Lista Completa de Donadores", filas, columnas)
        ruta = guardarHTML(html, "lista_completa_donadores")
        if ruta != None:
            labelResultado.config(
                text="Reporte creado satisfactoriamente.\nArchivo: " + ruta, fg="green")
        else:
            labelResultado.config(text="Reporte no creado.", fg="red")
    generarReporte()
    #Solo boton de regresar porque el reporte se genera automaticamente
    marcoBotones = tk.Frame(marcoReporte)
    marcoBotones.grid(row=2, column=0, pady=8)
    tk.Button(marcoBotones, text="Regresar", width=12,
              command=ventanaReporte.destroy).pack() #cierra ventana y vuelve al submenu
def registrar():
    """
    Funcionalidad: Valida todos los campos del formulario y registra al donador si son correctos.
    Entrada: ninguna (lee los widgets globales)
    Salida: ninguna
    """
    cedula     = entryCedula.get().strip()      # .get() extrae el texto que el usuario escribio
    nombre     = entryNombre.get().strip()
    fecha      = entryFecha.get().strip()
    tipoSangre = comboSangre.get().strip()      # en el combobox .get() trae la opcion que el usuario selecciono
    sexo       = varSexo.get()                  # varSexo es una variable especial de tkinter, .get() trae el valor del radio button seleccionado (1 o 2)
    peso       = entryPeso.get().strip()
    telefono   = entryTelefono.get().strip()
    correo     = entryCorreo.get().strip()
    if cedula == "" or nombre == "" or fecha == "" or tipoSangre == "" or peso == "" or telefono == "" or correo == "":
        messagebox.showerror("Error", "Todos los campos son requeridos.")    # showerror muestra un popup rojo de error con el mensaje
        return
    if validarCedula(cedula) == False:
        messagebox.showerror("Error", "Cedula invalida. Use el formato #-####-####\nEl primer digito no puede ser 0.")
        entryCedula.focus()     # .focus() mueve el cursor al campo que tiene el error para que el usuario lo corrija directo
        return
    if validarNombre(nombre) == False:
        messagebox.showerror("Error", "Nombre invalido. Solo se permiten letras y espacios.")
        entryNombre.focus()
        return
    if validarFecha(fecha) == False:
        messagebox.showerror("Error", "Fecha invalida. Use el formato DD/MM/AAAA\nVerifique que el dia, mes y anno sean correctos.")
        entryFecha.focus()
        return
    if validarPeso(peso) == False:
        messagebox.showerror("Error", "Peso invalido. Debe ser mayor a 50 y menor a 120 kg.")
        entryPeso.focus()
        return
    if validarTelefono(telefono) == False:
        messagebox.showerror("Error", "Telefono invalido. Use el formato ####-####\nEl primer digito no puede ser 0, 1, 3 ni 5.")
        entryTelefono.focus()
        return
    if validarCorreo(correo) == False:
        messagebox.showerror("Error", "Correo invalido. Debe pertenecer a uno de los dominios:\ncostarricense.cr, racsa.go.cr, ccss.sa.cr, gmail.com")
        entryCorreo.focus()
        return
    if sexo == 1:
        textoSexo = "Masculino"
    else:
        textoSexo = "Femenino"
    mensaje = ("Donador registrado exitosamente:\n\n"
        "Cedula: " + cedula + "\n"
        "Nombre: " + nombre + "\n"
        "Fecha de nacimiento: " + fecha + "\n"
        "Tipo sangre: " + tipoSangre + "\n"
        "Sexo: " + textoSexo + "\n"
        "Peso: " + peso + " kg\n"
        "Telefono: " + telefono + "\n"
        "Correo: " + correo)
    messagebox.showinfo("Registro exitoso", mensaje)    #showinfo muestra un popup normal (sin icono de error)
    mostrarInfoDonador(cedula, fecha, tipoSangre, peso)
    limpiar()

def limpiar():
    """
    Funcionalidad: Limpia todos los campos del formulario y restablece los valores
    Entrada: ninguna
    Salida: ninguna
    """
    entryCedula.delete(0, tk.END)       #delete(0, tk.END) borra todo el texto del campo, desde el caracter 0 hasta el final
    entryNombre.delete(0, tk.END)
    entryFecha.delete(0, tk.END)
    comboSangre.set("")                 #en el combobox .set("") limpia la seleccion actual
    varSexo.set(1)                      #resetea el radio button a Masculino (valor 1)
    entryPeso.delete(0, tk.END)
    entryTelefono.delete(0, tk.END)
    entryCorreo.delete(0, tk.END)
    entryCedula.focus()                 #devuelve el cursor al primer campo

def regresar():
    """
    Funcionalidad: Cierra la ventana del formulario.
    Entrada: ninguna
    Salida: ninguna
    """
    ventana.destroy()   #destroy() cierra y destruye la ventana completamente

#construccion de la ventana principal
ventana = tk.Tk()                           #Tk() crea la ventana principal, siempre debe haber una sola
ventana.title("Insertar Donador")           #titulo que aparece en la barra de la ventana
ventana.resizable(False, False)             #False, False significa que no se puede cambiar el tamanno (ni ancho ni alto)
#marco principal
marco = tk.Frame(ventana, padx=20, pady=15) #Frame es un contenedor invisible para organizar los widgets adentro, padx/pady son los margenes internos
marco.pack()                                #pack() coloca el marco dentro de la ventana (lo hace visible)
#titulo del formulario
tk.Label(marco, text="Insertar Donador", font=("Arial", 14, "bold")).grid(  # Label es texto estatico, font define fuente/tamanno/estilo
    row=0, column=0, columnspan=3, pady=(0, 12))                            # grid lo posiciona en fila 0, columnspan=3 hace que ocupe 3 columnas, pady=(0,12) es margen abajo
#Fila de cedula
tk.Label(marco, text="Cedula", anchor="w", width=18).grid(row=1, column=0, sticky="w", pady=4)  # anchor="w" alinea el texto a la izquierda (west), sticky="w" hace lo mismo en el grid
entryCedula = tk.Entry(marco, width=20)     #Entry es la cajita donde el usuario escribe texto
entryCedula.grid(row=1, column=1, sticky="w", pady=4)  #grid(row, column) define en que celda de la cuadricula va el widget
tk.Label(marco, text="Ej: 1-2345-6789", fg="gray").grid(row=1, column=2, sticky="w", padx=8)   #fg="gray" es el color del texto (foreground)
#Fila de nombre
tk.Label(marco, text="Nombre Completo", anchor="w", width=18).grid(row=2, column=0, sticky="w", pady=4)
entryNombre = tk.Entry(marco, width=30)
entryNombre.grid(row=2, column=1, columnspan=2, sticky="w", pady=4)    #columnspan=2 hace que este entry ocupe dos columnas para que sea mas ancho
#Fila de fecha de nacimiento
tk.Label(marco, text="Fecha de nacimiento", anchor="w", width=18).grid(row=3, column=0, sticky="w", pady=4)
entryFecha = tk.Entry(marco, width=20)
entryFecha.grid(row=3, column=1, sticky="w", pady=4)
tk.Label(marco, text="Ej: 15/06/1990", fg="gray").grid(row=3, column=2, sticky="w", padx=8)
#Fila de tipo de sangre
listaTiposSangre = list(tiposSangre)        #se convierte la tupla a lista para usarla en el combobox
tk.Label(marco, text="Tipo de sangre", anchor="w", width=18).grid(row=4, column=0, sticky="w", pady=4)
comboSangre = ttk.Combobox(marco, values=listaTiposSangre, state="readonly", width=8)  # Combobox es el dropdown, state="readonly" impide que el usuario escriba a mano (solo puede elegir)
comboSangre.grid(row=4, column=1, sticky="w", pady=4)
tk.Label(marco, text="Con las opciones: O+, O-, A+, A-, B+, B-, AB+, AB-", fg="gray").grid(row=4, column=2, sticky="w", padx=8)
#Fila de indicar sexo
varSexo = tk.IntVar()   #IntVar es una variable especial de tkinter que guarda un entero y esta enlazada a los radio buttons
varSexo.set(1)          #se inicializa en 1 para que Masculino quede marcado por omision
tk.Label(marco, text="Sexo", anchor="w", width=18).grid(row=5, column=0, sticky="w", pady=4)
marcoSexo = tk.Frame(marco)     #Frame extra para agrupar los dos radio buttons juntos en la misma celda
marcoSexo.grid(row=5, column=1, sticky="w")
tk.Radiobutton(marcoSexo, text="Masculino", variable=varSexo, value=1).pack(anchor="w")    #Radiobutton es el circulo de seleccion, variable=varSexo los enlaza entre si para que solo uno pueda estar activo
tk.Radiobutton(marcoSexo, text="Femenino",  variable=varSexo, value=2).pack(anchor="w")    #cuando se elige este, varSexo pasa a valer 2
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
tk.Frame(marco, height=2, bd=1, relief="sunken").grid(row=9, column=0, columnspan=3, sticky="ew", pady=10)  # Frame con height=2 y relief="sunken" crea una linea horizontal decorativa, sticky="ew" la estira de lado a lado (east-west)
#Fila de botones
marcoBotones = tk.Frame(marco)  #otro Frame para agrupar los tres botones en una sola fila
marcoBotones.grid(row=10, column=0, columnspan=3, pady=5)
tk.Button(marcoBotones, text="Registrar", width=12, command=registrar).pack(side="left", padx=6)    #command=registrar enlaza el boton a la funcion, se pasa sin parentesis porque no se llama aqui sino cuando se haga clic
tk.Button(marcoBotones, text="Limpiar",   width=12, command=limpiar).pack(side="left", padx=6)      #side="left" los acomoda de izquierda a derecha dentro del frame
tk.Button(marcoBotones, text="Regresar",  width=12, command=regresar).pack(side="left", padx=6)
#Foco inicial en el primer campo
entryCedula.focus()
ventana.mainloop()  # mainloop() arranca el "loop" de la ventana, sin esto la ventana se abre y se cierra inmediatamente, este loop espera eventos del usuario (clics, teclas, etc.)
