import networkx as nx
import random



def link_selection(G_0, n):
    t = 0
    G = G_0        
    while t < n:
        addingI = len(G.nodes())
        G.add_node(addingI)
        choice_edge = random.choice(list(G.edges()))
        edge_to_connect = random.choice(choice_edge)
        G.add_edge(addingI, edge_to_connect)
        t += 1
    return G