import numpy as np

def save_matrix_to_file(filename, matrix):
    with open(filename, 'wb') as f:
        np.save(f, matrix)
