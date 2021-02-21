import numpy as np
from utils.eucladian_distance import eucladian_distance


def radius_based(distance_matrix, epsilon, verbose=False):
    """Method which constructs network from vector data

    Args:
        data ([type]): [description]
        verbose (bool, optional): [description]. Defaults to False.
    """
    size = len(distance_matrix)
    if verbose:
        print(distance_matrix)
    adj_matrix = np.zeros(shape=(size,size)) #symetric matrix
    return radius_based_logic(adj_matrix, distance_matrix, epsilon)


def radius_based_logic(adj_matrix, distance_matrix, epsilon):
    size = len(distance_matrix)
    for y in range(size):
        for x in range(size):
            if distance_matrix[y][x] < epsilon:
                adj_matrix[y][x] = 1
    return adj_matrix



