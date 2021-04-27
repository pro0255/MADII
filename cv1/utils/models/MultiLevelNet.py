import numpy as np
import math
import pandas as pd
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS 
from labs.cv9.CONSTANTS import NUMBER_OF_STEPS, NUMBER_OF_TIMES, MOVE_TO_LAYER
import random

#KAPFTS1
#KAPFTS2
#KAPFTI1
#KAPFTI2

class MultiLevelNet:
    def __init__(self, matrix, actors, layers, layers_name = None, calculate=False, lab=8):
        self.lab = lab
        size = int(len(matrix) / layers)
        self.number_of_layers = layers
        self.multi_net = self.create_matrix(matrix, layers)
        self.actors = actors
        self.aindex2actor = {i:actors[i] for i in range(len(actors))}
        self.layers_name = layers_name
        self.calculate = calculate #do nothing at all :D

        self.df = self.calculate_res_dataframe()
        self.layer_df = self.calculate_layer_properties()

        self.save_df(self.df, 'multilayer.csv')
        self.save_df(self.layer_df, 'layer.csv')
        # print(self.multi_net)

    def calculate_layer_properties(self):
        d_result = {}
        for l in range(self.number_of_layers):
            l_n = self.layers_name[l]
            l_res = {}

            for i, a in enumerate(self.actors):
                l_a_d = self.degree_centrality(i, [l])
                excl_neig = self.exclusive_neighborhood(i, [l])
                excl_rel = self.exclusive_relevance(i, [l])
                l_res[self.aindex2actor[i]] = {'Degree': round(l_a_d, 3), 'Exclu. Nei': round(excl_neig, 3), 'Exclu. Rele': round(excl_rel, 3)} 
        
            d_result[l_n] = l_res


        properties = ['Degree','Exclu. Nei','Exclu. Rele']
        header = pd.MultiIndex.from_product([self.layers_name,
                                            properties],
                                            names=['Layer name','Property'])


        columns=['Degree deviation', 'Degree', 'Neighbors', 'Connective redudancy']
        data = np.zeros((len(self.actors), 3 * self.number_of_layers))

        for i, k_i in enumerate(d_result.keys()): #layers as key
            for j, prop in enumerate(properties):
                constructed_array = []
                for _, k_j in enumerate(d_result[k_i].keys()): #actors as key
                    value = d_result[k_i][k_j][prop]
                    constructed_array.append(value)
                position = i * len(properties) + j
                data[:, position] = constructed_array    
            
        df = pd.DataFrame(data, columns=header, index=self.actors)
        return df

    def exclusive_relevance(self, actor, L):
        nom = self.exclusive_neighborhood(actor, L)
        den = self.neighborhood_centrality(actor,self.generate_all())
        if den == 0:
            return 0
        return nom / den




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
            d_c_res.append(round(d_c, 3))
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
        return df

    def save_df(self, df, name):
        df.to_csv(f'{PATH_TO_OUTPUTS}cv{self.lab}/{name}', sep=';')


    def create_matrix(self, matrix, layers):
        full_size = len(matrix)
        layer_size = int(full_size / layers)
        self.layer_size = layer_size 

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
        same = self.degree_centrality(actor, L) / len(L)
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


    def flattening(self):
        flat_net = np.zeros((self.layer_size, self.layer_size))
        for x in range(self.layer_size):
            for y in range(self.layer_size):
                res = np.sum(self.multi_net[x, y, :])                
                flat_net[x, y] = 1 if res > 0 else 0
        print(pd.DataFrame(flat_net))


    def random_walk(self, v_start, l_start, all_layers, number_of_steps):
        history = [] #((v, l), (v, l)) ((from), (to))
        current_vertex = v_start #actor
        current_layer = l_start


     
        for step in range(number_of_steps):

            f = (current_vertex, current_layer)

            n = list(self.neighbors(current_vertex, [current_layer]))
            n.append(MOVE_TO_LAYER)
            choice = random.choice(n)

            if choice == MOVE_TO_LAYER:
                rem_layers = list(filter(lambda x: x != current_layer, all_layers))
                choice_layer = random.choice(rem_layers) 
                current_layer = choice_layer
                # print('move to another layer')
            else:
                current_vertex = choice
                # print('move to another vertex')
            # print(n)

            t = (current_vertex, current_layer)

            history.append((f, t))
        
        return history


    def resolve_ava_layers(self, actor_index):
        return self.generate_all()


    def occupation_centrality(self, walks, number_of_times = NUMBER_OF_TIMES):
        occupation_centrality_res = {actor_i: 0 for actor_i in walks.keys()}
        
        for actor_i in walks.keys():
            init_actor_walks = walks[actor_i]
            for walk_history in init_actor_walks:
                start = walk_history[0][0][0]
                end = walk_history[-1][1][0]
                occupation_centrality_res[end] += 1




        calculated = {actor_i:(occupation_centrality_res[actor_i]/(number_of_times*len(list(walks.keys())))) for actor_i, times in occupation_centrality_res.items()}

        return occupation_centrality_res, calculated


    def make_random_walks(self, number_of_steps = NUMBER_OF_STEPS, number_of_times = NUMBER_OF_TIMES):
        actors = list(range(len(self.actors)))
        # actors = [0]
        # print(actors)
        walks = {}
        for actor_index in actors:
            walks[actor_index] = []
            layers_to_start = self.resolve_ava_layers(actor_index)
            for walk_index in range(number_of_times):
                start_layer = random.choice(layers_to_start)
                random_walk_history = self.random_walk(actor_index, start_layer, layers_to_start, number_of_steps)
                walks[actor_index].append(random_walk_history)

        return self.occupation_centrality(walks)







    

    

    










    

    
