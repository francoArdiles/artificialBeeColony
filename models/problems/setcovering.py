import logging

from .abstract_problem import AbstractProblem
import numpy as np

class SetCovering():
    tallaFilas = 0
    tallaColumnas = 0
    contador = 0
    aux = 0 
    k = 0 

    #Se abre archivo para test#
    fo = open("scp2.txt", "r")
    lines = fo.readlines()

    #Se ve dimension de la matriz con los datos entregados#
    dimensionDeLaMatriz = lines[0].split()
    filas = dimensionDeLaMatriz[0]
    columnas = dimensionDeLaMatriz[1]
    columnas = int(columnas)
    filas = int(filas)

    ##Lineas de testing##
    #print("Filas: " + str(filas) )
    #print("Columnas: " + str(columnas) )
    ##Fin lineas de testing##

    costosColumnas = []
    #Se leen los costos por columna#
    for i in lines:
        if(i == lines[0]): #Por matriz ya inicializada se salta lectura de primera linea#
            continue
        cadena = i.split()
        costosColumnas.append(cadena)
        contador += len(costosColumnas[aux])
        aux += 1
        if(contador == columnas):
            contador = aux #Se guarda en contador el número de línea en que quedo la lectura del archivo#
            break 



    contador += 1 #Se suma uno a contador para mover puntero en archivo .txt#
    j = 0  #Variable para recorrer solo la lista dentro de la lista, y no la lista completa#
    totalCasosIncorporados = 0 #Cuenta cuantos casos han sido incorporados a la lista. Solo para la última parte del txt. 3) # 
    filasConSusVecinos = [] #En posición 0 incluye total de vecinos, luego vecinos. Se repite este patrón en los otros casos que sigen en la lista pero empezando desde la último dato de las lista + 1#

    #Se leen numero de columnas y vecinos de fila#
    for i in lines:
        filasConSusVecinos.append(lines[contador]) 
        totalVecinos = lines[contador]
        totalCasosIncorporados += 1
        aux = 0
        #Se leen todos los números que corresponden al caso que se está evaluando#
        while (aux < int(totalVecinos) ):  
            contador += 1
            j += 1
            filasConSusVecinos.append(lines[contador].split() )
            aux += len(filasConSusVecinos[j]) 

        contador += 1
        j += 1
        if(contador >= len(lines)):
            break




    print("Descomenten las últimas líneas si quieren revisar que el código funciona: 72, 73 y 74")
    #Si se quiere ver lista de listas y cuantas líneas se leyeron del .txt. Descomentar las siguientes 3 líneas#
    #print(costosColumnas)
    #print(filasConSusVecinos)
    #print("contador Final: " +str(contador) )

          #FORMATO TXT#
#El formato del .txt es el siguiente: #
#1)Numero de filas y columnas.
#2)El costo de cada columna.
#3)Por cada fila "i", el número de columnas que cubre la fila "i" seguido por la lista de columnas que cubren "i"
