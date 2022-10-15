import abc
from abc import ABC


class AbstractProblem(ABC):

    def __init__(self):
        self.problem = None
        self.restrictions = None
        self.fitness = None
        self.dimensions: int = 0

    @abc.abstractmethod
    def get_solution_fitness(self, solution):
        pass

    @abc.abstractmethod

    def get_random_solution(self, rng=None):
        pass

    @abc.abstractmethod
    def is_solution(self, solution) -> bool:
        pass
