from dimacs import *
from LexBFS import *
def chordal(G):
    def is_PEO(G, order):
        n = len(G)
        pos = [0] * n
        for i, v in enumerate(order):
            pos[v] = i

        for v in range(n):
            RN = {u for u in G[v].out if pos[u] < pos[v]}

            if len(RN) <= 1:
                continue
            parent = max(RN, key=lambda u: pos[u])
            for u in RN:
                if u != parent and u not in G[parent].out:
                    return False

        return True


    graph, V = build(G)
    order = lexBFS(graph)
    return is_PEO(graph, order)