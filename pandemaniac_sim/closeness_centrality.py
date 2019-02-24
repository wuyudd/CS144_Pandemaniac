#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import networkx as nx
from readfile import *
from writefile import *
import heapq
import sys
import sim

def build_graph(G):
    graph = nx.Graph()
    for key in G:
        for node in G[key]:
            graph.add_edge(node, key)
    return graph

def closeness(graph, n):
    closeness = nx.closeness_centrality(graph)
    # print closeness
    nlargest_closeness = heapq.nlargest(n, closeness, key=closeness.get)
    return nlargest_closeness

def degree(graph, n):
    degree = nx.degree_centrality(graph)
    nlargest_degree = heapq.nlargest(n, degree, key=degree.get)
    return nlargest_degree

if __name__ == "__main__":
    filename = sys.argv[1]
    num_seeds = int(sys.argv[2])
    final_name = "final.txt"
    G = read_graph(filename)
    graph = build_graph(G)
    close = closeness(graph, num_seeds)
    write_file(final_name, close)

    # # for sim test
    # deg = degree(graph, num_seeds)
    # strategy = {}
    # strategy["closeness"] = close
    # strategy["degree"] = deg
    # result = sim.run(G, strategy)
    # print result
