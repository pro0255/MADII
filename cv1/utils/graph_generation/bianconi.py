import random

def bianconi(G_0, n, m, P_t):
    G = G_0
    t = 0

    while(t < n):
        adding_vertex = len(G.keys())
        counter = 1
        G, i1 = first_link(G, adding_vertex)
        while counter < m:
            G = second_link(G, adding_vertex, P_t, i1)
            counter += 1
        t+=1
    return G


def first_link(G, adding_vertex):
    verticies = G.keys()
    r = random.choice(list(verticies))
    G[r].append(adding_vertex)

    if adding_vertex not in G:
        G[adding_vertex] = []
    G[adding_vertex].append(r)
    return G, r


def second_link(G, adding_vertex, P, i1):
    r = random.uniform(0, 1)
    my_neighbors = G[adding_vertex]
    if r < P:
        neighbors = [v for v in G[i1] if v not in my_neighbors and v != adding_vertex and v != i1]
        choice = random.choice(neighbors)
        G[choice].append(adding_vertex)
        G[adding_vertex].append(choice)
    else:
        options = [v for v in G.keys() if v not in my_neighbors and v != adding_vertex and v != i1]
        choice = random.choice(options)
        G[choice].append(adding_vertex)
        G[adding_vertex].append(choice)
    return G



