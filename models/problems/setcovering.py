import logging

from .abstract_problem import AbstractProblem
import numpy as np

class SetCovering():
    tallaFilas = 0
    tallaColumnas = 0
    contador = 0
   

    #Se abre archivo para test#
    fo = open("scp2.txt", "r")
    lines = fo.readlines()

    #Se ve dimension de la matriz con los datos entregados#
    dimensionDeLaMatriz = lines[0].split()
    filas = dimensionDeLaMatriz[0]
    filas = int(filas)
    columnas = dimensionDeLaMatriz[1]
    columnas = int(columnas)
    #Comentario personal: Parece que no necesito crear una matriz#
    #matriz = [[0 for _ in range(columnas)] for _ in range(filas)]


    ##Lines de testing##
    print("Filas: " + str(filas) )
    print("Columnas: " + str(columnas) )
    ##Fin lineas de testing##

    costosColumnas = []
    #Se leen los costos por columna#
    for i in lines:
        if(i == lines[0]): #Por matriz ya inicializada se salta lectura de primera linea#
            continue
        cadena = i.split()
        print(cadena) 
        for j in cadena:
            #costosColumnas[contador] = j Esta es la línea que mencioné por interno la explicaré en la línea 75#
            contador += 1
            if(contador == columnas):
                break
        if(contador == columnas):
            break 


    contador += 1
    filasConSusVecinos = [] #En posición 0 incluye total de vecinos#

    #Se leen numero de columnas y vecinos de fila#
    #Esta parte del codigo la revisare exhaustivamente mañana. Encontré un error y me sorprendió#
    for i in lines:
        totalVecinos = lines[contador]  
        bufferDatos = []
        bufferDatos[0] = totalVecinos[0]  #Esta linea de código tiene una falla. La lista tiene más de un elemento al parecer#
        aux = 0
        while (aux <= totalVecinos):  #Anotación: Acá hay un problema en como se leyó .txt#
            bufferDatos.append(lines[contador + 1].split() )
            aux = len(bufferDatos)
            contador += 1
        filasConSusVecinos.append(bufferDatos) 
        bufferDatos.clear()



    #Testing: print("Contador: " + str(contador) )



#El formato del .txt es el siguiente: #
#1)Numero de filas y columnas.
#2)El costo de cada columna.
#3)Por cada fila "i", el número de columnas que cubre la fila "i" seguido por la lista de columnas que cubren "i"

#Explicación: la idea es que costosColumnas[contador] = j  utilize "j" para ir por todos números 
#que ocurrieron en el split hecho a la cadena en la línea 36:
#cadena = i.split()
#Y con contador se van colocando en la lista costos Columnas#
