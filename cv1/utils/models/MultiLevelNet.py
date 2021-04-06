import numpy as np

#KAPFTS1
#KAPFTS2
#KAPFTI1
#KAPFTI2

class MultiLevelNet:
    def __init__(self, matrix, labels, layers):
        size = int(len(matrix) / layers)
        self.multi_net = self.create_matrix(matrix, layers)
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










    

    
