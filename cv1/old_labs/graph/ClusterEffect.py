from old_labs.graph.ClusterCoefficient import calculate_cluster_coefficient
import matplotlib.pyplot as plt


def draw_cluster_effect(matrix):
    """
        Určete shlukovací efekt. Ten se určí jako průměrný CC pro vrcholy daného stupně. 
        Distribuci tohoto průměrného CC (osa Y) vůči stupni (osa X).
    """    

    dic = {}

    for index,row in enumerate(matrix):
        degree = len(row[row > 0])
        if degree in dic:
            value = dic[degree]
            value.append((index, calculate_cluster_coefficient(matrix, index)))
        else:
            dic[degree] = [(index, calculate_cluster_coefficient(matrix, index))]



    dictionary_items = dic.items()
    sorted_items = sorted(dictionary_items)
    X = [t[0] for t in sorted_items]

    Y = []
    for t in sorted_items:
        index, c = zip(*t[1])
        Y.append(sum(c)/len(t[1]))

    plt.figure(figsize=(10,8))
    plt.plot(X, Y, 'ro')
    plt.grid()
    plt.show()