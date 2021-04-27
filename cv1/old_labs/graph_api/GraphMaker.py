import matplotlib.pyplot as plt
from old_labs.graph.GraphProperties import GRAPH_INSPECTION, GRAPH_CONNECTED_COMPONENTS_PROPERTIES

class GraphMaker():
    def __init__(self, graph_inspection):
        self.graph_inspection = graph_inspection
    #!: todo make graphs dependent on dictionary

    def plot_components_distribution(self):
        connected_components = self.graph_inspection[GRAPH_INSPECTION.CONNECTED_COMPONENTS]
        counter = connected_components[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_COUNTER]
        s = sorted(counter.items())
        size, occurences = zip(*s)
        plt.bar(size, height=occurences)
        plt.title('Rozlozeni komponent souvislosti')
        plt.grid()
        plt.xticks(size, size)
        plt.show()