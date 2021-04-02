from utils.calc_modularity import resolve_c
import pandas as pd
from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS
import networkx as nx
import numpy as np

CLASS_KEY = 'variety'

pathKNN = 'knn3'
pathRADIUS = 'radius0.75'
pathCOMBINATION = 'combination3,0.75'

suffix_csv = '.csv'
suffix_gexf = '.gexf'

path = f'{PATH_TO_OUTPUTS}/cv1/'




def calculate_modularity_for_dataset(path, data, types, classes=None, minus=False):
    G = nx.read_gexf(path)
    graph_matrix = nx.to_numpy_matrix(G)
    m = len(G.edges())
    matrix_size = len(graph_matrix)
    suma = 0


    results = {}
    if classes is not None:
        classes_dic = create_dic_classes(classes) 
        Q_classes = calculate_modularity(classes_dic, graph_matrix, m)
        results['class'] = Q_classes

    for t in types:
        c_dic = create_dic_community(data, t, minus)
        Q = calculate_modularity(c_dic, graph_matrix, m)
        results[t] = Q
    return results


def calculate_modularity(c_dic, graph_matrix, m):
    matrix_size = len(graph_matrix)
    suma = 0
    for i in range(matrix_size):
        vector_i = graph_matrix[i]
        for j in range(matrix_size):
            vector_j = graph_matrix[j]
            k_i = np.sum(vector_i)
            k_j = np.sum(vector_j)
            d = (k_i * k_j) / (2*m)
            A_ij = graph_matrix[i, j]
            calc = (A_ij - d) * resolve_c(c_dic[i], c_dic[j])
            suma += calc
    Q = suma / (2*m)
    return Q

def create_dic_community(data, t, minus=False):
    community_data = data.loc[:, t].values
    ids = data.loc[:, columns[0]].values
    res = {}
    for i in range(len(ids)):
        index = ids[i]
        if minus:
            index -= 1
        res[index] = community_data[i] 
    return res




# def run_commands(path, c_dic, type):
#     print(type)
#     print(c_dic)
#     G = nx.read_gexf(path)
#     graph_matrix = nx.to_numpy_matrix(G)
#     m = len(G.edges())
#     matrix_size = len(graph_matrix)
#     suma = 0
    
#     for i in range(matrix_size):
#         vector_i = graph_matrix[i]
#         for j in range(matrix_size):
#             vector_j = graph_matrix[j]
#             k_i = np.sum(vector_i)
#             k_j = np.sum(vector_j)
#             d = (k_i * k_j) / (2*m)
#             A_ij = graph_matrix[i, j]
#             calc = (A_ij - d) * resolve_c(c_dic[i], c_dic[j])
#             suma += calc
#     Q = suma / (2*m)
#     print('modularity:', Q)
#     return Q







def create_dic_classes(data):
    return {i:data[i] for i in range(len(data))}


columns = ['Id', 'fast_greedy', 'edge_betweenness', 'louvain', 'optimal', 'label_prop']


def cv6():
    kc = pd.read_csv(f'{PATH_TO_DATASETS}KarateClub.csv', ';', header=None)
    first = kc.loc[:, 0]
    second = kc.loc[:, 1]
    tmp_m = np.zeros(shape=(34, 34))
    for i in range(len(second)):
        f = first[i] - 1
        s = second[i] - 1

        tmp_m[f][s] = 1
        tmp_m[s][f] = 1

    G_kc = nx.from_numpy_array(tmp_m)
    nx.write_gexf(G_kc, f'{PATH_TO_OUTPUTS}cv1/kc.gexf')


    if True:
        iris = pd.read_csv(f'{PATH_TO_DATASETS}iris.csv', ';')

        classes = iris.loc[:, CLASS_KEY].values
        
        data_knn = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/{pathKNN}{suffix_csv}', ';')
        data_raidus = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/radius{suffix_csv}', ';')
        data_combination = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/combination{suffix_csv}', ';')
        data_kc = pd.read_csv(f'{PATH_TO_OUTPUTS}/cv5/karateclub{suffix_csv}', ';')

        knn_graph_path = f'{path}{pathKNN}{suffix_gexf}'
        radius_graph_path = f'{path}{pathRADIUS}{suffix_gexf}'
        combination_graph_path = f'{path}{pathCOMBINATION}{suffix_gexf}'
        kc_graph_path = f'{path}kc{suffix_gexf}'

        classes_dic = create_dic_classes(classes)


        ##CSV for classes
        # df_classes = dict_to_df(classes_dic)
        # unique = df_classes.Class.unique()
        # mapper = {u:i for i, u in enumerate(unique)}
        # mapped = list(map(lambda v: mapper[v], df_classes['Class'].values))
        # df_classes['Class'] = mapped
        # df_classes.to_csv(f'{PATH_TO_OUTPUTS}cv6/classes.csv', index=False, header=True, sep=';')


        # type = columns[3]
        # run_commands(kc_graph_path, create_dic_community(data_kc, type, True), type) #karateclub

        res_kc = calculate_modularity_for_dataset(kc_graph_path, data_kc, [columns[1], columns[2], columns[3], columns[4], columns[5]], None, True)

        print(res_kc)


#columns = ['Id', 'fast_greedy', 'edge_betweenness', 'louvain', 'optimal', 'label_prop']
        res_knn = calculate_modularity_for_dataset(knn_graph_path, data_knn, [columns[1], columns[2]], classes)
        res_radius = calculate_modularity_for_dataset(radius_graph_path, data_raidus, [columns[1], columns[2]], classes)
        res_combination = calculate_modularity_for_dataset(combination_graph_path, data_combination, [columns[1], columns[2]], classes)


        df_knn = dict_to_df(res_knn)
        df_radius = dict_to_df(res_radius)
        df_combination = dict_to_df(res_combination)
        df_kc = dict_to_df(res_kc)



        df_knn.to_csv(f'{PATH_TO_OUTPUTS}cv6/knn.csv', header=True, sep=';')
        df_radius.to_csv(f'{PATH_TO_OUTPUTS}cv6/radius.csv', header=True, sep=';')
        df_combination.to_csv(f'{PATH_TO_OUTPUTS}cv6/combination.csv', header=True, sep=';')
        df_kc.to_csv(f'{PATH_TO_OUTPUTS}cv6/karateclub.csv', header=True, sep=';')



def dict_to_df(dic):
    df = pd.DataFrame(list(dic.items()),columns = ['Method', 'Modularity'])
    return df




    



    # calc_modularity()