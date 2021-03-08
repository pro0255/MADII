import networkx as nx
import random
import numpy as np



def link_selection(G_0, n, internal_links_P = -1):
    t = 0
    G = G_0        
    while t < n:
        #internal links
        internal_random = np.random.uniform()
        if internal_random < internal_links_P:
            print(f'internal links in time: {t}')
            random_choice = random.choice(list(G.nodes()))
            v_l = len(G.nodes())
            neigh = list(G.neighbors(random_choice))
            not_connected = [v for v in G.nodes() if v not in neigh and v != random_choice]
            if len(not_connected) > 0:
                second_v = random.choice(not_connected)
                G.add_edge(random_choice, second_v)


        addingI = len(G.nodes())
        G.add_node(addingI)
        choice_edge = random.choice(list(G.edges()))
        edge_to_connect = random.choice(choice_edge)
        G.add_edge(addingI, edge_to_connect)




        t += 1
    return G