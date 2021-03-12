import numpy as np
from labs.cv4.CONSTANTS import K, verbose, LINKAGE
import copy
from itertools import product
import pandas as pd

def single_linkage_concat(tuples, matrix):
    #Be careful cause similarity is "opposite" to distance.
    #We look for maximum similar (the nearest) individuals!

    res = 0
    lengths = [matrix[y][x] for y, x in tuples]
    res = np.max(lengths)
    if verbose:
        print('tuple', tuples)
        print('matrix\n', pd.DataFrame(matrix))
        print('lengths', lengths);
        print('res', res)
        print('========================')
        print('\n')
    return res

def complete_linkage_concat(tuples, matrix):
    #Be careful cause similarity is "opposite" to distance.
    #We look for minimum similar (furthest individuals) individuals!
    res = 0
    lengths = [matrix[y, x] for y, x in tuples]
    res = np.min(lengths)
    return res


def rebuild(cluster_names, matrix, selected_pair, concatation_func):
    new_cluster_names = []
    for name in cluster_names:
        ignore = set(cluster_names[selected_pair[1]])
        A = set(cluster_names[selected_pair[0]])
        target_name = set(name)
        if ignore.issubset(target_name):
            continue
        if A == target_name:
            merged = name + cluster_names[selected_pair[1]]
            new_cluster_names.append(merged)
        else:
            new_cluster_names.append(name)

    new_size = len(new_cluster_names)
    new_matrix = np.zeros(shape=(new_size, new_size))
    # print('old', cluster_names)
    # print('new', new_cluster_names)
    # print('pair', selected_pair)
    # print(matrix)
    if verbose:
        print(new_cluster_names)

    for y in range(new_size):
        from_cluster = new_cluster_names[y]
        for x in range(new_size):
            if x == y:
                new_matrix[y][x] = 1
                continue    
            to_cluster = new_cluster_names[x]
            new_matrix[y][x] = concatation_func(list(product(from_cluster, to_cluster)), matrix)

    # print(new_cluster_names)
    # print(pd.DataFrame(new_matrix))
    # print(new_cluster_names)
    return new_matrix, new_cluster_names


def hierarchical_clustering(input_matrix, concatation_func = single_linkage_concat if LINKAGE == 'single' else complete_linkage_concat , k = K, distance_break = None):
    matrix = input_matrix.copy()
    cluster_names = [[i] for i in range(len(matrix))]
    snapshots = {}

    while len(cluster_names) > 1:
        distance_matrix_len = len(matrix)
        sim  = None
        selected_pair = None

        if verbose:
            print(pd.DataFrame(matrix))


        for i in range(distance_matrix_len):
            for j in range(i+1, distance_matrix_len):
                if sim is None:
                    sim = matrix[i][j]
                    selected_pair = (i, j)      
                if matrix[i][j] > sim:
                    sim = matrix[i][j]
                    selected_pair = (i, j)

        if verbose:
            print('check matrix\n', pd.DataFrame(matrix))
            print('similarity', sim)
            print('selected pair', selected_pair)
            print(f'GEN {len(cluster_names)}')
        snapshots[len(snapshots.keys())] = (matrix, cluster_names) #
        matrix, cluster_names = rebuild(cluster_names, input_matrix, selected_pair, concatation_func)


    key = len(snapshots.keys()) - (K - 1)
    return snapshots[key]