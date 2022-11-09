import logging
import sys

from models.problems.abstract_problem import AbstractProblem
import numpy as np


class HimmelBlaus(AbstractProblem):

    def __init__(self, max_value=None, min_value=None, rng=None):
        super().__init__()
        self.dimensions = 2
        finfo = np.finfo(np.float16)

        self.max_value = max_value or finfo.max
        self.min_value = min_value or finfo.min
        if not rng:
            self.rng = np.random.default_rng()
        else:
            self.rng = rng

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
        return self.rng.uniform(low=self.min_value, high=self.max_value,
                                size=self.dimensions)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
    else:
        x = self.rng.random()
        y = np.random.rand()
    problem = HimmelBlaus()
    # print(problem.get_solution_fitness([x, y]))
    logging.debug('BUSQUEDA FINALIZADA\n')
