import numpy as np
import math
import pandas as pd
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS 

#KAPFTS1
#KAPFTS2
#KAPFTI1
#KAPFTI2

class MultiLevelNet:
    def __init__(self, matrix, actors, layers, layers_name = None):
        size = int(len(matrix) / layers)
        self.number_of_layers = layers
        self.multi_net = self.create_matrix(matrix, layers)
        self.actors = actors
        self.layers_name = layers_name
        df = self.calculate_res_dataframe()
        # print(self.multi_net)

    def calculate_res_dataframe(self):
        d_res = []
        d_c_res = []
        neighborhood_res = []
        redudancy_res = []

        for i, a in enumerate(self.actors):
            
            L = list(range(self.number_of_layers))
            d = self.degree_centrality(i, L)
            d_c = self.degree_deviation(i, L)
            neighborhood = self.neighborhood_centrality(i, L)
            redudancy = self.connective_redundancy(i, L)            



            d_res.append(d)
            d_c_res.append(d_c)
            neighborhood_res.append(neighborhood)
            redudancy_res.append(round(redudancy, 3))


            # print(f'{a} {d}')
            # print(f'{a} {d_c}')
            # # print(f'{a} {neighbors}')
            # print(f'{a} {red}')
            # print(f'{a} {tmp}')
            # exit()

        columns=['Degree deviation', 'Degree', 'Neighbors', 'Connective redudancy']
        df = pd.DataFrame({columns[0]: d_c_res, columns[1]: d_res, columns[2]: neighborhood_res, columns[3]: redudancy_res},index=self.actors)
        df.to_csv(f'{PATH_TO_OUTPUTS}cv8/multilayer.csv', sep=';')




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

    def degree_centrality(self, actor, L):
        sum_matrix = np.sum(self.multi_net[:, :, L], axis=-1)
        actor_vector = sum_matrix[actor, :]
        degree = int(np.sum(actor_vector))
        return degree

    def degree_deviation(self, actor, L):
        same = self.degree_centrality(actor, L)
        s = 0
        for l in L:
            l_c = self.degree_centrality(actor, [l])
            # print(l_c)
            calc = pow(l_c - same, 2)
            s += calc
        res = s / len(L) 
        return math.sqrt(res)

    def generate_all(self):
        return list(range(self.number_of_layers))

    def neighbors(self, actor, L=None):
        L = L
        if L is None:
            L = self.generate_all()

        sum_matrix = np.sum(self.multi_net[:, :, L], axis=-1)
        actor_vector = sum_matrix[actor, :]
        neighbors = np.argwhere(actor_vector > 0)
        return neighbors.flatten()

    def neighborhood_centrality(self, actor, L):
        return len(self.neighbors(actor, L))


    def connective_redundancy(self, actor, L):
        nom = self.neighborhood_centrality(actor, L)
        den = self.degree_centrality(actor, L)
        x = 0
        if den != 0:
            x = nom / den  
        return 1 - x
        
    def exclusive_neighborhood(self, actor, L):
        xneighborhood = 0
        first = self.neighbors(actor, L)
        al = set(self.generate_all())
        i = set(L)
        res = al.difference(i)
        second = self.neighbors(actor, list(res))
        xneighborhood = set(first).difference(set(second))
        return len(list(xneighborhood))
    

    

    










    

    
