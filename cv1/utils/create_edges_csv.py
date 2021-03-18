import numpy as np
import pandas as pd


def create_edges_csv(G, filename):
    number_of_edges = len(G.edges())
    num = np.zeros(shape=(number_of_edges, 2))
    for i, edge in enumerate(G.edges()):
        f, t = edge
        num[i][0] = f
        num[i][1] = t 
    df = pd.DataFrame(num).astype(int)
    df.to_csv(filename, sep=';', encoding='utf-8', index=False, header=False)