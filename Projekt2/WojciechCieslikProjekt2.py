from data import runtests
from collections import deque

def solve(friends, prices):
    #Budowa grafu przyjaźni
    V = len(prices)
    graph = [set() for i in range(V)]
    for u, v in friends:
        u -= 1
        v -= 1
        graph[u].add(v)
        graph[v].add(u)
    #Maximum Cardinality Search - algorytm zbliżony do LexBFS działający w O(n) 
    #zwracający PEO dla grafów przekątniowych - co stanowią grafy przyjaźni. 
    #Wynik to PEO w tablicy order  
    order = []
    visited = [False for i in range(V)]
    labels = [0 for i in range(V)]
    buckets = [deque() for i in range(V + 1)]
    
    for v in range(V):
        buckets[0].append(v)
    max_label = 0
    i = 0
    while i < V:
        while not buckets[max_label]:
            max_label -= 1
        v = buckets[max_label].pop()
        if visited[v]:
            continue
        i+=1
        visited[v] = True
        order.append(v)
        for u in graph[v]:
            if not visited[u]:
                labels[u] += 1
                new_label = labels[u]
                buckets[new_label].append(u)
                if new_label > max_label:
                    max_label = new_label
    
    pos = [0 for i in range(V)]
    for i, node in enumerate(order):
        pos[node] = i
    #Schodzimy w dół PEO, wybierając wierzchołki, które nie zostaną zawarte
    #w koniecznych do wybrania, ponieważ sąsiedzi każdego kolejnego wierzchołka
    #stanowią klikę. Odejmujemy od sąsiadów wagę danego wierzchołka - jeśli waga
    #zostanie zredukowana jedynie częściowo, to bardziej opłacalne będzie wybranie
    #tej wyższej wagi, więc po dodaniu jej zredukowanej o wartość wybranego wcześniej
    #sztucznie zostanie cofnięty poprzedni wybór. Jeśli waga się zredukuje - wierzchołek
    #musi zostać wybrany do sumy koniecznych kosztów.
    whole = sum(prices)
    weight = 0
    for v in reversed(order):
        if prices[v] > 0:
            w = prices[v]
            weight += w
            for u in graph[v]:
                if pos[u] < pos[v]:
                    prices[u] -= w
    return whole - weight
runtests(solve)
