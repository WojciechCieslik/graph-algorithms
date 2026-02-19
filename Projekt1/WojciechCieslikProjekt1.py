from data import runtests
from collections import deque
from math import log10

def solve(scores):
    #Funkcja rozbijająca liczbę na czynniki pierwsze
    def factorize(n):
        factors={}
        if(n%2==0):
            counter=0
            while(n%2==0):
                counter+=1
                n//=2
            factors[2]=counter
        i=3
        while(i*i<=n):
            if(n%i==0):
                counter=0
                while(n%i==0):
                    counter+=1
                    n//=i
                factors[i]=counter
            i+=2
        if(n>1):
            factors[n]=1
        return factors
    
    #Funkcja dodająca krawędzie w grafie
    def addEdge(graph, u, v, capacity):
        graph[u].append([v, capacity, len(graph[v])])
        graph[v].append([u, 0.0, len(graph[u])-1])

    #Rozbijanie liczb na czynniki pierwsze, zapis występujących liczb pierwszych i najwyższych potęg liczb pierwszych
    highestPowers={}
    factored=[]
    for d, c in scores:
        if(c<=0):
            continue
        factors = factorize(d)
        factored.append((factors, c))
        for p, count in factors.items():
            if(count>highestPowers.get(p, 0)):
                highestPowers[p]=count
    primes = sorted(highestPowers.keys())
    primeIndexes={}
    for i, p in enumerate(primes):
        primeIndexes[p]=i
    #Indeksy w grafie i budowa grafu - źródło łączy się dzielnikami z pojemnością krawędzi równą
    #c_i dla danego dzielnika d_i, dzielnik łączy się ze swoimi czynnikami pierwszymi krawędziami
    #o nieskończonej pojemności (ich rozdzielenie nie jest możliwe), a czynniki pierwsze łączą się 
    #z ujściem krawędziami o pojemności równej 5*log10(czynnik pierwszy).
    powerPrefix = [0 for i in range(len(primes)+1)]
    for i, p in enumerate(primes):
        powerPrefix[i+1] = powerPrefix[i]+highestPowers[p]        
    S, T = 0, 1
    n = len(factored)
    factoredStart = 2
    factorsStart = 2+n
    V = factorsStart+powerPrefix[-1]
    graph = [[] for i in range(V)]
    for i, (factors, c) in enumerate(factored):
        addEdge(graph, S, factoredStart+i, float(c))
        for p, count in factors.items():
            addEdge(graph, factoredStart+i, factorsStart+powerPrefix[primeIndexes[p]]+count-1, float('inf'))
    for i, p in enumerate(primes):
        #log(ab) = log(a) + log(b), więc koszt indywidualnych czynników pierwszych to 5*log10(czynnik pierwszy)
        cost = 5.0*log10(p)
        start = factorsStart + powerPrefix[i]
        for power in range(highestPowers[p]):
            current = start + power
            addEdge(graph, current, T, cost)
            if(power>0):
                addEdge(graph, current, current-1, float('inf'))
    #Algorytm Dinica do znajdywania maksymalnego przepływu - jeśli krawędź od żródła do wybranego dzielnika
    #spadnie wartością do zera - zostanie przepełniona, to "koszta" jej czynników pierwszych połączonych z ujściem przekraczają zysk
    #i nie opłaca się jej wzięcie. W przeciwnym wypadku przepełnione będą krawędzie od czynników do ujścia dla danego dzielnika.
    #Wtedy wzięcie danego dzielnika opłaca się. Na podstawie końcowego zapisu poziomów, wierzchołki osiągalne przez BFS to wierzchołki,
    #które zostały wybrane jako opłacalne.
    levels = [-1 for i in range(V)]

    #BFS dzielący wierzchołki na podstawie odległości od źródła
    def levelsBFS():
        for i in range(V):
            levels[i]=-1
        levels[S]=0
        Q = deque()
        Q.append(S)
        while Q:
            u = Q.popleft()
            for v, cap, reverse in graph[u]:
                if(cap>0 and levels[v]<0):
                    levels[v]=levels[u]+1
                    Q.append(v)
        return levels[T]>=0
    
    #Zmodyfikowany DFS tworzący ścieżki powiększające, które z każdą krawędzią przechodzą bliżej ujścia - wybierane są jedynie wierzchołki
    #należące do kolejego poziomu w BFS.
    def DFS(u, flow, ptrs):
        if(u==T or flow==0):
            return flow
        for i in range(ptrs[u], len(graph[u])):
            v, cap, reverse = graph[u][i]
            if(levels[v]==levels[u]+1 and cap>0):
                pushed = DFS(v, min(flow, cap), ptrs)
                if(pushed>0):
                    graph[u][i][1]-=pushed
                    graph[v][reverse][1]+=pushed
                    return pushed
            ptrs[u]+=1
        return 0
    
    #Pętla kończy się, gdy ujście nie jest osiągalne przez BFS
    while levelsBFS():
        #Optymalizacja - podczas szukania kolejnych ścieżek powiększających program pomija te,
        #które zostały już przebyte.
        ptrs = [0 for i in range(V)]
        while True:
            pushed = DFS(S, float('inf'), ptrs)
            if pushed == 0:
                break
    result=1
    for i, prime in enumerate(primes):
        maxPower = 0
        start = factorsStart + powerPrefix[i]
        for power in range(highestPowers[prime]):
            if levels[start + power] != -1:
                maxPower = power + 1
        if maxPower > 0:
            result*=prime**maxPower
    return result

runtests(solve)