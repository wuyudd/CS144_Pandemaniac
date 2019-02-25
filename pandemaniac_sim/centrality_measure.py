#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import networkx as nx
from readfile import *
from writefile import *
import heapq
import sys
import sim

'''
How to run this program:
Environment: python 2.7
Packages: networkx
Dependencies: readfile.py, writefile.py, sim.py

Run Command: python closeness_centrality.py json_filename num_seeds
         e.g.:
            python closeness_centrality.py ./testgraph1.json 10

Output: final.txt (contains (num_seeds * round) lines of nodes)
'''

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

def betweenness(graph, n):
    betweenness = nx.betweenness_centrality(graph)
    nlargest_betweenness = heapq.nlargest(n, betweenness, key=betweenness.get)
    return nlargest_betweenness


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
    # between = betweenness(graph, num_seeds)
    # strategy = {}
    # strategy["closeness"] = close
    # strategy["degree"] = deg
    # strategy["between"] = between
    # result = sim.run(G, strategy)
    # print result
