import logging
from typing import Union
import time

import numpy as np

from abstract_problem import AbstractProblem


class SetCovering(AbstractProblem):
    # TODO:
    #  Implementar funciones de costos
    #  Implementar restricciones
    #  Implementar creación de soluciones aleatorias
    #  Implementar funciones de penalización en caso de ser necesario

    def __init__(self, filename: str) -> None:
        super(SetCovering, self).__init__()
        self.rows: Union[int, None] = None
        self.columns: Union[int, None] = None
        self.columns_vector: Union[list, None] = None
        self.rows_vector: Union[list, None] = None
        logging.info(f"leyendo archivo: {filename}")
        logging.info('Midiendo tiempos de lectura de archivo')
        start = time.time()
        self.read_file(filename)
        logging.info(f"{time.time() - start}")
        self.dimensions = self.rows

    def get_solution_fitness(self, solution):
        cost = self.rows[0]
        feasible = is_solution(self.rows[0], solution)
        #Creo que el self.rows tiene que tener una variable para recorrerse
        # en este caso no ? y esa se debería pasar por parametro de función ? #
        if not feasible:
            return inf
        else:
            fitness = np.dot(sol, cost)
        
        return fitness


    def get_random_solution(self, rng=None):

        pass

    def is_solution(self, solution) -> bool:
        flag = True
        aux = np.dot(self.rows_vector[0"leer comentario"],solution)           # Multiplica la lista  de cobertura por la solucion
        #Parece que en el self.rows_vector tenemos que pasarle a la funcion una variable que recorra el rows_vector no ? #

        if 0 in aux:     #Si zona no esta cubierta entonces se entrega falso#             
            flag = False

        return flag, aux



    def read_file(self, filename: str = 'scp2.txt') -> None:
        # logging.debug('Lectura de archivos')
        with open(filename, "r") as f:
            logging.debug('abriendo archivo de instancia')
            # Genera una lista de valores numéricos
            content = list(map(int, f.read().strip().split()))
            self.rows = content.pop(0)
            self.columns = content.pop(0)
            logging.debug(f"filas: {self.rows}\tColumnas{self.columns}")
        costs_vector, rows_data = content[0:self.columns], content[
                                                           self.columns:]
        self.columns_vector = np.array(costs_vector)
        logging.debug(f'Columnas obtenidas: {len(costs_vector)}')

        # Las filas tienen la siguiente estructura

        # primer valor(N) = cantidad de columnas asociadas
        # siguientes N valores: idx de las columnas asociadas

        # Esta lista debe tener largo "rows" al finalizar la iteración
        rows_info = []
        logging.debug(f'*' * 80)
        logging.debug(f'Mostrando filas')
        for i in range(self.rows):
            # El primer valor indica la cantidad de vecinos
            row_size = rows_data.pop(0)
            logging.debug(rows_data[0:row_size])
            # Los siguientes "row_size" valores son los vecinos
            rows_info.append(rows_data[0:row_size])
            rows_data = rows_data[row_size:]
        # Se almacena la lista de vecinos en el objeto
        self.rows_vector = rows_data
        logging.debug(f'*' * 80)
        logging.debug(f'filas encontradas: {len(rows_info)}')


if __name__ == "__main__":
    logging.basicConfig(filename='reader.log', level='DEBUG')
    SetCovering("test_problem_file_scp.txt")
    # read_instance("scp2.txt")

