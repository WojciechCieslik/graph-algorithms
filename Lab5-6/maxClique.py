from dimacs import *
from LexBFS import *

def maxClique(graph):
    G, V = build(graph)
    order = lexBFS(G)
    pos = [0] * V
    for i, v in enumerate(order):
        pos[v] = i

    max_size = 0

    for v in range(V):
        RN = {u for u in G[v].out if pos[u] < pos[v]}
        clique_v = RN | {v}
        if len(clique_v) > max_size:
            max_size = len(clique_v)

    return max_size