from dimacs import *
from queue import PriorityQueue

def modifiedDijkstra(n, graph, a, b):
    d = [0 for _ in range(n)]
    d[a] = float('inf')
    q = PriorityQueue()
    q.put((0, a))

    while not q.empty():
        w, v = q.get()
        for l, u in graph[v]:
            low = min(d[v], -l)
            if low > d[u]:
                d[u]=low
                q.put((-low, u))

    return d[b] if d[b] != float('inf') else -1

def PrzewodnikTurystyczny_Dijkstra(graf):
    V, L = loadWeightedGraph(graf)
    G =[[] for i in range(V+1)]
    for u, v, c in L:
        G[u].append((-c, v))
        G[v].append((-c, u))
    return modifiedDijkstra(V+1, G, 1, 2)