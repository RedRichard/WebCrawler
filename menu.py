# -*- coding: utf-8 -*-
"""
Created on Sat May 28 14:11:38 2016

@author: gomri
"""

import busqueda

def main():
    tipoBusqueda = 0
    opcion = 0
    while opcion != 4:
        opcion = 0
        print("1. Realizar busqueda por profundidad")
        print("2. Realizar busqueda exclusiva")
        print("3. Realizar busqueda exhaustiva")
        print("4. Salir.")
        while opcion < 1 or opcion > 4:
            opcion = int(input("\tSeleccion: "))
            if opcion <1 or opcion > 4:
                print("\tSeleccion incorrecta.")
                
        if opcion == 1:
            tipoBusqueda = 3
            respuesta = busqueda.procesoBusquedaPr(tipoBusqueda)
            #busqueda.imprimirLinks()
            if respuesta != 0:
                menuInterno(tipoBusqueda)
        elif opcion == 2:
            tipoBusqueda = 1
            respuesta = busqueda.procesoBusquedaEx(tipoBusqueda)
            #busqueda.imprimirLinks()
            if respuesta != 0:
                menuInterno(tipoBusqueda)
        elif opcion == 3:
            tipoBusqueda = 2
            respuesta = busqueda.procesoBusqueda1(tipoBusqueda)
            #busqueda.imprimirLinks()
            if respuesta != 0:
                menuInterno(tipoBusqueda)
        
        elif opcion == 4:
            return 0
        
def menuInterno(tipoBusqueda):
    opcion = 0
    while opcion != 5:
        opcion = 0
        print("La busqueda ha terminado")
        print("1. Ver links encontrados")
        print("2. Ver links rotos")
        print("3. Buscar un link en los resultados")
        print("4. Grafica de tiempo")
        print("5. Volver al menu principal")
        while opcion < 1 or opcion > 5:
            opcion = int(input("\tSeleccion: "))
            if opcion < 1 or opcion > 5:
                print("\tSeleccion incorrecta.")    
        if opcion == 1:
            busqueda.imprimirLinks()
        elif opcion == 2:
            busqueda.imprimirLinksRotos()
        elif opcion == 3:
            busqueda.buscarLink()
        elif opcion == 4:
            busqueda.imprimirGrafica()
        elif opcion == 5:
            if tipoBusqueda == 3:
                busqueda.guardarArchivoPr(tipoBusqueda)
            else:
                busqueda.guardarArchivo(tipoBusqueda)
            return 0

if __name__ == "__main__":
    main()