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
    filas = int(filas)
    columnas = dimensionDeLaMatriz[1]
    columnas = int(columnas)


    ##Lineas de testing##
    print("Filas: " + str(filas) )
    print("Columnas: " + str(columnas) )
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

   #print(costosColumnas)



    j = 0  #Variable para recorrer solo la lista dentro de la lista, y no la lista completa#
    totalCasosIncorporados = 0 #Cuenta cuantos casos han sido incorporados a la lista. Para la última parte del txt. 3) # 
    filasConSusVecinos = [] #En posición 0 incluye total de vecinos, luego vecinos. Se repite este patrón en los otros casos#
    bufferDatos = []
    #Se leen numero de columnas y vecinos de fila#
    for i in lines:
        bufferDatos.append(lines[contador+1]) 
        totalVecinos = lines[contador+1]
        print("TotalVecinos: " + totalVecinos)
        print("Linea: " + str(contador+1))
        totalCasosIncorporados += 1
        aux = 0
        while (aux < int(totalVecinos) ):  
            contador += 1
            bufferDatos.append(lines[contador].split() )
            aux += len(bufferDatos[j]) 
            j += 1
            print("aux: " + str(aux) )
            print("contador: " + str(contador) )

        #Se tiene que agregar la lista de filas#
        filasConSusVecinos.append(bufferDatos) 
        j += 1
        #bufferDatos.clear()



#El formato del .txt es el siguiente: #
#1)Numero de filas y columnas.
#2)El costo de cada columna.
#3)Por cada fila "i", el número de columnas que cubre la fila "i" seguido por la lista de columnas que cubren "i"
