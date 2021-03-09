import numpy as np
from utils.calc_similarity import calc_similarity

def create_similarity_matrix(matrix):
    sim_matrix = np.zeros(shape=(matrix.shape))
    for y in range(matrix.shape[0]):
        current_y = matrix[y, :]
        for x in range(y, matrix.shape[1]):
            current_x = matrix[x, :]
            sim = calc_similarity(current_y, current_x)
            sim_matrix[y][x] = sim
            sim_matrix[x][y] = sim
    return sim_matrix






