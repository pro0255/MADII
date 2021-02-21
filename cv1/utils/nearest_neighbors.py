import numpy as np




def nearest_neightbors(distance_matrix, k, verbose=False):
    """Method which constructs network from vector data

    Args:
        data ([type]): [description]
        verbose (bool, optional): [description]. Defaults to False.
    """
    size = len(distance_matrix)
    if verbose:
        print(distance_matrix)
    adj_matrix = np.zeros(shape=(size,size)) #symetric matrix
    return nearest_neighbors_logic(adj_matrix, distance_matrix, k)


def nearest_neighbors_logic(adj_matrix, distance_matrix, k):
    for node_index, node in enumerate(distance_matrix):
        indicies = np.argsort(node)[1:k+1]
        for s_i in indicies:
            if s_i == node_index:
                continue
            adj_matrix[node_index][s_i] = 1
    return adj_matrix
