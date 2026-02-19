from dimacs import *
from collections import deque

def DFS(G,s,t):
    n=len(G)
    Q=[]
    visited = [False for i in range(n)]
    visited[s]=True
    Q.append(s)
    while(Q):
        u=Q.popleft()
        for v in G[u]:
            if not visited[v]:
                if(v==t):
                    return True
                visited[v]=True
                Q.append(v)        
    return False

def BFS(G,s,t):
    n=len(G)
    Q=deque()
    visited = [False for i in range(n)]
    visited[s]=True
    Q.append(s)
    while(Q):
        u=Q.pop()
        for v in G[u]:
            if not visited[v]:
                if(v==t):
                    return True
                visited[v]=True
                Q.append(v)        
    return False

def graph_partial(V, edges, mid):
    G = [[] for _ in range(V + 1)]
    for u, v, w in edges:
        if w >= mid:
            G[u].append(v)
            G[v].append(u)
    #return DFS(G, 1, 2)
    return BFS(G, 1, 2)

def heapsort(T):
    def left(x):
        return 2*x+1
    def right(x):
        return 2*x+2
    def heapify(T, x, n):
        maxid=x
        if(left(x)<n and T[left(x)][2]>T[maxid][2]):
            maxid = left(x)
        if(right(x)<n and T[right(x)][2]>T[maxid][2]):
            maxid = right(x)
        if(maxid!=x):
            T[x],T[maxid]=T[maxid],T[x]
            heapify(T, maxid, n)
    def sort(T):
        n=len(T)
        for i in range(n//2-1, -1, -1):
            heapify(T, i, n)
        for i in range(n-1, 0, -1):
            T[0],T[i]=T[i],T[0]
            heapify(T, 0, i)
        return T
    return sort(T)


def PrzewodnikTurystyczny_DFS(graf):
    V, L = loadWeightedGraph(graf)
    L = heapsort(L)
    highest_weight = 0
    low, high = 0, len(L) - 1
    while low <= high:
        mid = (low + high) // 2
        w = L[mid][2]
        if graph_partial(V, L, w):
            highest_weight = L[mid][2]
            low = mid + 1
        else:
            high = mid - 1
    return highest_weight
