#Elaborado por: Pablo Vargas y Julian Moya
#Fecha de creacion: 22-05-26 12:00 md
#Ultima modificacion: 22-05-26 10:30 pm
#Versionn: 3.14.3
import funciones
import archivos

def menu():
    print("\n  Cargando base de datos desde memoria secundaria...")
    baseDatos = archivos.leerBD()
    hayBD = len(baseDatos) > 0
    print("  Base de datos cargada. Registros actuales: " + str(len(baseDatos)))
    salir = False
    while not salir:
        print("\n")
        print("  |        SISTEMA - Donemos Sangre          |")
        print("")
        print("  1. Insertar donador")
        print("  2. Generar donadores")
        if hayBD:
            print("  3. Actualizar datos del donador")
            print("  4. Eliminar donador")
        else:
            print("  3. Actualizar datos del donador  [NO DISPONIBLE]")
            print("  4. Eliminar donador              [NO DISPONIBLE]")
        print("  5. Insertar lugar de donacion segun provincia")
        if hayBD:
            print("  6. Reportes")
        else:
            print("  6. Reportes                      [NO DISPONIBLE]")
        print("  7. Salir")
        print("")
        opcion=input("  Seleccione una opcion: ").strip()
        if opcion== "1":
            baseDatos=funciones.insertarDonador(baseDatos)
            hayBD=len(baseDatos) > 0
            archivos.grabarBD(baseDatos)
        elif opcion== "2":
            baseDatos= funciones.generarDonadores(baseDatos)
            hayBD=len(baseDatos) > 0
            archivos.grabarBD(baseDatos)
        elif opcion== "3":
            if hayBD:
                baseDatos=funciones.actualizarDonador(baseDatos)
                archivos.grabarBD(baseDatos)
            else:
                print("\n  Opcion no disponible. Primero inserte donadores.")
        elif opcion== "4":
            if hayBD:
                baseDatos=funciones.eliminarDonador(baseDatos)
                archivos.grabarBD(baseDatos)
            else:
                print("\n  Opcion no disponible. Primero inserte donadores.")
        elif opcion== "5":
            funciones.insertarLugar()
        elif opcion== "6":
            if hayBD:
                funciones.menuReportes(baseDatos)
            else:
                print("\n  Opcion no disponible. Primero inserte donadores.")
        elif opcion== "7":
            print("\n  Donar sangre, es donar vida.")
            salir= True
        else:
            print("\n  Opcion invalida. Intente de nuevo.")
    return
menu()
