from dimacs import *
import networkx as nx
from networkx.algorithms.planarity import check_planarity
def test_planarity_from_file(filename):
    V, edges = loadWeightedGraph(filename)

    G = nx.Graph()
    G.add_nodes_from(range(1, V + 1))

    for u, v, _ in edges:
        G.add_edge(u, v)

    planar, _ = check_planarity(G)
    return planar