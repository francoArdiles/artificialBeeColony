import logging

import numpy as np

from models.hive import MatrixHive
from models.problems.himmelblaus import HimmelBlaus
from models.utils.plotter import Plotter
from models.problems.setcovering import SetCovering 


def solve_himmelBlaus(colony_size=50, iterations=100):
    #func = HimmelBlaus(max_value=5, min_value=-5)
    func = HimmelBlaus(max_value=5, min_value=-5)
    hive = MatrixHive(func, colony_size=colony_size, iterations=iterations,
                      max_trials=10)
    logging.debug('COMENZANDO BUSQUEDA...\n')
    hive.run([])
    return hive


def solve_scp(colony_size, iterations, max_retries, filename, sols=[]):
    func = SetCovering(filename)
    _hive = MatrixHive(func,
                      colony_size,
                      max_retries,
                      seed=123,
                      iterations=iterations,
                      maximization=False,
                      problem_type='BINARY',
                      transfer_function='S_SHAPE_2D',
                      binarization_method='ELITIST', alpha=0.7)

    logging.debug('COMENZANDO BUSQUEDA...\n')
    _hive.run(sols)
    return _hive



if __name__ == '__main__':

    prob = 'scp'
    c_size = 5
    it = 10
    mr = 5
    fn = './data/41.scp'
    if prob == 'scp':
        logging.basicConfig(filename='scpsearch.log', level='DEBUG')
        logging.debug('INCIANDO COLMENA\n')
        hive = solve_scp(c_size, it, mr, fn, [])
    else:
        logging.basicConfig(filename='loghimmel.log', level='INFO')
        logging.debug('INCIANDO COLMENA\n')
        hive = solve_himmelBlaus(c_size, it)

    print(hive.get_best()[2])
    p = Plotter(hive.get_history())
    p.draw()
    logging.debug('BUSQUEDA FINALIZADA\n')
