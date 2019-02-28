#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Created by Sha Sha, Wen Gu, Yu Wu
#

import networkx as nx
from readfile import *
from writefile import *
import heapq
import sys
import sim
import random
import math
import clustering

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

def aggregate(graph,n,pool_ratio):
    cl = closeness(graph, int(pool_ratio*n))
    dg = degree(graph, int(pool_ratio*n))
    bt = betweenness(graph, int(pool_ratio*n))
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
    return overlap, non_overlap, union


def pick(overlap,non_overlap, union, n, overlap_ratio = 0.5):
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
    elif num_missing < 0:
        candidates = candidates[:n]
    return candidates

def get_largest_cluster(graph, num_clusters):
    adj_largest_mat, nodes_largest_graph = clustering.largest_subgraph_adj(graph)
    nodes_largest_map, nodes_largest_invmap = clustering.map_nodes(nodes_largest_graph)
    A_d, A_emb = clustering.embedding_adj(adj_largest_mat)
    nodes_of_clusters = clustering.spetral_clustering(A_emb, nodes_largest_graph, num_clusters, nodes_largest_map, nodes_largest_invmap)
    max_subgraph, max_len = clustering.output_subgraph(nodes_of_clusters, graph)
    return max_subgraph, max_len

if __name__ == "__main__":
    filename = sys.argv[1]
    num_seeds = int(filename.split('.')[1])
    final_name = "_".join(filename.split('.')) +  "_clu.txt"
    overlap_ratio = float(sys.argv[2])
    num_clusters = int(sys.argv[3])
    atmost_nodes_num = int(sys.argv[4])

    G = read_graph(filename)
    graph = nx.Graph(G)

    num_of_cluster_nodes = float('inf')

    while num_of_cluster_nodes >= atmost_nodes_num:
        graph, max_len = get_largest_cluster(graph, num_clusters)
        num_of_cluster_nodes = max_len
    # close = closeness(graph, num_seeds)
    pool_ratio = 2
    overlap, non_overlap, union = aggregate(graph, num_seeds, pool_ratio)
    # print "ratio = ", overlap_ratio
    # print overlap
    # print non_overlap
    rounds = 50
    fid = open(final_name, 'w')
    for i in range(rounds):
        candidates = pick(overlap,non_overlap,union, num_seeds,overlap_ratio = overlap_ratio)
        for j in range(len(candidates)):
            if (i == rounds-1) and (j == len(candidates)-1):
                fid.write(candidates[j])
            else:    
                fid.write(candidates[j]+'\n')
    fid.close()

    # # for sim test
    # deg = degree(graph, num_seeds)
    # between = betweenness(graph, num_seeds)
    # close = closeness(graph, num_seeds)
    # mix = pick(overlap,non_overlap,union, num_seeds,overlap_ratio = 0.5)
    # strategy = {}
    # strategy["closeness"] = close
    # strategy["degree"] = deg
    # strategy["between"] = between
    # strategy["mix"] = mix
    # result = sim.run(G, strategy)
    # print result
