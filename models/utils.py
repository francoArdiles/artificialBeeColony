from typing import Iterable

import numpy as np

V_SHAPE_INTEGRAL = 0
V_SHAPE_TANH = 1
V_SHAPE_SQRT = 2
V_SHAPE_ARCTAN = 3


def s_shape(x: np.array, variable):
    return 1/(1 + np.power(np.e, x*variable))


def v_shape(x, v_shape_type):
    if v_shape_type == V_SHAPE_INTEGRAL:
        raise NotImplementedError('Función integral no implementada')
    elif v_shape_type == V_SHAPE_TANH:
        return np.abs(np.tanh(x))
    elif v_shape_type == V_SHAPE_SQRT:
        return np.abs(x/np.sqrt(1+np.power(x, 2)))
    else:
        return np.abs((2/np.pi) * np.arctan((np.pi*x)/2))


def transform(solution: np.array, transformation_type='CONTINUOUS',
              transfer_function='2SHAPE_2D', binarization_method='STANDARD',
              alpha=None):

    if transformation_type == 'CONTINUOUS':
        return solution
    if transformation_type == 'BINARY':
        if transfer_function == 'S_SHAPE_2D':
            value = s_shape(solution, -2)
            pass
        elif transfer_function == 'S_SHAPE_D/2':
            value = s_shape(solution, -1)
        elif transfer_function == 'S_SHAPE_2D/3':
            value = s_shape(solution, -1/2)
        elif transfer_function == 'S_SHAPE_2D':
            value = s_shape(solution, -1/3)
        elif transfer_function == 'V_SHAPE_INTEGRAL':
            value = v_shape(solution, V_SHAPE_INTEGRAL)
        elif transfer_function == 'V_SHAPE_TANH':
            value = v_shape(solution, V_SHAPE_TANH)
        elif transfer_function == 'V_SHAPE_SQRT':
            value = v_shape(solution, V_SHAPE_SQRT)
        elif transfer_function == 'V_SHAPE_ARCTAN':
            value = v_shape(solution, V_SHAPE_ARCTAN)
        else:
            raise ValueError(f'Selected transfer method does not exist: '
                             f'{transfer_function}')
        return binarization(value, binarization_method, alpha)

    elif transformation_type == 'DISCRETE':
        raise NotImplementedError(
            'There is not discretization methods implemented'
        )
    else:
        raise ValueError(
            f'Transformation type does not exist: {transformation_type}'
        )


def binarization(solution: np.array, bin_type, alpha=None):
    rng = np.random.random(size=solution.size)
    if bin_type == 'standard':
        return np.array(rng <= solution, dtype=int)
   elif bin_type == 'complement':
        """raise NotImplementedError('Binarización por complemento no '
                                  'implementada.')"""
        if(rng<=transfer function(d,j,w)){
            return 1;
        }
        return 0;
    elif bin_type == 'static_probability':
        """assert alpha is not None
        raise NotImplementedError(
            
        )"""
        if(transfer function(d,j,w)<=a){
           return0; 
        }else{
            if((a<transfer function(d,j,w)&&(transfer function(d,j,w)<=(1/2)*(1+a))){
                return binarizar(j,w);
            }
        }else{
            if(transfer function(d,j,w)>=(1/2)*(1+a))
            return 1;
        }
        
    elif bin_type == 'elitist':
        """raise NotImplementedError(
            'Binarización por metodo elitista no implementado'
        )"""
        if(rand<transfer function(d,j,w)){
            return(j,best);
        }
        return 0;
    elif bin_type == 'elitist_roulette':
        """raise NotImplementedError(
            'Binarización por metodo elitista no implementado'
        )"""
        if(a<transfer function(d,j,w)){
            return
        }
        return       
    else:
        raise ValueError(
            f'Binarization method does not exists {bin_type}'
        )


