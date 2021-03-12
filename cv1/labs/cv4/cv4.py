import numpy as np
import pandas as pd
from constants.PATH_TO_DATASETS import KARATE_CLUB, PATH_TO_DATASETS
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS
from utils.models.AdjMatrix import AdjacencyMatrix
from utils.create_similarity_matrix import create_similarity_matrix
from utils.print_sim_matrix import print_sim_matrix
from utils.hierarchical_clustering import hierarchical_clustering
from labs.cv4.CONSTANTS import K, LINKAGE
import networkx as nx
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering




sklearn = True
resize = False
size = 6


def cv4():
    kc = pd.read_csv(f'{PATH_TO_DATASETS}{KARATE_CLUB}', ';')

    first_column = kc.iloc[:, 0]
    second_column = kc.iloc[:, 1]

    max_index_first = np.max(first_column)
    max_index_second = np.max(second_column)
    max_value = max_index_first if max_index_first > max_index_second else max_index_second  

    adj_matrix = AdjacencyMatrix(max_value, kc)
    numpy_matrix = adj_matrix.matrix

    if resize:
        numpy_matrix = numpy_matrix[0:size, 0:size]

    sim_matrix = create_similarity_matrix(numpy_matrix)
    if sklearn:
        res = AgglomerativeClustering(n_clusters=K, linkage=LINKAGE).fit_predict(sim_matrix)
        network_labels = {}
        for index in range(len(numpy_matrix)):
            network_labels[index] = {"hierarchical_cluster":res[index], "label": index+1}
        G = nx.from_numpy_matrix(numpy_matrix)
        nx.set_node_attributes(G, network_labels)
        nx.write_gexf(G, f'{PATH_TO_OUTPUTS}cv4/test_sklearn_{LINKAGE}.gexf')


    # print_sim_matrix(sim_matrix)
    matrix, clusters = hierarchical_clustering(sim_matrix)

    network_labels = {}
    for index in range(len(numpy_matrix)):
        for cluster_index, cluster in enumerate(clusters):
            if index in cluster:
                network_labels[index] = {"hierarchical_cluster":cluster_index, "label": index+1}
    G = nx.from_numpy_matrix(numpy_matrix)
    nx.set_node_attributes(G, network_labels)
    nx.write_gexf(G, f'{PATH_TO_OUTPUTS}cv4/clusters_{LINKAGE}.gexf')