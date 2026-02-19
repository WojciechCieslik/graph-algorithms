from dimacs import *
from collections import deque

def connectivityFlow(graf):

    def build(graf):
        V, L = loadWeightedGraph(graf)
        graph = [[] for i in range(V)]
        for u, v, w in L:
            u-=1
            v-=1
            #graph[u]=(v, flow, max, indeks krawędzi odwrotnej)
            graph[u].append([v, 0, 1, len(graph[v])])
            graph[v].append([u, 0, 1, len(graph[u])-1])
        return graph, V
    
    def BFS(graph, s, t):
        visited = [False for _ in range(len(graph))]
        parent = [None for _ in range(len(graph))]
        q = deque()
        q.append((s, float('inf')))
        visited[s] = True
        while q:
            u, flow = q.popleft()
            for i in range(len(graph[u])):
                v, f, cap, id = graph[u][i]
                rest = cap - f
                if not visited[v] and rest > 0:
                    visited[v] = True
                    parent[v] = (u, i)
                    new_flow = min(flow, rest)
                    if v == t:
                        return new_flow, parent
                    q.append((v, new_flow))

        return 0, parent
    
    def EdmondsKarp(graph, s, t):
        maxflow = 0
        while True:
            flow, parent = BFS(graph, s, t)
            if flow == 0:
                break
            else: maxflow+=flow
            tmp=t
            while tmp!=s:
                u, idx = parent[tmp]
                graph[u][idx][1] += flow
                reverse = graph[u][idx][3]
                graph[tmp][reverse][1] -= flow
                tmp = u
        return maxflow
    
    graph, V = build(graf)
    smallestMaxFlow = float('inf')
    for i in range(V):  
        for j in range(V):
            if(i!=j):
                new_graph, V = build(graf)
                new_flow = EdmondsKarp(new_graph, i, j)
                if(new_flow!=0):
                    smallestMaxFlow = min(new_flow, smallestMaxFlow)
    if smallestMaxFlow == float('inf'):
        return 0
    return smallestMaxFlow

