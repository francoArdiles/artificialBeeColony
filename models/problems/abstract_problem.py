from abc import ABC


class AbstractProblem(ABC):

    def __init__(self):
        self.problem = None
        self.restrictions = None
        self.fitness = None
        self.dimensions = 0

    def get_solution_fitness(self, solution):
        pass

    def get_random_solution(self, rng=None):
        pass

    def is_solution(self, solution) -> bool:
        pass
