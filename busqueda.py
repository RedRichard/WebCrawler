# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:32:48 2016

@author: gomri
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 17:59:45 2016

@author: gomri
"""

from urllib.request import urlopen
from urllib.parse import urlparse
import hashlib
import lxml.html
import sys
from clases import url
import pickle
import os.path

import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

#import random
from time import time

#import numpy as n 

tiempo_wc = [] 

sys.setrecursionlimit(100000)

links = []
links2 = []
llaves = {}
contador = 0
numTotalUrl = 0
numLinksRotos = 0
numRepeticiones = 0
cantidadProfundidad = 0
profundidad = 0
root = ""
paginasEvitar = ["www.google.com", "google.com","www.twitter.com",
                 "twitter.com","www.facebook.com", "fb.com","facebook.com",
                 "www.fb.com","www.youtube.com", "youtube.com", 
                 "play.spotify.com","www.spotify.com", "accounts.google.com", 
                 "www.vimeo.com","vimeo.com", "www.instagram.com",
                 "instagram.com","plus.google.com", "t.co", "www.bing.com",
                 "bing.com","www.yahoo.com", "yahoo.com", "www.wordpress.com", 
                 "wordpress.com", "www.devianart.com", "devianart.com",
                 "reddit.com", "www.reddit.com", "open.spotify.com"]

def imprimirGrafica():
    global contador, tiempo_wc, llaves
    #print(len(tiempo_wc))
    #print(len(llaves))
    contador2 = [ii for ii in range(1,len(tiempo_wc)+1)]
    fig, ax = plt.subplots()
    #if len(tiempo_wc) > 1:
    ax.plot(contador2, tiempo_wc, label="Tiempo de ejecución", marker="D",color="r")
    ax.set_xlabel('Links analizados') 
    ax.set_ylabel('Tiempo') 
    ax.grid(True)
    ax.legend(loc=2); 
    plt.title('Tiempo de ejecución:')
    plt.show()


#El siguiente es el algoritmo con ciclo recursivo:
def busqueda(contador, t0):
    global links, links2, numLinksRotos, profundidad, cantidadProfundidad
    global tiempo_wc
    #links2 = []
    if contador >= len(links):
        return links2
    else:
        aux1 = links[contador]
        print(contador) #Link analizandose
        direccion = aux1.dir
        paginaParsing = urlparse(direccion)
        if paginaParsing.path and paginaParsing.netloc not in paginasEvitar:
            try:
                pagina = urlopen(direccion, timeout=5)
                lectura =  lxml.html.fromstring(pagina.read())
                links.extend(extraccion(lectura, direccion))
                #contador = contador + 1
            except:
                auxiliar = links[contador]
                auxiliar.existe = False
                links[contador] = auxiliar
                numLinksRotos += 1
                #contador = contador + 1
            #contador = contador + 1
        tiempo_wc.append(round(time()-t0, 6))
        return busqueda(contador+1, t0)
           
            
def extraccion(lectura, aux1):
    global numTotalUrl, links, llaves, numRepeticiones, cantidadProfundidad
    for link in lectura.xpath('//a/@href'): # busca el tag href en el html
        aux2 = url(link)
        if aux2.dir[0:4] != "http":
            if aux2.dir[0] != "/":
                aux2.dir = (aux1 + aux2.dir)
            else:
                aux2.dir = (aux1[0:-1] + aux2.dir)
        if contador < cantidadProfundidad:
            aux2.profundidad = profundidad+1
        #print("%d. " %(numTotalUrl)+ aux2.dir)   #Revisa los links que estan siendo checados
        llaveAux = hashlib.md5(aux2.dir.encode("utf-8"))
        if str(llaveAux.hexdigest()) not in llaves: #Revisa la existencia de llave
            auxParse = urlparse(aux2.dir)
            if auxParse.path and auxParse.netloc not in paginasEvitar:
                links.append(aux2)
                #direcciones.append(aux2.dir)
                print("%d. " %(numTotalUrl) + aux2.dir)
                llaves[str(llaveAux.hexdigest())] = numTotalUrl
                numTotalUrl = numTotalUrl + 1
        else:
            indiceElemento = llaves.get(str(llaveAux.hexdigest()))
            #print(indiceElemento)   #Checar indice del elemento en el diccionario llaves
            respaldo = links[indiceElemento-1]
            respaldo.repeticiones += 1
            #print(respaldo.dir) #Checar el contenido que se esta extrayendo a partir de la llave
            links[indiceElemento-1] = respaldo
            numRepeticiones += 1     #Cuenta las repeticiones totales

#El siguiente es el algoritmo con ciclo recursivo:
def busquedaProfundidad(contador, t0):
    #t0 = time()
    global links, links2, numLinksRotos, cantidadProfundidad, profundidad
    global profundidadDeseada, tiempo_wc
    #links2 = []
    if contador >= len(links) and contador > 0:
        return links2
    if contador == 1:
        cantidadProfundidad = len(links)
    if contador > 1 and contador == cantidadProfundidad:
        cantidadProfundidad = len(links)
        profundidad += 1
    if profundidad == profundidadDeseada and contador > 0:
        print(profundidad)
        return links2
    else:
        aux1 = links[contador]
        print(contador)
        direccion = aux1.dir
        paginaParsing = urlparse(direccion)
        if paginaParsing.path and paginaParsing.netloc not in paginasEvitar:
            try:
                pagina = urlopen(direccion, timeout=5)
                lectura =  lxml.html.fromstring(pagina.read())
                links.extend(extraccion(lectura, direccion))
                #contador = contador + 1
                #tiempo_wc.append(round(time()-t0, 6))
            except:
                auxiliar = links[contador]
                auxiliar.existe = False
                links[contador] = auxiliar
                numLinksRotos += 1
        tiempo_wc.append(round(time()-t0, 6))
                #contador = contador + 1
            #contador = contador + 1
        return busquedaProfundidad(contador+1, t0)
 
def busquedaExclusiva(contador, t0):
    global links, links2, numLinksRotos, root, tiempo_wc
    #links2 = []
    if contador == len(links):
        return links2
    else:
        aux1 = links[contador]
        print(contador)
        direccion = aux1.dir
        paginaParsing = urlparse(direccion)
        try:
            if root[4:] in paginaParsing.path or paginaParsing.netloc:
                pagina = urlopen(direccion, timeout=5)
                lectura =  lxml.html.fromstring(pagina.read())
                links.extend(extraccionEx(lectura, direccion))
            #contador = contador + 1
        except:
            auxiliar = links[contador]
            auxiliar.existe = False
            links[contador] = auxiliar
            numLinksRotos += 1
            #contador = contador + 1
            #contador = contador + 1
        tiempo_wc.append(round(time()-t0, 6))
        return busquedaExclusiva(contador+1, t0)
    
def extraccionEx(lectura, aux1):
    global numTotalUrl, links, llaves, numRepeticiones, cantidadProfundidad
    global root
    for link in lectura.xpath('//a/@href'): # busca el tag href en el html
        aux2 = url(link)
        if aux2.dir[0:4] != "http":
            if aux2.dir[0] != "/":
                aux2.dir = (aux1 + aux2.dir)
            else:
                aux2.dir = (aux1[0:-1] + aux2.dir)
        if contador < cantidadProfundidad:
            aux2.profundidad = profundidad+1
        #print("%d. " %(numTotalUrl)+ aux2.dir)   #Revisa los links que estan siendo checados
        llaveAux = hashlib.md5(aux2.dir.encode("utf-8"))
        if str(llaveAux.hexdigest()) not in llaves: #Revisa la existencia de llave
            auxParse = urlparse(aux2.dir)
            if auxParse.path and auxParse.netloc not in paginasEvitar:
                if root in aux2.dir:
                    links.append(aux2)
                    #direcciones.append(aux2.dir)
                    print("%d. " %(numTotalUrl) + aux2.dir)
                    llaves[str(llaveAux.hexdigest())] = numTotalUrl
                    numTotalUrl = numTotalUrl + 1
        else:
            indiceElemento = llaves.get(str(llaveAux.hexdigest()))
            #print(indiceElemento)   #Checar indice del elemento en el diccionario llaves
            respaldo = links[indiceElemento-1]
            respaldo.repeticiones += 1
            #print(respaldo.dir) #Checar el contenido que se esta extrayendo a partir de la llave
            links[indiceElemento-1] = respaldo
            numRepeticiones += 1     #Cuenta las repeticiones totales

#Preparaciones
def imprimirLinks():
    global links
    j = 0
    for element in links:
        if element.existe:
            print("%d. " %(j+1) + element.dir)
            print("\t\tNumero de veces repetido: " + str(element.repeticiones))
            j += 1
    print("Numero de links encontrados: " + str(j))
        
def imprimirLinksRotos():
    global links
    j = 0
    for element in links[1:]:
        if element.existe == False:
            print("%d. " %(j+1) + element.dir)
            print("\t\tNumero de veces repetido: " + str(element.repeticiones))
            j += 1
    if len(links) == 1:
        print("No hay links rotos")
    else:
        print("Numero de links rotos: " + str(j))
      
def buscarLink():
    global llaves, links
    #print(len(llaves))
    #print(len(links))
    busqueda = str(input("\n\tLink a buscar: \n"))
    busquedaAux = 0
    for element in links:
        if element.dir == busqueda:
            busquedaAux = element
            break
    if busquedaAux:
        print("Se encontro el link:")
        print("- Numero de repeticiones: " + str(busquedaAux.repeticiones))
        print("- El link existe: " + str(busquedaAux.existe) + "\n")
    else:
        print("No se encontro el link")
      
def preparaciones():
    global links, llaves, contador, numTotalUrl, numLinksRotos
    global numRepeticiones, cantidadProfundidad, profundidad, tiempo_wc
    links = []
    llaves = {}
    tiempo_wc = []
    contador = 0
    numTotalUrl = 0
    numLinksRotos = 0
    numRepeticiones = 0
    cantidadProfundidad = 0
    profundidad = 0
    
def obtenerDireccion():
    direccion = input("\n\tEscriba la direccion web:\n")
    if direccion[0:3] == "htt":
        if direccion[-1] != "/":
            direccion = direccion + "/"
    else:
        direccion = "http://" + direccion
        if direccion[-1] != "/":
            direccion = direccion + "/"
        
    return direccion


#Proceso de busquedaEx  
def procesoBusquedaEx(tipoBusqueda):
    respuesta = ""
    print("A continuacion se realizara una busqueda de todos los")
    print("links contenidos dentro de la misma pagina original")
    #while respuesta != "s" or respuesta != "n":
    respuesta = str(input("\n\tDesea continuar? (s/n): "))
        
    if respuesta == "s":
        preparaciones()
        iniciarProcesoEx(tipoBusqueda)
        return 1
    if respuesta == "n":
        return 0
        
def iniciarProcesoEx(tipoBusqueda):
    global root, numTotalUrl, links, llaves, contador
    direccion = obtenerDireccion()
    copia = url(direccion)
    links.append(copia)
    llaveAux = hashlib.md5(copia.dir.encode("utf-8"))
    llaves[str(llaveAux.hexdigest())] = numTotalUrl
    #contador += 1
    numTotalUrl += 1
    rootParse = urlparse(direccion)
    if rootParse.path[0] == "w":
        root = rootParse.path
    else:
        root = rootParse.netloc
    
    aux = urlparse(links[0].dir)
    if aux.path[0] == "w":
        nombre = aux.path
    else:
        nombre = aux.netloc
    nombre = nombre + aux.path
    nombre = nombre.replace(".","")
    nombre = nombre.replace("/","")
    nombre = nombre + str(tipoBusqueda)
    
    if os.path.isfile(nombre + ".pickle"):
        abrirArchivo(tipoBusqueda)
    else:
        t0 = time()
        busquedaExclusiva(contador, t0)
    
#Proceso de busqueda exhaustivo
def procesoBusqueda1(tipoBusqueda):
    respuesta = ""
    print("A continuacion se realizara una busqueda de todos los")
    print("links")
    #while respuesta != "s" or respuesta != "n":
    respuesta = str(input("\n\tDesea continuar? (s/n): "))
        
    if respuesta == "s":
        preparaciones()
        iniciarProceso(tipoBusqueda)
        return 1
    if respuesta == "n":
        return 0
        
def iniciarProceso(tipoBusqueda):
    global root, numTotalUrl, links, llaves, contador
    direccion = obtenerDireccion()
    copia = url(direccion)
    links.append(copia)
    llaveAux = hashlib.md5(copia.dir.encode("utf-8"))
    llaves[str(llaveAux.hexdigest())] = numTotalUrl
    #contador += 1
    numTotalUrl += 1
    rootParse = urlparse(direccion)
    if rootParse.path[0] == "w":
        root = rootParse.path
    else:
        root = rootParse.netloc
        
    aux = urlparse(links[0].dir)
    if aux.path[0] == "w":
        nombre = aux.path
    else:
        nombre = aux.netloc
    nombre = nombre + aux.path
    nombre = nombre.replace(".","")
    nombre = nombre.replace("/","")
    nombre = nombre + str(tipoBusqueda)
    
    if os.path.isfile(nombre + ".pickle"):
        abrirArchivo(tipoBusqueda)
    else:
        t0 = time()
        busqueda(contador, t0)
        
def guardarArchivo(tipoBusqueda):
    global links
    #print(tipoBusqueda)
    aux = urlparse(links[0].dir)
    if aux.path[0] == "w":
        nombre = aux.path
    else:
        nombre = aux.netloc
    nombre = nombre + aux.path
    nombre = nombre.replace(".","")
    nombre = nombre.replace("/","")
    nombre = nombre + str(tipoBusqueda)
    with open(nombre + ".pickle", "wb") as archivo:
        pickle.dump(links, archivo, protocol = 2)
    
def abrirArchivo(tipoBusqueda):
    global links
    aux = urlparse(links[0].dir)
    if aux.path[0] == "w":
        nombre = aux.path
    else:
        nombre = aux.netloc
    nombre = nombre + aux.path
    nombre = nombre.replace(".","")
    nombre = nombre.replace(".","")
    nombre = nombre + str(tipoBusqueda)
    with open(nombre + ".pickle", "rb") as archivo:
        links = pickle.load(archivo)

    
#Proceso de busqueda profundidad
def procesoBusquedaPr(tipoBusqueda):
    respuesta = ""
    print("A continuacion se realizara una busqueda de todos los")
    print("links encontrados hasta determinada profundidad")
    #while respuesta != "s" or respuesta != "n":
    respuesta = str(input("\n\tDesea continuar? (s/n): "))
        
    if respuesta == "s":
        preparaciones()
        iniciarProcesoPr(tipoBusqueda)
        return 1
    if respuesta == "n":
        return 0

def iniciarProcesoPr(tipoBusqueda):
    global root, numTotalUrl, links, llaves, contador, profundidadDeseada
    direccion = obtenerDireccion()
    copia = url(direccion)
    links.append(copia)
    llaveAux = hashlib.md5(copia.dir.encode("utf-8"))
    llaves[str(llaveAux.hexdigest())] = numTotalUrl
    #contador += 1
    numTotalUrl += 1
    rootParse = urlparse(direccion)
    if rootParse.path[0] == "w":
        root = rootParse.path
    else:
        root = rootParse.netloc
        
         
    profundidadDeseada = input("Profundidad hasta la que desea buscar: ")
    profundidadDeseada = str(profundidadDeseada)
    aux = urlparse(links[0].dir)
    if aux.path[0] == "w":
        nombre = aux.path
    else:
        nombre = aux.netloc
    nombre = nombre + aux.path
    nombre = nombre.replace(".","")
    nombre = nombre.replace("/","")
    nombre = nombre + str(tipoBusqueda) + "_" + str(profundidadDeseada)
    profundidadDeseada = int(profundidadDeseada)
    if os.path.isfile(nombre + ".pickle"):
        abrirArchivoPr(tipoBusqueda)
    else:
        t0 = time()
        busquedaProfundidad(contador, t0)
    
def guardarArchivoPr(tipoBusqueda):
    global links, profundidadDeseada
    #print(tipoBusqueda)
    aux = urlparse(links[0].dir)
    if aux.path[0] == "w":
        nombre = aux.path
    else:
        nombre = aux.netloc
    nombre = nombre + aux.path
    nombre = nombre.replace(".","")
    nombre = nombre.replace("/","")
    nombre = nombre + str(tipoBusqueda) + "_" + str(profundidadDeseada)
    #archivo = open(nombre + ".pickle", "wb")
    #print("Hay un total de: " + str(len(links)))
    with open(nombre + ".pickle", "wb") as archivo:
        pickle.dump(links, archivo, protocol = 2)
    
def abrirArchivoPr(tipoBusqueda):
    global links, profundidadDeseada
    aux = urlparse(links[0].dir)
    if aux.path[0] == "w":
        nombre = aux.path
    else:
        nombre = aux.netloc
    nombre = nombre + aux.path
    nombre = nombre.replace(".","")
    nombre = nombre.replace("/","")
    nombre = nombre + str(tipoBusqueda) + "_" + str(profundidadDeseada)
    with open(nombre + ".pickle", "rb") as archivo:
        links = pickle.load(archivo)
