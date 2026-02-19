from dimacs import *
from collections import deque

def maxFlow(graf, algorithm):

    def build(graf):
        V, L = loadDirectedWeightedGraph(graf)
        graph = [[] for i in range(V)]
        for u, v, w in L:
            u-=1
            v-=1
            #graph[u]=(v, flow, max, indeks krawędzi odwrotnej)
            graph[u].append([v, 0, w, len(graph[v])])
            graph[v].append([u, 0, 0, len(graph[u])-1])
        return graph
    
    def DFS(graph,s,t, flow, visited):
        if(s==t):
            return flow
        visited[s]=True
        for i in range(len(graph[s])):
            v, f, cap, id = graph[s][i]
            rest = cap - f
            if not visited[v] and rest > 0:
                further = DFS(graph, v, t, min(flow, rest), visited)
                if further > 0:
                    graph[s][i][1]+=further
                    graph[v][id][1]-=further
                    return further
        return 0
    
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
    
    #O(VE^2)
    def EdmondsKarp(graf):
        graph = build(graf)
        maxflow = 0
        t=len(graph) - 1 
        while True:
            flow, parent = BFS(graph, 0, len(graph) - 1)
            if flow == 0:
                break
            else: maxflow+=flow
            tmp=t
            while tmp!=0:
                u, idx = parent[tmp]
                graph[u][idx][1] += flow
                reverse = graph[u][idx][3]
                graph[tmp][reverse][1] -= flow
                tmp = u
        return maxflow
    
    #O(E*flow)
    def FordFulkerson(graf):
        graph = build(graf)
        maxflow = 0
        t=len(graph) - 1
        while(True):
            visited = [False for i in range(t+1)]
            flow = DFS(graph, 0, t, float('inf'), visited)
            if flow == 0:
                break
            else: maxflow+=flow
        return maxflow
    
    if(algorithm == "DFS"):
        return FordFulkerson(graf)
    if(algorithm == "BFS"):
        return EdmondsKarp(graf)