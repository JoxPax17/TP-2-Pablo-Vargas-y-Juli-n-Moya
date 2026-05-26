#Elaborado por Pablo Vargas y Julian Moya
#Fecha de creacion 23-05-26 6:00 pm
#Ultima modificacion 25-05-26
#Version: 3.14.4

#Definicion de funciones
import re

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
