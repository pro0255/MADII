import numpy as np
import math

#http://www.cs.vsb.cz/ochodkova/courses/MADII/mad2_01_E0.pdf slide 15
def calc_similarity(v_i, v_j):
    n = np.sum(np.dot(v_i, v_j))
    d_i = np.sum(v_i)
    d_j = np.sum(v_j)
    d_m = d_i * d_j

    s = math.sqrt(d_m)
    if s == 0:
        return 0
    else:
        return n / s 

