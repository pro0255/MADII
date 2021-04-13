from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
import numpy as np
import pandas as pd
from utils.models.MultiLevelNet import MultiLevelNet
from labs.cv9.CONSTANTS import NUMBER_OF_STEPS


def read_labels(name):
    labels = []
    with open(name, encoding='utf8') as f:
        for line in f.readlines():
            labels.append(line.strip())
    return labels






def cv9():
    LAYERS = 4
    tailor_path = f'{PATH_TO_DATASETS}ml/tailor/' 
    tailor_matrix_path = f'{tailor_path}matrix.txt'
    tailor_labels_path = f'{tailor_path}labels.txt'
    tailor_layer_labels_path = f'{tailor_path}layer_names.txt'

    matrix = np.loadtxt(tailor_matrix_path)
    
    labels = read_labels(tailor_labels_path)
    layer_labels = read_labels(tailor_layer_labels_path)

    ml_net = MultiLevelNet(matrix, labels, LAYERS, layer_labels)

    # ml_net.flattening()

    ml_net.make_random_walks()