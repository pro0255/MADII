import pandas as pd
from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS
import numpy as np
import networkx as nx
from labs.cv7.Performance import Performace
from labs.cv7.CONSTANTS import kc_JAC_T, kc_CN_T, TEST, VERBOSE, lem_JAC_T, lem_CN_T


"""
    Implement at least two link prediction methods and applies
    them to at least two networks (e.g., Karate Club, Les
    Misérables). Compute all listed performance measures for all
    methods and networks.
"""
def create_d(source, target):
    res = {}
    size = len(target)
    for i in range(size):
        c_s = source[i]
        c_t = target[i]
        if c_s in res:
            res[c_s].append(c_t)
        else:
            res[c_s] = [c_t]
        if c_t in res:
            res[c_t].append(c_s)
        else:
            res[c_t] = [c_s]
    return res

def create_kc_matrix(d):
    size = len(d.keys())
    A = np.zeros(shape=(size, size))
    for i in range(size):
        vertex_edges = d[i+1] #1..max
        for e in vertex_edges:
            r_index = e - 1
            A[i, r_index] = 1
    return A

def create_lemis_matrix(d):
    size = len(d.keys())
    keys = list(d.keys())
    label2index = {keys[i]:i for i in range(size)}
    A = np.zeros(shape=(size, size))
    for key in keys:
        v_index = label2index[key]
        for edge in d[key]:
            edge_index = label2index[edge]
            A[v_index, edge_index] = 1
    return A


def cn_calc(y, x):
    edges_y = np.where(y > 0)
    edges_x = np.where(x > 0)
    set_y = set(np.array(edges_y).flatten()) 
    set_x = set(np.array(edges_x).flatten())
    intersect = set_y.intersection(set_x)
    if TEST:
        print(set_y)
        print(set_x)
        print(intersect)
        exit()
    same = len(intersect)
    return same

def jaccard_calc(y, x):
    edges_y = np.where(y > 0)
    edges_x = np.where(x > 0)
    set_y = set(np.array(edges_y).flatten()) 
    set_x = set(np.array(edges_x).flatten()) 
    intersect = set_y.intersection(set_x)
    unioned = set_y.union(set_x)
    nom = len(intersect)
    den = len(unioned)
    if den == 0:
        return 0
    return nom/den


def create_matrix_deps_on_method(matrix, method):
    result_A = np.zeros(shape=matrix.shape)
    for y in range(result_A.shape[0]):
        y_vertex = matrix[y, :]
        for x in range(result_A.shape[1]):
            if y == x:
                continue
            x_vertex = matrix[x, :]
            res = method(y_vertex, x_vertex)
            result_A[y, x] = res
    return result_A



def common_neighbors_matrix(matrix):
    return create_matrix_deps_on_method(matrix, cn_calc)


def jaccard_matrix(matrix):
    return create_matrix_deps_on_method(matrix, jaccard_calc)


def create_confusion_tuple(matrix, m_matrix):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0


    for y in range(matrix.shape[0]):
        for x in range(y+1, matrix.shape[1]):
            available_value = matrix[y, x]
            predicted_value = m_matrix[y, x]
            if available_value == True and predicted_value == True:
                true_positive += 1

            if available_value == False and predicted_value == False:
                true_negative += 1

            if available_value == False and predicted_value == True:
                true_negative += 1

            if available_value == True and predicted_value == False:
                false_negative += 1

    res = (true_positive, true_negative, false_positive, false_negative)
    if VERBOSE:
        print(f'\n\tTrue positive {true_positive}\n\tTrue negative {true_negative}\n\tFalse positive {false_positive}\n\tFalse negative {false_negative}\n')
    return res


def apply_threshold(matrix, threshold):
    thresholded_matrix = np.copy(matrix)
    res = np.where(thresholded_matrix > threshold, 1, 0)
    return res

def make_calculation(matrix, cn_t, jac_t):
    cn_A = common_neighbors_matrix(matrix)
    jac_A = jaccard_matrix(matrix)

    cn_A_thresholded = apply_threshold(cn_A, cn_t)
    jac_A_thresholded = apply_threshold(jac_A, jac_t)


    cn_conf_tuple = create_confusion_tuple(matrix, cn_A_thresholded)
    jac_conf_tuple = create_confusion_tuple(matrix, jac_A_thresholded)

    cn_perf = Performace("Common Neighbors (CN)")
    cn_perf.calculate(cn_conf_tuple)

    jac_perf = Performace('Jaccard Coefficient')
    jac_perf.calculate(jac_conf_tuple)


    print(jac_perf)
    print(cn_perf)



def cv7():
    kc = pd.read_csv(f'{PATH_TO_DATASETS}KarateClub.csv', ';', header=None)
    lesmis = pd.read_csv(f'{PATH_TO_DATASETS}lesmis.csv', ',', header=None)

    kc_source = kc.iloc[:, 0].values
    kc_target =  kc.iloc[:, 1].values
    kc_d = create_d(kc_source, kc_target)
    kc_matrix = create_kc_matrix(kc_d)

    lesmis_source = lesmis.iloc[:, 0]
    lesmis_target = lesmis.iloc[:, 2]
    lesmis_d = create_d(lesmis_source, lesmis_target)
    lesmis_matrix = create_lemis_matrix(lesmis_d)


    print('karate club'.upper())
    make_calculation(kc_matrix, kc_CN_T, kc_JAC_T)
    print()

    print('lesmis'.upper())
    make_calculation(lesmis_matrix, lem_CN_T, lem_JAC_T)
    print()

    # print(kc_matrix)
    # print(lesmis_matrix)
    print('cv7')