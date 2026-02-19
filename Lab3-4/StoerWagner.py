from dimacs import *
from queue import PriorityQueue

class Node:
    def __init__(self):
        self.edges = {}    # słownik mapujący wierzchołki do których są krawędzie na ich wagi
    
    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight # dodaj krawędź do zadanego wierzchołka
                                                        # o zadanej wadze; a jeśli taka krawędź
                                                        # istnieje, to dodaj do niej wagę
    
    def delEdge(self, to):
        del self.edges[to]  # usuń krawędź do zadanego wierzchołka

def build_graph(graf):
    (V, L) = loadWeightedGraph(graf)
    G = [Node() for i in range(V)]
    
    for (x, y, c) in L:
        G[x-1].addEdge(y-1, c)
        G[y-1].addEdge(x-1, c)
    
    return G, V

def mergeVertices(G, x, y):
    for z, weight_yz in list(G[y].edges.items()):
        if z == x:
            continue
        weight_xz = G[x].edges.get(z, 0)
        total_weight = weight_xz + weight_yz
        G[x].addEdge(z, total_weight)
        G[z].addEdge(x, total_weight)
    if y in G[x].edges:
        G[x].delEdge(y)
    if x in G[y].edges:
        G[y].delEdge(x)

def minimumCutPhase(G, active):
    n = len(G)
    active_vertices = [i for i in range(n) if active[i]]
    
    if len(active_vertices) < 2:
        return 0, -1, -1
    a = active_vertices[0]
    S = [a]
    
    connectivity = [0 for i in range(n)]
    visited = [False for i in range(n)]
    visited[a] = True

    Q = PriorityQueue()
    
    for neighbor, weight in G[a].edges.items():
        if active[neighbor] and not visited[neighbor]:
            connectivity[neighbor] += weight
            Q.put((-connectivity[neighbor], neighbor))
    
    while len(S) < len(active_vertices):
        found = False
        v = -1
        
        while not Q.empty() and not found:
            neg_conn, candidate = Q.get()
            if active[candidate] and not visited[candidate]:
                v = candidate
                found = True
        
        if not found:
            break
            
        S.append(v)
        visited[v] = True
        
        for neighbor, weight in G[v].edges.items():
            if active[neighbor] and not visited[neighbor]:
                connectivity[neighbor] += weight
                Q.put((-connectivity[neighbor], neighbor))
    
    if len(S) < 2:
        return 0, -1, -1
        
    s = S[-1]
    t = S[-2]
    cut_weight = connectivity[s]
    
    return cut_weight, s, t

def stoer_wagner(graf): 
    G, V = build_graph(graf)
    active = [True for i in range(V)]
    min_cut = float('inf')
    
    for _ in range(V - 1):
        cut_weight, s, t = minimumCutPhase(G, active)
        
        if cut_weight > 0 and cut_weight < min_cut:
            min_cut = cut_weight
        
        if s != -1 and t != -1:
            mergeVertices(G, s, t)
            active[t] = False
    
    return min_cut if min_cut != float('inf') else 0