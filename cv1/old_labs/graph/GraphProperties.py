import pandas as pd
from old_labs.graph.Floyd import FloydAlgorithm
from old_labs.graph.AverageDistance import average_distance
from old_labs.graph.GraphAverage import graph_average
from old_labs.graph.ClosnessCentrality import calculate_closness_centrality
from old_labs.graph.ClusterCoefficient import calculate_cluster_coefficient, run_calculate_cluster_coefficient, calculcate_graph_transitivity
from old_labs.graph.DegreeDistribution import degree_distribution
from old_labs.graph.ConnectedComponents import connected_components
from collections import defaultdict, Counter
import numpy as np
from enum import Enum

verbose = False
DELIMITER = '=============================================================='

class GRAPH_PROPERTIES(Enum):
    GRAPH_AVERAGE = 'graph_average' ##prumer graf
    AVERAGE_DISTANCE = 'average_distance' ##prumarna vzdalenost v grafu
    MAX_DEGREE = 'max_degree' ##maximalni stupen v grafu
    MIN_DEGREE = 'min_degree' ##minimalni stupen v grafu
    AVG_DEGREE = 'avg_degree' ##prumerny stupen v grafu
    DEGREE_DISTRIBUTION = 'degree_distribution' ##distribuce stupnu v grafu (moznost histogramu)
    FLOYD_MATRIX = 'floyd_matrix' ##floyd matice - matice vzdalenosti
    ADJECENCY_MATRIX = 'adjecency_matrix' ##matice sousednosti
    GRAPH_TRANSITIVITY = 'graph_transitivity' ##tranzitivita grafu
    CLOSSNES_CENTRALITY = 'clossnes_centrality' ## centralita uzlu
    CLUSTER_COEFFICIENT = 'cluster_coefficient' ##shlukovaci koeficinet

class GRAPH_CONNECTED_COMPONENTS_PROPERTIES(Enum):
    NUMBER_OF_CONNECTED_COMPONENTS = 'number_of_connected_components' ##pocet komponent souvislosti
    MAX_CONNECTED_COMPONENT = 'max_connected_component' ##velikost nejvetsi komponenty souvislosti
    MIN_CONNECTED_COMPONENT = 'min_connected_component' ##velikost nejmensi komponenty souvislosti
    COMPONENTS = 'components' ##pole GRAPH_PROPERTIES pro kazdou nelezenou komponentu
    COMPONENTS_PROPERTIES = 'components_properties'
    COMPONENTS_SIZES = 'component_sizes'
    COMPONENTS_COUNTER = 'components_counter'
    COMPONENTS_GRAPH_AVERAGE_OVER_ALL = 'graph_average_over_all'


class GRAPH_INSPECTION(Enum):
    WHOLE = 'whole' ##cely graf - GRAPH_PROPERTIES
    CONNECTED_COMPONENTS = 'connected_components' ##pole - GRAPH_PROPERTIES

def create_connected_components_dictionary_for_graph(matrix):
    result = {}
    components, matrix = connected_components(matrix)
    result[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS] = components
    result["number_of_connected_components"] = len(components.keys())
    sizes = [len(v) for k,v in components.items()]
    c = Counter(sizes)
    result[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_SIZES] = sizes
    result[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_COUNTER] = c
    result["max_connected_component"] = max(sizes)
    result["min_connected_component"] = min(sizes)

    sorted_components_indicies = [sorted(value) for value in components.values()]
    subgraphs = []
    for subgraph_indicies in sorted_components_indicies:
        grid = np.ix_(subgraph_indicies, subgraph_indicies)
        subgraphs.append(matrix[grid])

    component_dics = []
    for sub_matrix in subgraphs:
        component_dic = create_graph_properties_dictionary(sub_matrix)
        component_dics.append(component_dic)

    result["components_properties"] = component_dics

    graph_average_list = [tmp[GRAPH_PROPERTIES.GRAPH_AVERAGE] for tmp in result["components_properties"]]   
    result["graph_average_over_all"] = sum(graph_average_list)/len(graph_average_list)

    return result


#!: Create output function for this dictionary
def create_graph_properties_dictionary(matrix):
    floyd = FloydAlgorithm()
    floyd_matrix = floyd.start(matrix)
    properties = {}
    properties[GRAPH_PROPERTIES.ADJECENCY_MATRIX] = matrix
    properties[GRAPH_PROPERTIES.FLOYD_MATRIX] = floyd_matrix
    properties[GRAPH_PROPERTIES.GRAPH_AVERAGE] = graph_average(floyd_matrix)[1]
    degree_value = degree_distribution(matrix)[1]
    properties[GRAPH_PROPERTIES.MAX_DEGREE] = degree_value[0]
    properties[GRAPH_PROPERTIES.MIN_DEGREE] = degree_value[1]
    properties[GRAPH_PROPERTIES.AVG_DEGREE] = degree_value[2]
    properties[GRAPH_PROPERTIES.DEGREE_DISTRIBUTION] = degree_value[3]
    properties[GRAPH_PROPERTIES.AVERAGE_DISTANCE] = average_distance(floyd_matrix)[1]

    closness_centrality_array = []
    for i in range(len(floyd_matrix)):
        calculate_closness_centrality_output, calculate_closness_centrality_value = calculate_closness_centrality(floyd_matrix, i, verbose)
        closness_centrality_array.append(calculate_closness_centrality_value)

    properties[GRAPH_PROPERTIES.CLOSSNES_CENTRALITY] = closness_centrality_array

    cluster_coefficient_array = []
    for i in range(len(matrix)):
        value = calculate_cluster_coefficient(matrix, i, verbose)
        cluster_coefficient_array.append(value)

    properties[GRAPH_PROPERTIES.CLUSTER_COEFFICIENT] = cluster_coefficient_array
    properties[GRAPH_PROPERTIES.GRAPH_TRANSITIVITY] = sum(cluster_coefficient_array)/len(matrix)

    return properties

def make_graph_inspection(matrix):
    dic = {}
    dic[GRAPH_INSPECTION.WHOLE] = create_graph_properties_dictionary(matrix)
    dic[GRAPH_INSPECTION.CONNECTED_COMPONENTS] = create_connected_components_dictionary_for_graph(matrix)
    return dic


###############################################################################################



    