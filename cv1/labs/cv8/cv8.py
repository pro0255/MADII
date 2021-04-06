from constants.PATH_TO_DATASETS import PATH_TO_DATASETS
import numpy as np
import pandas as pd
from utils.models.MultiLevelNet import MultiLevelNet


def read_labels(name):
    labels = []
    with open(name, encoding='utf8') as f:
        for line in f.readlines():
            labels.append(line.strip())
    return labels
    


def cv8():
    #TODO: vypocitat miry sousedstvi, stupne, a relevance
    #http://vlado.fmf.uni-lj.si/pub/networks/data/UciNet/UciData.htm
    #ZACHE
    #ZACHC
    LAYERS = 4
    tailor_path = f'{PATH_TO_DATASETS}ml/tailor/' 
    tailor_matrix_path = f'{tailor_path}matrix.txt'
    tailor_labels_path = f'{tailor_path}labels.txt'
    matrix = np.loadtxt(tailor_matrix_path)
    labels = read_labels(tailor_labels_path)
    ml_net = MultiLevelNet(matrix, labels, LAYERS)