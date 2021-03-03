import numpy as np

def calculate_closness_centrality(floyd_matrix, i, verbose=False):
    result = 0
    numerator = len(floyd_matrix[i])
    denominator = np.sum(floyd_matrix[i])
    if denominator:
        result = numerator / denominator

    
    o = f'ID {i+1} - clossnes centraility {result}'
    output = f'{o}\n'
    if verbose:
        print(o)
    return (output, result)