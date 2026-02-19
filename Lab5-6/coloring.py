from dimacs import *
from LexBFS import *

def coloring(graph):
    G, V  = build(graph)
    order = lexBFS(G)
    color = [0] * V

    for v in order:
        used = {color[u] for u in G[v].out if color[u] > 0}
        c = 1
        while c in used:
            c += 1
        color[v] = c

    chromatic_number = max(color)
    return chromatic_number