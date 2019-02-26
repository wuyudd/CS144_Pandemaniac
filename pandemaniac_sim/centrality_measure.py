#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import networkx as nx
from readfile import *
from writefile import *
import heapq
import sys
import sim
import random
import math

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

def aggregate(graph,n,pool_ratio = 2):
    cl = closeness(graph, pool_ratio*n)
    dg = degree(graph, pool_ratio*n)
    bt = betweenness(graph, pool_ratio*n)
    data = {}
    for item in cl:
        data[item] = data.get(item,0) +1
    for item in dg:
        data[item] = data.get(item,0) +1
    for item in bt:
        data[item] = data.get(item,0) +1
    overlap = []
    non_overlap = []
    union = set(data.keys())
    for key,value in data.items():
        if value >= 2:
            overlap.append(key)
        else:
            non_overlap.append(key)
    return overlap, non_overlap


def pick(overlap,non_overlap,n,overlap_ratio = 0.5):
    candidates = []
    if len(overlap) <= overlap_ratio*n:
        candidates += overlap
    else:
        candidates += random.sample(overlap, int(math.floor(overlap_ratio*n)))
    if len(non_overlap) <= (1 - overlap_ratio)*n:
        candidates += non_overlap
    else:
        candidates += random.sample(non_overlap, int(math.floor((1-overlap_ratio)*n)))
    num_missing = n - len(candidates)
    if num_missing > 0:
        candidates += random.sample(union - set(candidates), num_missing)
    return candidates

if __name__ == "__main__":
    filename = sys.argv[1]
    num_seeds = int(sys.argv[2])
    final_name = sys.argv[3]
    G = read_graph(filename)
    graph = build_graph(G)
    # close = closeness(graph, num_seeds)
    overlap, non_overlap = aggregate(graph, num_seeds, pool_ratio = 2)
    # print(overlap)
    # print(non_overlap)
    rounds = 50
    fid = open(final_name, 'w')
    for i in range(rounds):
        candidates = pick(overlap,non_overlap,num_seeds,overlap_ratio = 0.5)
        for j in range(len(candidates)):
            if (i == rounds-1) and (j == len(candidates)-1):
                fid.write(candidates[j])
            else:    
                fid.write(candidates[j]+'\n')
    fid.close()

    # for sim test
    deg = degree(graph, num_seeds)
    between = betweenness(graph, num_seeds)
    close = closeness(graph, num_seeds)
    mix = pick(overlap,non_overlap,num_seeds,overlap_ratio = 0.5)
    strategy = {}
    strategy["closeness"] = close
    strategy["degree"] = deg
    strategy["between"] = between
    strategy["mix"] = mix
    result = sim.run(G, strategy)
    print result
