import numpy as np

#KAPFTS1
#KAPFTS2
#KAPFTI1
#KAPFTI2

class MultiLevelNet:
    def __init__(self, matrix, actors, layers, layers_name = None):
        size = int(len(matrix) / layers)
        self.multi_net = self.create_matrix(matrix, layers)
        self.actors = actors
        self.layers_name = layers_name
        # print(self.multi_net)


    def create_matrix(self, matrix, layers):
        full_size = len(matrix)
        layer_size = int(full_size / layers)
        metricies = np.zeros((layer_size, layer_size, layers))    
        for i in range(layers):            
            f = layer_size*i
            t = layer_size*(i+1)
            layer_matrix = matrix[f:t]
            metricies[:, :, i] = layer_matrix

        if(not np.all(metricies[0, :, 0] == matrix[0, :])):
            raise Exception("Preprocessing was not correct")

        return metricies

    def degree_centrality(self):
        pass

    def degree_deviation(self):
        pass

    def neighbors(self):
        pass

    def neighborhood_centrality(self):
        pass

    def connective_redundancy(self):
        pass

    def exclusive_neighborhood(self):
        pass

    

    










    

    
