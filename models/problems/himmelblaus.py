import logging

from .abstract_problem import AbstractProblem
import numpy as np


class HimmelBlaus(AbstractProblem):

    def __init__(self, max_value=None, min_value=None):
        super().__init__()
        self.dimensions = 2
        finfo = np.finfo(np.float16)

        self.max_value = max_value or finfo.max
        self.min_value = min_value or finfo.min

    def get_solution_fitness(self, solution):
        x = solution[0]
        y = solution[1]

        return np.power(np.power(x, 2) + y - 11, 2) \
               + np.power(x + np.power(y, 2) - 7, 2)

    def apply_restrictions(self, solution) -> bool:
        """
        Restricciones duras, si no se cumplen, la solución se considera
        infactible
        :param solution:
        :return:
        """

        first_invaild = solution[0] > self.max_value or solution[0] < self.min_value
        second_invalid = solution[1] > self.max_value or solution[1] < self.min_value

        return first_invaild or second_invalid

    def is_solution(self, solution) -> bool:
        not_valid = self.apply_restrictions(solution)
        # logging.debug(f'not valid: {not_valid}')
        return True

    def get_random_solution(self, rng=None):
        """
        :param rng: random generator
        :return:
        """
        if rng is not None:
            pass
        return np.random.uniform(low=self.min_value, high=self.max_value,
                                 size=self.dimensions)
