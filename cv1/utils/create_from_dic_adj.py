import numpy as np

def create_from_dic_adj(G):
    size = len(G.keys())
    adj = np.zeros(shape=(size, size))
    for k, v in G.items():
        for vertex in v:
            adj[k][vertex] = 1
            adj[vertex][k] = 1
    return adj






