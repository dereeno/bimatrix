from numpy.linalg import slogdet, matrix_rank, det
import sys
from copy import copy


def is_singular(m): return not is_square(m) or not is_full_rank(m)

def is_square(m): return m.shape[0] == m.shape[1]

def is_full_rank(m): return matrix_rank(m) == m.shape[0]

def sign_of_matrix(matrix):
    if not is_square(matrix):
        return 0

    shape = matrix.shape[0]
    sign = slogdet(matrix)[0] # get the sign of the determinant of 'matrix'
    i = 0
    while sign == 0 and i < shape:
        sign = (-1) * slogdet(replace_column_by_1(matrix, i))[0]
        i = i+1

    return sign

def replace_column_by_1(matrix, index):
    clone = copy(matrix)
    clone[:, index] = 1 # replace column 'index' by the vector 1.
    return clone