import numpy as np

class FloydAlgorithm():
    def __init__(self):
        pass

    def start(self, adjacency_matrix):
        number_of_vertecies = len(adjacency_matrix)

        floyd_matrix = np.full(adjacency_matrix.shape, np.inf)
        for i in range(len(floyd_matrix)):
            floyd_matrix[i][i] = 0

        for i in range(len(floyd_matrix)):
            for j in range(len(floyd_matrix)):
                if adjacency_matrix[i][j] != 0:
                    floyd_matrix[i][j] = adjacency_matrix[i][j]


        for k in range(number_of_vertecies):
            for i in range(number_of_vertecies):
                for j in range(number_of_vertecies):
                    first = floyd_matrix[i][j]
                    second = floyd_matrix[i][k]
                    third = floyd_matrix[k][j]

                    if first > second + third:
                        floyd_matrix[i][j] = second + third

        return floyd_matrix