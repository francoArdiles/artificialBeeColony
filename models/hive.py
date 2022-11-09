"""
Módulo encargado de la ejecución de búsquedas utilizando la metaheurística de
Artificial Bee Colony
"""

import logging
from typing import Union
from datetime import datetime

import numpy as np

from models.utils.logger import log_fitness_table, log_hive_detail
from models.utils.utils import transform, binarize
from models.utils.iteration_history import History
from .problems import AbstractProblem


class MatrixHive:
    """
    Clase que contiene la colmena
    """
    def __init__(self, problem: AbstractProblem,
                 colony_size,
                 max_trials: int = 5,
                 iterations=10,
                 maximization=False,
                 seed: Union[int, None] = None,
                 problem_type='CONTINUOUS',
                 transfer_function='S_SHAPE_2D',
                 binarization_method='STANDARD',
                 alpha=0.5):

        # Hive elements
        self.problem: AbstractProblem = problem
        if seed:
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()
        self.problem.rng = self.rng
        self.colony_size: int = colony_size
        self.bees = np.zeros(shape=[self.colony_size,
                                    self.problem.dimensions], dtype=float)
        self.history = History(problem.__class__.__name__)
        # Solution elements
        self.fitness = np.zeros([self.colony_size], dtype=float)
        self.best_bee = None
        self.best_fitness = -np.inf if maximization else np.inf

        # search elements
        self.iterations = iterations
        self.max_trials = max_trials
        self.trials = np.zeros([self.colony_size])
        self.maximization = maximization
        self.index_array = np.array(range(colony_size))

        # Transformation elements
        self.transformation_kwargs = {
            'transformation_type': problem_type,
            'transfer_function': transfer_function,
            'bin_type': binarization_method,
            'alpha': alpha,
            'original_solution': None,
            'best_solution': None,
            'rng': self.rng
        }

        log_hive_detail({
            'colony_size': colony_size,
            'max_trials': max_trials,
            'is_maximization': maximization,
            'iterations': iterations,
        })
    """
    Clase que contiene la colmena
    """

    def run(self, base_sols):
        """
        Ejecuta la búsqueda
        :return: None
        """
        self.initialize(base_sols)
        self.global_fitness()

        counter = 0
        # print('starting...', end='')
        while counter < self.iterations:
            logging.debug('sending employees')
            self.send_employees()
            # print('.', end='')

            logging.debug('sending outlooks')
            self.send_onlookers()
            # print('.', end='')

            logging.debug('sending scouts')
            self.global_fitness()
            self.send_scouts()
            # print('.', end='')

            log_fitness_table(counter, self.best_bee, self.best_fitness)
            counter += 1
            # print()
            # print('nueva iteración')

        to_csv = np.append(self.bees, self.fitness.reshape(-1, 1), axis=1)
        np.savetxt(f'./results{datetime.now().date()}.csv', to_csv,
                   delimiter=',')
        # logging.info(f' best solution found: {self.best_bee}')
        # logging.info(f' fitness: {self.best_fitness}')

    def initialize(self, sols: Union[list, None] = None) -> None:
        """
        Inicializa la colmena, creando abejas aleatorias y registrando su
        fitness

        :return: None
        """
        hive = []
        fitness = []
        for i in range(self.colony_size):
            if sols:
                new_bee = sols.pop()
            else:
                new_bee = self.problem.get_random_solution()
            hive.append(new_bee)
            fitness.append(self.problem.get_solution_fitness(new_bee))
        self.bees = np.array(hive)
        self.fitness = np.array(fitness)

    def send_employees(self) -> None:
        """
        Ejecuta interacción de abejas obreras

        :return: None
        """
        # print('buscando....')
        for bee in self.index_array:
            self.move_bee(bee)

    def send_onlookers(self):
        """
        Ejecuta iteración de abejas en espera

        :return: None
        """
        # logging.debug(self.fitness)
        sol_vector = np.copy(self.fitness)
        if not self.maximization:
            sol_vector = 1/self.fitness
        # logging.debug(sol_vector)
        probability_vector = sol_vector / sum(sol_vector)
        # logging.debug(probability_vector)
        logging.debug('moviendo abejas')
        for bee in self.index_array:
            self.move_bee(bee, employee=False,
                          probability_vector=probability_vector)

    def send_scouts(self) -> None:
        """
        Ejecuta iteración de abejas exploradoras.

        :return:
        """
        stale_source = np.where(self.trials > self.max_trials)[0]
        for bee in stale_source:
            new_source = self.problem.get_random_solution()
            self.bees[bee] = new_source
            self.fitness[bee] = self.problem.get_solution_fitness(new_source)
            self.trials[bee] = 0

    ############################################################################
    # Selección de vecino
    ############################################################################

    def pick_roulette(self, bee: int, probability_vector: np.array):
        """
        Selecciona un vecino basado en un vector de probabilidades.
        :param bee: Índice de la abeja en la colmena.
        :param probability_vector: Vector de probabilidades basado en fitness.
        :return: Solución vecina encontrada.
        """
        new_source = self.rng.choice(self.index_array, p=probability_vector)
        while new_source == bee:
            new_source = self.rng.choice(self.index_array,
                                          p=probability_vector)
        return new_source

    def pick_random_neighbor(self, bee: int) -> np.array:
        """
        Elige un vecino de la colmena de manera aleatoria.
        :param bee: Índice de la abeja en la colmena.
        :return: Solución vecina encontrada.
        """

        neighbor = self.rng.integers(0, self.colony_size)
        while neighbor == bee:
            neighbor = self.rng.integers(0, self.colony_size)
        return neighbor

    ############################################################################
    # Selección de nueva solución
    ############################################################################

    def pick_new_fitness(self, old_fitness: float, new_fitness: float) -> bool:
        """
        Indica si el nuevo fitness es mejor al registrado anteriormente.
        :param old_fitness: Fitness de solución conocida.
        :param new_fitness: Fitness de nueva solución.
        :return: True si la nueva solución es mejor que la actual. False,
        en caso contrario.
        """
        if self.maximization:
            return new_fitness > old_fitness
        return old_fitness > new_fitness

    def get_neighbor(self, bee: int,
                     employee: bool = True,
                     probability_vector: np.array = None) -> int:
        """
        Método encargado de retornar un vecino para una abeja dada.
        :param bee: Índice de la abeja en la colmena.
        :param employee: Indica si la abeja es obrera.
        :param probability_vector: Vector de probabilidades para la colmena.
        :return: Índice del vecino encontrado.
        """
        if employee:
            neighbor = self.pick_random_neighbor(bee)
        else:
            neighbor = self.pick_roulette(bee, probability_vector)
        return neighbor

    def move_bee(self, bee: int, employee: bool = True,
                 probability_vector: np.array = None) -> np.array:
        """
        Realiza el movimiento de una abeja

        :param bee: Abeja que se moverá.
        :param employee: Indica si la abeja es obrera.
        :param probability_vector: Vector de probabilidades para la colmena.
        :return: Tuple con la solución generada, y el fitness de la solución
        """
        neighbor = self.get_neighbor(bee, employee, probability_vector)
        updated_bee = self.perform_movement(bee, neighbor)
        # Se presume que existirá al menos una solución válida al combinar
        # con vecino
        # logging.debug('searching neighbor...')
        if not self.problem.is_solution(updated_bee):
            updated_bee = self.problem.repair(updated_bee)
            # neighbor = self.get_neighbor(bee, employee, probability_vector)
            # updated_bee = self.perform_movement(bee, neighbor)

        fitness = self.problem.get_solution_fitness(updated_bee)

        if self.pick_new_fitness(self.fitness[bee], fitness):
            # Actualiza el fitness si es mejor al anterior
            # logging.debug('new food source found')
            self.bees[bee] = updated_bee
            self.fitness[bee] = fitness
            self.trials[bee] = 0
        else:
            # Si es peor aumenta el contador
            self.trials += 1
        return updated_bee, fitness

    def global_fitness(self):
        """
        Obtiene el mejor fitness encontrado. Si es mejor que el mejor
        encontrado hasta el momento, se actualiza.
        :return: None
        """
        if self.maximization:
            index = np.where(self.fitness == np.max(self.fitness))[0][0]
        else:
            index = np.where(self.fitness == np.min(self.fitness))[0][0]
        if self.pick_new_fitness(self.best_fitness, self.fitness[index]):
            self.best_bee = np.copy(self.bees[index])
            self.best_fitness = np.copy(self.fitness[index])
        self.history.add(self.best_fitness)

    def get_history(self):
        """
        Retorna el objeto historia de la ejecución.
        :return:
        """
        return self.history

    ############################################################################
    # Generación de nueva solución
    ############################################################################

    def perform_movement(self, bee: int, neighbor: int) -> np.array:
        """
        Genera la nueva solución a partir de una abeja y su vecina.
        :param bee: Índice de la abeja en la colmena.
        :param neighbor: Índice de la abeja vecina en la colmena.
        :return: Nueva solución generada por la función de movimiento.
        """

        phi = self.rng.random(size=self.problem.dimensions)
        difference = self.bees[bee] - self.bees[neighbor]
        # logging.debug(f'{phi} * {difference}')
        updated_bee = np.copy(self.bees[bee])

        delta = np.multiply(phi, difference)
        updated_bee += delta
        self.transformation_kwargs['original_solution'] = self.bees[bee]
        self.transformation_kwargs['best_solution'] = self.best_bee

        updated_bee = self.get_solution(updated_bee)
        return updated_bee

    def get_solution(self, updated_bee: np.array) -> np.array:
        """
        Realiza la transformación al movimiento de una abeja en caso de ser
        necesario.
        :param updated_bee: Arregla de la abeja en su nueva posición.
        :return: Valor actualizado de la abeja
        """

        t_type = self.transformation_kwargs.get('transformation_type')
        if t_type == 'CONTINUOUS':
            return updated_bee
        transformed = transform(updated_bee, **self.transformation_kwargs)
        if t_type == 'BINARY':
            return binarize(transformed, **self.transformation_kwargs)
        elif t_type == 'DISCRETE':
            return transformed

    def get_best(self, array=True, fitness=True, result=True):
        """
        Obtiene la información de la mejor solución encontrada.
        :param array: Entregar el arreglo de la solución.
        :param fitness: Entregar el fitness de la solución.
        :param result: Entregar el resultado de la función objetivo.
        :return: Lista con los elementos solicitados
        """
        if self.best_bee is None:
            return []
        x = []
        if array:
            x.append(self.best_bee)
        if fitness:
            x.append(self.best_fitness)
        if result:
            x.append(self.problem.result(self.best_bee))
        return x
