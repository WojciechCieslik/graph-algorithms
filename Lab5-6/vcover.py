from dimacs import *
from LexBFS import *

def minVertexCover(graph_name):
    G, V = build(graph_name)
    
    peo = lexBFS(G)
    peo.reverse()

    independent_set = set()

    for v in peo:
        if not (G[v].out & independent_set):
            independent_set.add(v)
    min_cover = set(range(V)) - independent_set
    return len(min_cover)
