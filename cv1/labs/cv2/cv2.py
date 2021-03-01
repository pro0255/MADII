from utils.graph_generation.bianconi import bianconi
from utils.graph_generation.holme_kim import holme_kim
from utils.create_from_dic_adj import create_from_dic_adj
from labs.cv2.CONSTANTS import NUMBER_OF_VERTICIES
import networkx as nx
from labs.cv2 import CONSTANTS 
from constants.PATH_TO_OUTPUTS import PATH_TO_OUTPUTS



def cv2():



    holme_kim_dic = holme_kim(CONSTANTS.n_0, CONSTANTS.TIMESTAMP, CONSTANTS.m_holme, CONSTANTS.P_t_holme)
    holme_kim_adj = create_from_dic_adj(holme_kim_dic)
    holme_kim_G = nx.from_numpy_matrix(holme_kim_adj)
    nx.write_gexf(holme_kim_G, f'{PATH_TO_OUTPUTS}cv2/holme_kim.gexf')


    G = nx.complete_graph(CONSTANTS.n_0)
    G_0 = {v:[] for v in G.nodes}
    for edge in G.edges:
        f, s = edge
        G_0[f].append(s) 
        G_0[s].append(f)

    
    bianconi_dic = bianconi(G_0, CONSTANTS.TIMESTAMP, CONSTANTS.m_bianconi, CONSTANTS.P_t_bianconi)
    bianconi_adj = create_from_dic_adj(bianconi_dic)
    bianconi_G = nx.from_numpy_matrix(bianconi_adj)
    nx.write_gexf(bianconi_G, f'{PATH_TO_OUTPUTS}cv2/bianconi.gexf')


