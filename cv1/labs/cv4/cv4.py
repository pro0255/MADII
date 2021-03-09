import numpy as np
import pandas as pd
from constants.PATH_TO_DATASETS import KARATE_CLUB, PATH_TO_DATASETS
from utils.models.AdjMatrix import AdjacencyMatrix
from utils.create_similarity_matrix import create_similarity_matrix

def cv4():
    kc = pd.read_csv(f'{PATH_TO_DATASETS}{KARATE_CLUB}', ';')
    first_column = kc.iloc[:, 0]
    second_column = kc.iloc[:, 1]

    max_index_first = np.max(first_column)
    max_index_second = np.max(second_column)
    max_value = max_index_first if max_index_first > max_index_second else max_index_second  


    adj_matrix = AdjacencyMatrix(max_value, kc)
    numpy_matrix = adj_matrix.matrix
    sim_matrix = create_similarity_matrix(numpy_matrix)
    print(sim_matrix)
    input('Input to end cv4 completed ..')