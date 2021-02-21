import numpy as np
from utils.eucladian_distance import eucladian_distance



def create_distance_matrix(data, verbose=False):
    size = len(data)
    
    if verbose:
        print(data)

    n_data = data.to_numpy()
    distance_matrix = np.zeros(shape=(size,size)) #symetric matrix
    for i in range(0, size):
        current_vector = n_data[i]
        for j in range(0, size):
            neighbor_vector = n_data[j]
            distance_matrix[i][j] = eucladian_distance(current_vector, neighbor_vector)
    return distance_matrix
