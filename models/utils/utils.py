from typing import Iterable, Union
from math import erf
import numpy as np

V_SHAPE_ERF = 0
V_SHAPE_TANH = 1
V_SHAPE_SQRT = 2
V_SHAPE_ARCTAN = 3


def s_shape(x: np.array, variable):
    return 1/(1 + np.power(np.e, x*variable))


def v_shape(x, v_shape_type):
    if v_shape_type == V_SHAPE_ERF:
        return np.abs(np.array(list(map(lambda i: erf(i), x))))
    elif v_shape_type == V_SHAPE_TANH:
        return np.abs(np.tanh(x))
    elif v_shape_type == V_SHAPE_SQRT:
        return np.abs(x/np.sqrt(1+np.power(x, 2)))
    else:
        return np.abs((2/np.pi) * np.arctan((np.pi*x)/2))


def transform(solution: np.array, transformation_type='CONTINUOUS',
              transfer_function='2SHAPE_2D', **kwargs):

    if transformation_type == 'CONTINUOUS':
        return solution
    if transformation_type == 'BINARY':
        if transfer_function == 'S_SHAPE_2D':
            value = s_shape(solution, -2)
            pass
        elif transfer_function == 'S_SHAPE_D':
            value = s_shape(solution, -1)
        elif transfer_function == 'S_SHAPE_D/2':
            value = s_shape(solution, -1/2)
        elif transfer_function == 'S_SHAPE_D/3':
            value = s_shape(solution, -1/3)
        elif transfer_function == 'V_SHAPE_INTEGRAL':
            value = v_shape(solution, V_SHAPE_ERF)
        elif transfer_function == 'V_SHAPE_TANH':
            value = v_shape(solution, V_SHAPE_TANH)
        elif transfer_function == 'V_SHAPE_SQRT':
            value = v_shape(solution, V_SHAPE_SQRT)
        elif transfer_function == 'V_SHAPE_ARCTAN':
            value = v_shape(solution, V_SHAPE_ARCTAN)
        else:
            raise ValueError(f'Selected transfer method does not exist: '
                             f'{transfer_function}')
        return value
    elif transformation_type == 'DISCRETE':
        raise NotImplementedError(
            'There is not discretization methods implemented'
        )
    else:
        raise ValueError(
            f'Transformation type does not exist: {transformation_type}'
        )


def binarize(solution: np.array,
             bin_type: str,
             alpha: Union[float, None] = None,
             original_solution: Union[np.array, None] = None,
             best_solution: Union[np.array, None] = None,
             rng=None,
             **kwargs):
    """
    Binariza una solución transformada.
    :param solution: Solución transformada.
    :param bin_type: Tipo de binarización.
    :param alpha: valor de probabilidad estática.
    :param original_solution: solucion que genera la actual.
    :param best_solution: mejor solucion conocida.
    :param rng: generador de valores aleatorios.
    :param kwargs:
    :return: Solución binarizada.
    """
    bin_type = bin_type.upper()
    if not rng:
        rnd_vector = np.random.random(size=solution.size)
    else:
        rnd_vector = rng.random(size=solution.size)
    new_solution = np.copy(solution)
    if bin_type == 'STANDARD':
        return np.array(rnd_vector <= solution, dtype=int)
    elif bin_type == 'COMPLEMENT':
        # idx = np.where(new_solution[rng <= new_solution])
        # new_solution[idx] = abs(original_solution[idx] - 1)
        new_solution[rnd_vector <= new_solution] = abs(
            original_solution[rnd_vector <= new_solution] - 1)
        mask = np.ones(new_solution.size, dtype=bool)
        mask[rnd_vector <= new_solution] = False
        new_solution[mask] = 0
        return new_solution
    elif bin_type == 'STATIC_PROBABILITY':
        assert alpha is not None
        assert best_solution is not None
        new_solution[new_solution <= alpha] = 0
        new_solution[new_solution >= (1 + alpha)/2] = 1
        idx = np.where(np.logical_and(new_solution > alpha, new_solution <= (
                1 + alpha)/2))

        new_solution[
            np.logical_and(
                new_solution > alpha,
                new_solution <= (1 + alpha)/2)
        ] = original_solution[np.logical_and(new_solution > alpha,
                                             new_solution <= (1 + alpha)/2)]
        # new_solution[idx] = original_solution[idx]
        return new_solution
    elif bin_type == 'ELITIST':
        new_solution[rnd_vector < new_solution] = best_solution[rnd_vector <
                                                                new_solution]
        new_solution[rnd_vector >= new_solution] = 0
        return new_solution
    elif bin_type == 'ELITIST_ROULETTE':
        raise NotImplementedError(
            'Binarización por metodo elitista no implementado'
        )
    else:
        raise ValueError(
            f'Binarization method does not exists {bin_type}'
        )


