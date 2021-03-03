
import numpy as np
from labs.cv2.CONSTANTS import TIMESTAMP
import random







def holme_kim(m_0, n, m, P_t):
    """
    Extension of the standard scale-free network (Barabasi-Albert) model to include a “triad formation step.”
    
    """
    G = {i:[] for i in range(m_0)}
    list_verticies = [i for i in range(m_0)]
    t = 0
   

    while(t < n):
        pa_addition = []
        counter = 1
        adding_index = len(G.keys())
        res, last_pa_vertex = pa_step(G, list_verticies, 1, adding_index)
        pa_addition += last_pa_vertex
        G = res[0]
        list_verticies = res[1]
        while counter < m:
            r = random.uniform(0 , 1)
            if r < P_t:
                neigh_w = G[pa_addition[len(pa_addition) - 1]]
                v = []
                if adding_index in G.keys():
                    v = G[adding_index]
                not_connected = [w_v for w_v in neigh_w if w_v not in v and w_v != adding_index]
                if len(not_connected) > 0:
                    G, list_verticies = tf_step(G, list_verticies, not_connected, adding_index)
                else:
                    res, last_pa_vertex = pa_step(G, list_verticies, 1, adding_index)
                    G = res[0]
                    list_verticies = res[1]
            else:
                res, last_pa_vertex = pa_step(G, list_verticies, 1, adding_index)
                G = res[0]
                list_verticies = res[1]
            counter += 1
        t += 1
    return G



def select_m(list_verticies, m, adding):
    res = []
    while len(res) < m:
        vertex = random.choice(list_verticies)
        if vertex not in res and vertex != adding:
            res.append(vertex)
    return res

def pa_step(G, list_verticies, m, adding_index):

    verticies = select_m(list_verticies, m, adding_index)
    new_vertex = adding_index
    if new_vertex in G.keys():
        G[new_vertex] += verticies
    else:
        G[new_vertex] = verticies
    [G[vertex].append(new_vertex) for vertex in verticies]
    list_verticies = list_verticies + verticies + ([new_vertex] * m)
    return ((G, list_verticies), verticies)

def tf_step(G, list_verticies, not_connected, adding_index):
    r = random.choice(not_connected)
    if adding_index in G.keys():
        G[adding_index].append(r)
    else:
        G[adding_index] = [r]
    G[r].append(adding_index)
    list_verticies = list_verticies + [adding_index, r]
    return G, list_verticies



