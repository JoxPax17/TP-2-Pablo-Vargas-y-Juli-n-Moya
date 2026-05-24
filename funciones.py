#Elaborado por Pablo Vargas y Julian Moya
#Fecha de creacion 23-05-26 6:00 pm
#Ultima modificacion 23-05-26 
#Version: 3.14.3

#Definicion de funciones
import re

def validarCedula(cedula):
    """
    Funcionalidad: Valida que la cedula tenga el formato #-####-#### y que el primer digito no sea 0.
    Entrada: cedula
    Salida: True si es valida, False si no
    """
    patron = r'^[1-9]\d{0,3}-\d{4}-\d{4}$'
    return re.match(patron, cedula) is not None


def validarFecha(fecha):
    """
    Funcionalidad: Valida que la fecha tenga el formato DD/MM/AAAA y que los valores de dia, mes y anno sean coherentes.
    Entrada: fecha
    Salida: True si es valida, False si no
    """
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(patron, fecha):
        return False
    partes = fecha.split("/")
    dd = int(partes[0])
    mm = int(partes[1])
    aaaa = int(partes[2])
    if mm <1 or mm > 12:
        return False
    if dd < 1 or dd > 31:
        return False
    if aaaa < 1900 or aaaa> 2026:
        return False
    return True


def validarCorreo(correo):
    """
    Funcionalidad: Valida que el correo tenga un formato valido y pertenezca a uno de los dominios permitidos.
    Entrada: correo
    Salida: True si es valido, False si no
    """
    patron= r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\.){1,2}[a-zA-Z]{2,}$'
    dominiosValidos = ["costarricense.cr", "racsa.go.cr", "ccss.sa.cr", "gmail.com"]
    if not re.match(patron, correo):
        return False
    dominio = correo.split("@")[1]
    return dominio in dominiosValidos


def validarTelefono(telefono):
    """
    Funcionalidad: Valida que el telefono tenga el formato ####-#### y que el primer digito no sea 0, 1, 3 ni 5.
    Entrada: telefono
    Salida: True si es valido, False si no
    """
    patron = r'^[2467889]\d{3}-\d{4}$'
    return re.match(patron, telefono) is not None


def validarPeso(peso):
    """
    Funcionalidad: Valida que el peso sea mayor a 50 y menor a 120 kg.
    Entrada: peso
    Salida: True si es valido, False si no
    """
    try:
        p = float(peso)
        return 50 < p < 120
    except:
        return False