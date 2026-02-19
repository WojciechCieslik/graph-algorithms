from dimacs import *
import networkx as nx
from networkx.algorithms.flow import maximum_flow
def max_flow_from_file(filename):
    V, edges = loadDirectedWeightedGraph(filename)

    G = nx.DiGraph()
    G.add_nodes_from(range(1, V + 1))

    for u, v, w in edges:
        G.add_edge(u, v, capacity=w)

    value, flow = maximum_flow(G, 1, V)
    return value