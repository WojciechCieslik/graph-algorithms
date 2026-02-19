from collections import deque
from dimacs import *
class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()

    def connect_to(self, v):
        self.out.add(v)

def build(graf):
    V, L = loadWeightedGraph(graf)
    G = [Node(i) for i in range(V)]

    for u, v, _ in L:
        u -= 1
        v -= 1
        G[u].connect_to(v)
        G[v].connect_to(u)

    return G, V

def lexBFS(G):
    n = len(G)
    sets = [set(range(n))]
    order = []

    while sets:
        current_set = sets[-1]
        v = current_set.pop()
        order.append(v)

        if not current_set:
            sets.pop()

        new_sets = []
        for s in sets:
            Y = s & G[v].out
            K = s - G[v].out
            if K:
                new_sets.append(K)
            if Y:
                new_sets.append(Y)
        sets = new_sets

    return order

def MCS(G):
    n = len(G)
    order = []
    visited = [False for i in range(n)]
    labels = [0 for i in range(n)]

    buckets = [deque() for i in range(n+1)]
    
    for v in range(n):
       buckets[0].append(v)
    max_label = 0
    for i in range(n):
        while not buckets[max_label]:
            max_label -=1
        v = buckets[max_label].pop()
        visited[v] = True
        order.append(v)

        for u in G[v].out:
           if not visited[u]:
              labels[u]+=1
              buckets[labels[u]].append(u)
              if labels[u] > max_label:
                 max_label = labels[u]
    return order