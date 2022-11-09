import logging
import sys


from models.hive import MatrixHive
from models.problems.setcovering import SetCovering
# INFO:root:argumentos utilizados: {'colony_size': '100', 'iterations':
# '108', 'instance': '/home/iraceTester/franco/instances/scp48.txt', 'seed': '1880787867', 'transfer': 'V_SHAPE_ARCTAN', 'bin_method': 'COMPLEMENT', 'alpha': 0.5, 'max_retries': '17'}


ARGUMENTS = {
    'colony_size': 50,
    'iterations': 100,
    'instance': 'data/instances/scp41.txt',
    'seed': 1234567,
    'transfer': 'S_SHAPE_2D',
    'bin_method': 'ELITIST',
    'alpha': 0.5,
    'max_retries': 17,
}


def solve_scp(colony_size,
              iterations,
              max_retries,
              instance,
              transfer='S_SHAPE_2D',
              bin_method='STANDARD',
              alpha=0.5,
              sols=None,
              **kwargs):
    func = SetCovering(instance)
    _hive = MatrixHive(func,
                       colony_size,
                       max_retries,
                       seed=123,
                       iterations=iterations,
                       maximization=False,
                       problem_type='BINARY',
                       transfer_function=transfer,
                       binarization_method=bin_method,
                       alpha=alpha)

    logging.debug('COMENZANDO BUSQUEDA...\n')
    _hive.run(sols)
    return _hive


if __name__ == '__main__':

    for idx in range(len(sys.argv) - 1):
        name = sys.argv[idx].replace('-', '')
        value = ARGUMENTS.get(name)
        if value is not None:
            if isinstance(value, int):
                ARGUMENTS[name] = int(sys.argv[idx+1])
            ARGUMENTS[name] = sys.argv[idx + 1]

    logging.basicConfig(filename='scpsearch.log', level='DEBUG')
    logging.debug('INCIANDO COLMENA\n')
    logging.info(f'argumentos utilizados: {ARGUMENTS}')
    hive = solve_scp(**ARGUMENTS)

    print(hive.get_best()[2])
    logging.debug('BUSQUEDA FINALIZADA\n')
