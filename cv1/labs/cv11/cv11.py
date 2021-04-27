
import pandas as pd
from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
import numpy as np
import networkx as nx
from utils.models.MultiLevelNet import MultiLevelNet

"""
    Zvážit rozdělení na snapshoty..
    Reprezentuje kontakty lidí, během 2,5 dne.. (rozsekání na 5 snaphotů)
    Jde vyčíst z dat, kdy den končí, a kdy začíná? 
    Vytvořit report s výsledky analýzy.. vizualizovat vrstvy, nebo snapshoty..
    Vizualizovat komunitní stukturu, co všechno do analýzy zahrnout?

    Lze na to jít pomocí vícevrstvé analýza sítě. Takže si veme nějaký interval a prohlasíme
    to jako vrstvu..
"""


#http://www.sociopatterns.org/datasets/hypertext-2009-dynamic-contact-network/
def from_df_g(sub_df):
    G = nx.from_pandas_edgelist(sub_df, 1, 2)

    # print('nodes', len(G.nodes()))
    # print('edges', len(G.edges()))

    return G



def create_sub_df(step, index, last_end_index, data, last=False):
    end_value = index * step
    time_values = data.iloc[:, 0].values

    find_value = end_value
    v = None
    while True:
        v = np.argwhere(time_values == find_value).flatten()
        if(len(v) > 0):
            break
        find_value -= 20

    f_i = int(last_end_index) #from index
    t_i = int(v[-1] + 1) #to index 

    sub_df = data.iloc[f_i:t_i, :]
    my_end_index = t_i
    return sub_df, my_end_index



def cv11():
    TIME_MAX = int(2.5 * 24 * 60 * 60)
    NUMBER_OF_STEPS = 5
    TIME_STEP = int(TIME_MAX / NUMBER_OF_STEPS)


    path = f'{PATH_TO_DATASETS}/contact/ht09_contact_list.txt'
    data = pd.read_csv(path, sep='\t', header=None)

    sub_dfs = []
    last_end_index = 0



    nodes_ids_1 = data.iloc[:, 1]
    nodes_ids_2 = data.iloc[:, 2]
    

    nodes_ids = np.unique(np.array(list(np.unique(nodes_ids_1)) +  list(np.unique(nodes_ids_2)))) 


    for i in range(NUMBER_OF_STEPS):
        transformed_i = i + 1
        sub_df, last_end_index = create_sub_df(TIME_STEP, transformed_i, last_end_index, data)
        sub_dfs.append(sub_df)

    Gs = []

    #create Gs
    for s_df in sub_dfs:
        s_G = from_df_g(s_df)
        Gs.append(s_G)

    #append not existing actors to Gs
    for current_G in Gs:
        current_nodes = current_G.nodes() 
        need_to_append = list(filter(lambda x: x not in current_nodes, nodes_ids)) 

        for node_to_append in need_to_append:
            current_G.add_node(node_to_append)


    

    


    # for g in Gs:
    #     print(np.argwhere(nx.to_numpy_matrix(g) > 1))

    # print(pd.DataFrame(nx.to_numpy_matrix(Gs[0]), index=Gs[0].nodes()))
    # print(pd.DataFrame(nx.to_numpy_matrix(Gs[1]), index=Gs[0].nodes()))
    # print(layer_labels)


    labels = list(Gs[0].nodes())
    layer_labels = [f'{i*TIME_STEP}-{int((i+1)*TIME_STEP)}[sec]' for i in range(NUMBER_OF_STEPS)]



    matrix_all = None
    i = 0
    while i < (len(Gs)):
        if i == 0:
            # 0  1
            matrix_all = np.vstack((nx.to_numpy_matrix(Gs[i]), nx.to_numpy_matrix(Gs[i+1])))
            i += 1
        else:
             matrix_all = np.vstack((matrix_all, nx.to_numpy_matrix(Gs[i])))
            # x 2
        i += 1




    ml_net = MultiLevelNet(matrix_all, labels, NUMBER_OF_STEPS, layer_labels, False, 11)
