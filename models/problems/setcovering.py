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
        self.matrix: Union[np.array, None] = None
        self.read_file(filename)
        logging.info(f"{time.time() - start}")
        self.dimensions = self.rows

    def get_solution_fitness(self, solution: np.array) -> float:
        """
        Obtiene el fitness de una solución para el problema en caso de ser
        factible
        :param solution: Solución entregada por el problema
        :return: fitness obtenido
        """
        cost = self.columns_vector
        feasible = self.is_solution(solution)
        #Creo que el self.rows tiene que tener una variable para recorrerse
        # en este caso no ? y esa se debería pasar por parametro de función ? #
        if not feasible:
            return np.inf
        else:
            fitness = np.dot(solution, cost)

        return fitness


    def get_random_solution(self, rng=None) -> np.array:
        """
        Intenta generar una solución aleaotoria para el problema
        :param rng: Generador random
        :return: Arreglo con una solución factible
        """
        pass

    def is_solution(self, solution: np.array) -> bool:
        """
        Indica si una solción entregada es factible
        :param solution: Arreglo con la solución a evaluaer
        :return: True si la solución en válida
        """
        is_solution, aux = self.is_solution(solution)
        return is_solution

    def check_solution(self, solution: np.array) -> tuple:
        """
        Comprueba que una solución sea válida y entrega el resultado del
        producto punto entre la matriz de costos y la solución entregada
        :param solution:
        :return:
        """
        flag = True
        aux = np.dot(self.matrix, solution)           # Multiplica la lista  de
        # cobertura por la solucion
        #Parece que en el self.rows_vector tenemos que pasarle a la funcion una variable que recorra el rows_vector no ? #

        if 0 in aux:     #Si zona no esta cubierta entonces se entrega falso#
            flag = False

        return flag, aux

    def read_file(self, filename: str = 'scp2.txt') -> None:
        """
        Lee el archivo solicitado y genera la información para el problema
        :param filename:
        :return:
        """
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
            # logging.debug(np.array(rows_data[0:row_size]) - 1)
            # Los siguientes "row_size" valores son los vecinos
            rows_info.append(np.array(rows_data[0:row_size]) - 1)
            rows_data = rows_data[row_size:]
        # Se almacena la lista de vecinos en el objeto
        self.rows_vector = rows_info
        logging.debug(f'*' * 80)
        logging.debug(f'filas encontradas: {len(rows_info)}')
        self.matrix = self.transform_to_matrix()

    def transform_to_matrix(self) -> np.array:
        """
        Transforma las listas generadas de la lectura de un archivo en la
        matriz de costos del problema

        :return: Arreglo con la matriz generada
        """
        logging.debug('creando matrix')
        matrix = np.zeros((self.rows, self.columns))
        for idx, row in enumerate(self.rows_vector):
            matrix[idx, row] = 1
            logging.debug(idx)
        opt = np.get_printoptions()
        np.set_printoptions(threshold=np.inf)
        logging.debug(matrix)

        np.set_printoptions(**opt)
        logging.debug('matriz creada')
        return matrix


if __name__ == "__main__":
    logging.basicConfig(filename='reader.log', level='DEBUG')
    SetCovering("test_problem_file_scp.txt")
    # read_instance("scp2.txt")

