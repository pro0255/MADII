

from labs.cv10.CONSTANTS import SAMPLE_SIZE
from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS
import pandas as pd
import networkx as nx
import random
from old_labs.graph.GraphProperties import make_graph_inspection
from old_labs.graph.printer.GraphInspectionPrinter import write_graph_inspection_to_file
from old_labs.graph_api.GraphMaker import GraphMaker
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

def get_graph_size(G, size):
    return int(len(G.nodes()) * size)

def random_node_sampling(G, size=SAMPLE_SIZE):
    """
        • Na počátku musíme stanovit velikost vzorku S.
        • Vyber (zahrň) do vzorku S náhodně vybraný vrchol i.
        • Každý vrchol je do vzorku zařazen s uniformní pravděpodobností 1/n.
        • Následně do vzorku přidej hrany ES = {(u, v) ∈ E|u ∈ VS, v ∈ VS} (tedy z
        původního grafu jsou ponechány pouze hrany mezi vrcholy z množiny
        VS).
        • Metodu je vhodná k poskytnutí objektivního odhadu průměrného
        stupně nebo distribuce stupňů velké sítě.
    """
    #s nějakou pravděpodobností přidávat vrcholy a nakonec mezi nimi dodělat hrany..
    sample_vertex_size = get_graph_size(G, size)
    verticies = random.choices(list(G.nodes()), k=sample_vertex_size)
    sample_G = G.subgraph(verticies)
    return sample_G


def random_edge_sampling(G, size=SAMPLE_SIZE):
    """
        • Provádí výběr hran s uniformní pravděpodobností ∼d(u)/2m a přidává
        je do vzorku ES ⊆ E tak dlouho, dokud vzorek není dostatečně velký.
        • Výběr vrcholů není nezávislý, protože do vzorku jsou vybrány oba
        krajní vrcholy hrany.
        • Kvůli zkreslení stupně vrcholů je statistika uzlů zkreslená ve prospěch
        uzlů s vysokým stupněm.
        • Statistiky hran zkreslené nejsou (kvůli uniformnímu výběru hran).
        • RE nedokáže zachovat mnoho požadovaných vlastností, např.
        nezachová komunitní strukturu a souvislost.
    """
    #náhodná hrana a incidentní vrcholy nacpat dovnitř..
    sample_G = nx.Graph()
    sample_vertex_size = get_graph_size(G, size)

    while len(sample_G.nodes()) <= sample_vertex_size:
        # print(len(sample_G.nodes()))
        possible_choices = list(filter(lambda tuple_edge: tuple_edge not in sample_G.edges(), G.edges()))
        choice = random.choice(possible_choices)

        for vertex in choice:
            current_verticies = sample_G.nodes()
            if vertex not in current_verticies:
                sample_G.add_node(vertex)

        sample_G.add_edge(*choice)

    return sample_G

PROPERTIES = ["Len V", 'Len E', 'Avg D', 'Conntected Components']


def get_cumulative_degree_distribution(nodes, degrees):
    c = Counter(degrees)
    suma = np.sum(list(c.values()))
    sorted_degrees = sorted(c.items())
    size, times = zip(*sorted_degrees)    
    freq = [t/suma for t in times]

    cum_freq = [0]

    for f_i, f_v in enumerate(freq[0:len(freq)]):
        cum_freq.append(cum_freq[f_i] + f_v)

    return list(size) + [size[-1] + 1], list(cum_freq) 



def create_prop_dic(G, properties, name_save):
    res = {}

    nodes, degrees = list(zip(*G.degree()))
    x, y =get_cumulative_degree_distribution(nodes, degrees)
    plt.plot(x,y)
    plt.savefig(f'{PATH_TO_OUTPUTS}cv10/{name_save}.jpg')
    plt.clf()

    m = len(G.edges())
    n = len(G.nodes())
    avg = m/n
    cc = nx.connected_components(G)

    res[properties[0]] = len(G.nodes())
    res[properties[1]] = len(G.edges())
    res[properties[2]] = round(avg, 3)
    res[properties[3]] = len(list(cc))
    return res

def create_df_according_to_lab(original, rn, re):
    properties = PROPERTIES
    header = ['Original', 'RN', 'RE']
    
    original_d = create_prop_dic(original, properties, header[0])
    rn_d = create_prop_dic(rn, properties, header[1])
    re_d = create_prop_dic(re, properties, header[2])

    merged = (original_d, rn_d, re_d)
    data = np.zeros((len(properties), len(header)))

    for i in range(len(merged)):
        constructed_value = []
        for prop_i, prop in enumerate(properties):
            value = merged[i][prop]
            constructed_value.append(value)
        data[:, i] = constructed_value

    df = pd.DataFrame(data, columns=header, index=properties)
    return df

#http://networkrepository.com/bio-CE-CX.php

PATH = f'{PATH_TO_DATASETS}/network/bio-CE-CX.edges'

def cv10():
    edges = pd.read_csv(PATH, sep=' ', header=None)
    init_G = nx.from_pandas_edgelist(edges, 0, 1)

    # print(create_prop_dic(init_G, PROPERTIES))
    rns_G = random_node_sampling(init_G)
    re_G = random_edge_sampling(init_G)


    # rns_G_inspection = make_graph_inspection(rns_G.to_numpy_array())
    # re_G_inspection = make_graph_inspection(re_G.to_numpy_array())

    # rns_G_gmaker = GraphMaker(rns_G_inspection)
    # re_G_inspection = GraphMaker(re_G_inspection)

    # rns_G_gmaker.plot_components_distribution()
    # re_G_inspection.plot_components_distribution()

    # write_graph_inspection_to_file(rns_G_inspection, f'{PATH_TO_OUTPUTS}cv10/randomNodeInspection.txt')
    # write_graph_inspection_to_file(re_G_inspection, f'{PATH_TO_OUTPUTS}cv10/randomNodeInspection.txt')
    df = create_df_according_to_lab(init_G, rns_G, re_G)
    df.to_csv(f'{PATH_TO_OUTPUTS}cv10/properties.csv', sep=';')
    nx.write_gexf(rns_G, f'{PATH_TO_OUTPUTS}cv10/randomNode.gexf')
    nx.write_gexf(re_G, f'{PATH_TO_OUTPUTS}cv10/randomEdge.gexf')
