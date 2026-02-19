from dimacs import *
import networkx as nx
from networkx.algorithms.components import strongly_connected_components
from networkx.algorithms.dag import topological_sort
def build_implication_graph(F):
    G = nx.DiGraph()
    for clause in F:
        a, b = clause
        G.add_edge(-a, b)
        G.add_edge(-b, a)
    return G

def compute_scc(G):
    sccs = list(strongly_connected_components(G))
    comp = {}

    for i, scc in enumerate(sccs):
        for v in scc:
            comp[v] = i

    return sccs, comp

def is_satisfiable(V, comp):
    for x in range(1, V + 1):
        if comp[x] == comp[-x]:
            return False
    return True

def build_component_graph(G, component):
    H = nx.DiGraph()
    for u, v in G.edges():
        if component[u] != component[v]:
            H.add_edge(component[u], component[v])
    return H

def build_assignment(order, sccs):
    assignment = {}

    for c in order:
        for literal in sccs[c]:
            var = abs(literal)
            if var not in assignment:
                assignment[var] = (literal < 0)

    return assignment

def verify_formula(F, assignment):
    for a, b in F:
        va = assignment[abs(a)] if a > 0 else not assignment[abs(a)]
        vb = assignment[abs(b)] if b > 0 else not assignment[abs(b)]
        if not (va or vb):
            return False
    return True

def solve_2cnf(filename):
    V, F = loadCNFFormula(filename)
    G = build_implication_graph(F)

    sccs, comp = compute_scc(G)
    if not is_satisfiable(V, comp):
        print("FORMUŁA NIESPEŁNIALNA")
        return

    H = build_component_graph(G, comp)
    order = list(topological_sort(H))
    assignment = build_assignment(order, sccs)

    print("FORMUŁA SPEŁNIALNA")
    for i in range(1, V + 1):
        print(f"x{i} = {assignment[i]}")

    print("Weryfikacja:", verify_formula(F, assignment))