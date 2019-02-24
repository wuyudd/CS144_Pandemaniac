import networkx as nx
from readfile import *
# from writefile import *
import heapq
import sim

def build_graph(G):
    graph = nx.Graph()
    for key in G:
        for node in G[key]:
            graph.add_edge(node, key)
    return graph

def closeness(graph, n):
    closeness = nx.closeness_centrality(graph)
    nlargest_closeness = heapq.nlargest(n, closeness, key=closeness.get)
    return nlargest_closeness

def degree(graph, n):
    degree = nx.degree_centrality(graph)
    nlargest_degree = heapq.nlargest(n, degree, key=degree.get)
    return nlargest_degree

if __name__ == "__main__":
    G = read_graph("testgraph1.json")
    graph = build_graph(G)
    # print graph
    n = 15 # input
    close = closeness(graph, n)
    # writefile(close)

    # for sim test
    deg = degree(graph, n)
    strategy = {}
    strategy["closeness"] = close
    strategy["degree"] = deg
    # print(strategy)
    result = sim.run(G, strategy)
    print result
