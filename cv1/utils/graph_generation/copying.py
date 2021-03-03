import random
import numpy as np

def copying(G_0, n, P):
    G = G_0
    t = 0   
    while t < n:
        addingI = len(G.keys())
        G[addingI] = []
        r = np.random.uniform(0, 1)
        choice = random.choice([v for v in G.keys() if v != addingI])

        if r < P:
            #to U
            G[addingI].append(choice)
            G[choice].append(addingI)
        else:
            #to neighbor from U
            neighbors = G[choice]
            options = [v for v in neighbors if v != addingI and v not in G[addingI]] 
            option_choice = random.choice(options)
            G[addingI].append(option_choice)
            G[option_choice].append(addingI)
        t += 1

    return G