import numpy as np

class AdjacencyMatrix():
    def __init__(self, size, data):
        self.matrix = np.zeros((size, size))
        self.create(data)
    
    def create(self, data):
        for row_index in range(data.shape[0]):
            row = data.iloc[row_index, :]
            self.matrix[row[0]-1, row[1]-1] += 1
            self.matrix[row[1]-1, row[0]-1] += 1


    def __str__(self):
        output = ""
        for index, row in enumerate(self.matrix):
            degree = np.sum(row == 1)
            vertex_id = index + 1
            output += f"Id: {vertex_id} - stupen {degree}\n" 
        return output
