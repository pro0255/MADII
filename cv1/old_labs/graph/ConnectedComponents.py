from collections import defaultdict 
import numpy as np


def connected_components(a_matrix):
    """Matrix represents graph. It is a adjacency matrix.
    Args:
        matrix (bool[][]): Adjacency matrix.
    """
    visited_vertecies = []
    components = defaultdict(list)
    number_of_verticies = len(a_matrix)
    count = 0

    for vertex_index in range(number_of_verticies):
        if vertex_index not in visited_vertecies:
            subgraph_indicies = [] 
            DFS(subgraph_indicies, vertex_index, visited_vertecies, a_matrix)
            components[count] = subgraph_indicies
            count += 1
    return (components, a_matrix)


def get_neigh_indicies(vertex_index, a_matrix):
    row = np.squeeze(a_matrix[vertex_index])
    filtered = np.argwhere(row > 0).reshape(-1)
    return filtered


def DFS(array, vertex, visited_vertecies, a_matrix):
    visited_vertecies.append(vertex)
    array.append(vertex)

    neighboors_indicies = get_neigh_indicies(vertex, a_matrix)
    for neigh_index in neighboors_indicies:
        if neigh_index not in visited_vertecies:
            DFS(array, neigh_index, visited_vertecies, a_matrix)






