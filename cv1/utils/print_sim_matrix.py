import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def print_sim_matrix(sim_matrix):
    verticies = np.arange(len(sim_matrix))

    fig, ax = plt.subplots(figsize=(10,10))
    im = ax.imshow(sim_matrix)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(verticies)))
    ax.set_yticks(np.arange(len(verticies)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(verticies)
    ax.set_yticklabels(verticies)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # for i in range(len(verticies)):
    #     for j in range(len(verticies)):
    #         text = ax.text(j, i, sim_matrix[i, j],
    #                     ha="center", va="center", color="w")


    ax.set_title("Similarity matrix")
    fig.tight_layout()
    plt.show()