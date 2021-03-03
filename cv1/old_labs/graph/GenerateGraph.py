import math
import numpy as np

def generate_random_graph(n, p):
    m=int(p*n*(n-1)/2)
    graph = np.zeros(shape=(n,n))
    while m:
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)
        if i != j and graph[i][j] == 0:
            graph[i][j] = 1
            graph[j][i] = 1
            m -= 1
    return graph
