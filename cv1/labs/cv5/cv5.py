import networkx as nx
import pandas as pd
from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS
import matplotlib.pyplot as plt
from collections import Counter

pathKNN = 'knn3'
pathRADIUS = 'radius0.75'
pathCOMBINATION = 'combination3,0.75'

suffix_csv = '.csv'
suffix_gexf = '.gexf'

path = f'{PATH_TO_OUTPUTS}/cv1/'

def set_and_save(G, modularity, types, name):
    network_labels = {}
    l = len(G.nodes())
    types = types + ['label']
    for vertex_id in range(l):
        network_labels[vertex_id] = {str(t):(modularity.loc[:, t].values[vertex_id] if t != 'label' else vertex_id+1) for t in types}
        #t:modularity.loc[:, t].values[vertex_id] for t in types
        # network_labels[vertex_id]['label'] = vertex_id
    print(network_labels)
    nx.set_node_attributes(G, network_labels)
    print(G.nodes())
    exit()
    attributes = nx.get_node_attributes(G, "fast_greedy")
    nx.write_gexf(G, f'{PATH_TO_OUTPUTS}cv5/{name}.gexf')


def cv5():
    data_knn = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/{pathKNN}{suffix_csv}', ';')
    data_raidus = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/radius{suffix_csv}', ';')
    data_combination = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/combination{suffix_csv}', ';')
    data_kc = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/KarateClub{suffix_csv}', ';')

    types = list(data_knn.columns)[1:len(list(data_knn.columns))]


    #load gexf data
    G_knn = nx.read_gexf(f'{path}{pathKNN}{suffix_gexf}')
    G_radius = nx.read_gexf(f'{path}{pathRADIUS}{suffix_gexf}')
    G_combination = nx.read_gexf(f'{path}{pathCOMBINATION}{suffix_gexf}')

    # print(len(G_knn.nodes()))
    # print(len(G_radius.nodes()))
    # print(len(G_combination.nodes()))
    # print(len(data_knn))
    # print(len(data_raidus))
    # print(len(data_combination))


    #Load data from data frame - cluster method results
    print_to(data_knn, f'{PATH_TO_OUTPUTS}/cv5/knn', create_types(data_knn))
    print_to(data_raidus, f'{PATH_TO_OUTPUTS}/cv5/radius', create_types(data_raidus))
    print_to(data_combination, f'{PATH_TO_OUTPUTS}/cv5/combination', create_types(data_raidus))
    print_to(data_kc, f'{PATH_TO_OUTPUTS}/cv5/karateclub', create_types(data_kc))

    # set_and_save(G_knn, data_knn, create_types(data_knn), 'knn')
    # set_and_save(G_radius, data_raidus, create_types(data_raidus), 'radius')
    # set_and_save(G_combination, data_combination, create_types(data_combination), 'combination')


def print_to(data, filename, types):
    for t in types:
        arr = data.loc[:, t].values
        c_0 = Counter(arr)
        c_1 = Counter(c_0.values())
        x = list(c_1.keys())
        y = list(c_1.values())
        plt.xticks(x,x)
        plt.title(t)
        plt.xlabel('velikost')
        plt.ylabel('freq')
        plt.bar(x, y, color='green', edgecolor='black')
        plt.savefig(f'{filename}/{t}.png')
        plt.clf()



def create_types(data):
    return list(data.columns)[1:len(list(data.columns))]