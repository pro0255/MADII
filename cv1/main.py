import os
import pandas as pd
import numpy as np
from utils.nearest_neighbors import nearest_neightbors
from utils.radius_based import radius_based
from utils.eucladian_distance import eucladian_distance
from utils.create_distance_matrix import create_distance_matrix
from utils.radius_knn_combination import radius_knn_combination
from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS
from constants.EPSILON import EPSILON
from constants.K import K
import networkx as nx
import matplotlib.pyplot as plt


data = pd.read_csv(f'{PATH_TO_DATASETS}iris.csv', ';')
data_without_class = data.drop(['variety'], axis=1)


#dodelat kombinaci
#vizualizovat v gephi

for index, value in data_without_class.items():
     data_without_class.loc[:, index] = value.str.replace(',', '.').astype(float)

distance_matrix = create_distance_matrix(data_without_class)

adj_matrix_radius = radius_based(distance_matrix, EPSILON)
adj_matrix_knn = nearest_neightbors(distance_matrix, K)
adj_matrix_combination = radius_knn_combination(distance_matrix, EPSILON, K)


G_radius = nx.from_numpy_matrix(adj_matrix_radius)
G_knn = nx.from_numpy_matrix(adj_matrix_knn)
G_combination = nx.from_numpy_matrix(adj_matrix_combination)
# nx.set_node_attributes(G, network_labels)

# nx.draw(G_radius, with_labels=False)
# plt.show()


nx.write_gexf(G_radius, f'{PATH_TO_OUTPUTS}cv1/radius{EPSILON}.gexf')
nx.write_gexf(G_knn, f'{PATH_TO_OUTPUTS}cv1/knn{K}.gexf')
nx.write_gexf(G_combination, f'{PATH_TO_OUTPUTS}cv1/combination{K},{EPSILON}.gexf')

# nx.draw(G_knn, with_labels=False)
# plt.show()

