from utils.radius_based import radius_based_logic
from utils.nearest_neighbors import nearest_neighbors_logic
import numpy as np


def radius_knn_combination(distance_matrix, epsilon, k, verbose=False):
    """Method which constructs network from vector data

    Args:
        data ([type]): [description]
        verbose (bool, optional): [description]. Defaults to False.
    """
    size = len(distance_matrix)

    if verbose:
        print(distance_matrix)

    adj_matrix = np.ones(shape=(size,size)) #symetric matrix
    adj_matrix = radius_based_logic(adj_matrix, distance_matrix, epsilon)
    return nearest_neighbors_logic(adj_matrix, distance_matrix, epsilon)