import logging
import random
from datetime import datetime

import numpy as np

from .logger import log_fitness_table, log_hive_detail
from .utils import transform

from .problems import AbstractProblem


class MatrixHive:

    def __init__(self, problem, colony_size, max_trials: int = 5,
                 iterations=10, maximization=False,
                 problem_type='CONTINUOUS', transfer_function='S_SHAPE_2D',
                 binarization_method='STANDARD', alpha=0.5):

        # Hive elements
        self.problem: AbstractProblem = problem
        self.colony_size: int = colony_size
        self.bees = np.zeros(shape=[self.colony_size,
                                    self.problem.dimensions], dtype=float)

        # Solution elements
        self.fitness = np.zeros([self.colony_size], dtype=float)
        self.best_bee = None
        self.best_fitness = -np.inf if maximization else np.inf

        # search elementws
        self.iterations = iterations
        self.max_trials = max_trials
        self.trials = np.zeros([self.colony_size])
        self.maximization = maximization
        self.index_array = np.array(range(colony_size))

        # Transformation elements
        self.transformation_kwargs = {
            'transformation_type': problem_type,
            'transfer_function': transfer_function,
            'binarization_method': binarization_method,
            'alpha': None
        }

        log_hive_detail({
            'colony_size': colony_size,
            'max_trials': max_trials,
            'is_maximization': maximization,
            'iterations': iterations,
        })

    def run(self):
        """
        Ejecuta la búsqueda
        :return: None
        """
        self.initialize()
        counter = 0
        while counter < self.iterations:
            logging.debug('sending employees')
            self.send_employees()
            logging.debug('sending outlookers')
            self.send_onlookers()
            logging.debug('sending scouts')
            self.global_fitness()
            self.send_scouts()
            log_fitness_table(counter, self.best_bee, self.best_fitness)
            counter += 1

        to_csv = np.append(self.bees, self.fitness.reshape(-1, 1), axis=1)
        np.savetxt(f'./results{datetime.now().date()}.csv', to_csv,
                   delimiter=',')
        logging.info(f'best solution found: {self.best_bee}')
        logging.info(f'fitness: {self.best_fitness}')

    def initialize(self):
        """
        Inicializa la colmena, creando abejas aleatorias y registrando su
        fitness

        :return: None
        """
        hive = []
        fitness = []
        for i in range(self.colony_size):
            new_bee = self.problem.get_random_solution()
            logging.debug(new_bee)
            hive.append(new_bee)
            fitness.append(self.problem.get_solution_fitness(new_bee))
        self.bees = np.array(hive)
        self.fitness = np.array(fitness)

    def send_employees(self):
        for bee in self.index_array:
            # logging.debug(f'bee: {bee}')
            self.move_bee(bee)

    def send_onlookers(self):
        probability_vector = self.fitness / sum(self.fitness)
        for bee in self.index_array:
            # logging.debug(f'bee: {bee}')
            self.move_bee(bee, employee=False,
                          probability_vector=probability_vector)

    def send_scouts(self):
        stale_source = np.where(self.trials > self.max_trials)[0]
        # logging.debug(f'stale sources: {stale_source}')
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
        Selecciona un vecino basado en un vector de probabilidades

        :param bee: Indice de la abeja en la colmena
        :param probability_vector: Vector de probabilidades basado en fitness

        :return: Solución vecina encontrada
        """
        new_source = np.random.choice(self.index_array, p=probability_vector)
        while new_source == bee:
            new_source = np.random.choice(self.index_array,
                                          p=probability_vector)
        return new_source

    def pick_random_neighbor(self, bee: int):
        """
        Elige un vecino de la colmena de manera aleatoria
        :param bee: Índice de la abeja en la colmena

        :return: Solución vecina encontrada
        """
        neighbor = random.randint(0, self.colony_size - 1)
        while neighbor == bee:
            neighbor = random.randint(0, self.colony_size - 1)
        return neighbor

    ############################################################################
    # Selección de nueva solución
    ############################################################################

    def pick_new_fitness(self, old_fitness: float, new_fitness: float) -> bool:
        """
        Indica si el nuevo fitness es mejor al registrado anteriormente

        :param old_fitness: Fitness de solución conocida
        :param new_fitness: Fitness de nueva solución
        :return: True si la nueva solución es mejor que la actual. False,
        en caso contrario
        """
        if self.maximization:
            return new_fitness > old_fitness
        return old_fitness > new_fitness

    def get_neighbor(self, bee: int,
                     employee: bool = True,
                     probability_vector: np.array = None) -> int:
        """
        Método encargado de retornar un vecino para una abeja dada
        :param bee: Índice de la abeja en la colmena
        :param employee: Indica si la abeja es obrera
        :param probability_vector: Vector de probabilidades para la colmena
        :return: Índice del vecino encontrado
        """
        if employee:
            neighbor = self.pick_random_neighbor(bee)
        else:
            neighbor = self.pick_roulette(bee, probability_vector)
        return neighbor

    def move_bee(self, bee: int, employee: bool = True,
                 probability_vector: np.array = None) -> np.array:
        """

        :param bee: Abeja que se moverá
        :param employee: Indica si la abeja es obrera
        :param probability_vector: Vector de probabilidades para la colmena
        :return: Tupla con la solución generada, y el fitness de la solución
        """
        neighbor = self.get_neighbor(bee, employee, probability_vector)
        updated_bee = self.perform_movement(bee, neighbor)
        # Se presume que existirá al menos una solución válida al combinar
        # con vecino
        # logging.debug('searching neighbor...')
        while not self.problem.is_solution(updated_bee):
            neighbor = self.get_neighbor(bee, employee, probability_vector)
            self.perform_movement(bee, neighbor)
        # logging.debug(f'neighbor picked {neighbor}')

        fitness = self.problem.get_solution_fitness(updated_bee)

        if self.pick_new_fitness(self.fitness[bee], fitness):
            # logging.debug('new food source found')
            self.bees[bee] = neighbor
            self.fitness[bee] = fitness
            self.trials[bee] = 0
        else:
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

    ############################################################################
    # Generación de nueva solución
    ############################################################################

    def perform_movement(self, bee: int, neighbor: int) -> np.array:
        """
        Genera la nueva solución a partir de una abeja y su vecina
        :param bee: Índice de la abeja en la colmena
        :param neighbor: Índice de la abeja vecina en la colmena
        :return: Nueva solución generada por la función de movimiento
        """
        # X'_ij + phi * ( X_ij - Y_ij )
        # logging.debug(f'mixing: {bee} and {neighbor}')
        # logging.debug(f'{self.bees[bee]} - {self.bees[neighbor]}')

        phi = np.random.sample(size=self.problem.dimensions)
        difference = self.bees[bee] - self.bees[neighbor]
        # logging.debug(f'{phi} * {difference}')
        updated_bee = np.copy(self.bees[bee])

        delta = np.multiply(phi, difference)
        updated_bee += delta

        updated_bee = transform(updated_bee, **self.transformation_kwargs)
        return updated_bee


