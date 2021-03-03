from labs.cv3 import CONSTANTS
from utils.graph_generation.copying import copying
from utils.graph_generation.link_selection import link_selection
import networkx as nx
from utils.create_from_dic_adj import create_from_dic_adj
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS


def cv3():


    G_0 = nx.complete_graph(CONSTANTS.START_NODES)
    link_selection_G = link_selection(G_0, CONSTANTS.TIMESTAMP)
    nx.write_gexf(link_selection_G, f'{PATH_TO_OUTPUTS}cv3/link_selection.gexf')


    G = nx.complete_graph(CONSTANTS.START_NODES)
    G_0 = {v:[] for v in G.nodes}
    for edge in G.edges:
        f, s = edge
        G_0[f].append(s) 
        G_0[s].append(f)

    copying_dic = copying(G_0, CONSTANTS.TIMESTAMP, CONSTANTS.P_copying)
    copying_adj = create_from_dic_adj(copying_dic)
    copying_G = nx.from_numpy_matrix(copying_adj)
    nx.write_gexf(copying_G, f'{PATH_TO_OUTPUTS}cv3/copying.gexf')
