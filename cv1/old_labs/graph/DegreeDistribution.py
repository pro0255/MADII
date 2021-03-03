import numpy as np
from collections import Counter

def degree_distribution(matrix, verbose=False):
    de = []
    output = '\n========================\nDegree Distribution\n========================\n'
    for i, row in enumerate(matrix):
        vertex_index = i + 1
        degree = len(row[row > 0])
        o = f'ID {vertex_index} - Degree {degree}'
        output += f'{o}\n'
        if verbose:
            print(o)
        de.append(degree)

    c = Counter(de)

    maximal = max(c.keys())
    minimal = min(c.keys())
    average = sum(de)/len(de)
    maxo = f'Maximalni stupen - {maximal}'
    mino = f'Minimalni stupen - {minimal}'
    avgo = f'Prumerny stupen - {average}' 

    output += f'{maxo}\n'
    output += f'{mino}\n'
    output += f'{avgo}\n'


    s = sorted(c.items(), reverse=False)
    output += '\nRelativni cetnost stupnu\n'
    for tup in s:
        d_i = tup[0]
        rc = tup[1]/sum(c.values())
        output += f'Degree {d_i} - {round(rc, 2)}%\n'

    if verbose:
        print(maxo)
        print(mino)
        print(avgo)
    return (output, (maximal, minimal, average, c))





