import logging

from models.hive import MatrixHive
from models.problems.himmelblaus import HimmelBlaus
from models.problems.setcovering import SetCovering 


def solve_himmelBlaus(colony_size=50, iterations=100):
    #func = HimmelBlaus(max_value=5, min_value=-5)
    func = SetCovering()
    hive = MatrixHive(func, colony_size=colony_size, iterations=iterations,
                      max_trials=10)
    logging.debug('COMENZANDO BUSQUEDA...\n')
    hive.run()


if __name__ == '__main__':
    logging.basicConfig(filename='loghimmel.log', level='INFO')
    logging.debug('INCIANDO COLMENA\n')
    solve_himmelBlaus()
    logging.debug('BUSQUEDA FINALIZADA\n')
