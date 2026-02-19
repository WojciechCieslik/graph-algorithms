from dimacs import *

class UnionFind:
    def __init__(self, size):
        self.parent = [i for i in range(size)]
        self.rank = [0 for i in range(size)]
    def Find(self, i):
        if self.parent[i]==i:
            return i
        return self.Find(self.parent[i])
    def Union(self, i, j):
        a = self.Find(i)
        b = self.Find(j)
        if(a==b):
            return
        if(self.rank[a] < self.rank[b]):
            self.parent[a]=b
        elif(self.rank[a] > self.rank[b]):
            self.parent[b]=a
        else:
            self.parent[b]=a
            self.rank[a]+=1

def heapsort(T):
    def left(x):
        return 2*x+1
    def right(x):
        return 2*x+2
    def parent(x):
        return x//2-1
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
        for i in range(parent(n), -1, -1):
            heapify(T, i, n)
        for i in range(n-1, -1, -1):
            T[0],T[i]=T[i],T[0]
            heapify(T, 0, i)
        return T
    return sort(T)

def PrzewodnikTurystyczny(graf):
    V, L = loadWeightedGraph(graf)
    S = UnionFind(V+1)
    L = heapsort(L)
    highest_weight = 0
    for i in range(len(L)-1, -1, -1):
        highest_weight = L[i][2]
        S.Union(L[i][0], L[i][1])
        if(S.Find(1)==S.Find(2)):
            return highest_weight
    return -1