#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
from readfile import *
import networkx as nx
import matplotlib.pyplot as plt
from main import *
from clustering import *
from centrality_measure import *

if __name__ == "__main__":
	filename = sys.argv[1] # input json filename
	G = read_graph(filename)
	origin_graph = nx.Graph(G) # create the graph object
	# select_strategy(strategy_name, origin_graph, cluster_flag, num_seeds, ratio, num_clusters, atmost_nodes_num, final_name) # get final result
	# # draw the original graph and the max_cluster graph
	# plt.figure()
	# pos=nx.spring_layout(origin_graph, k = 0.15, iterations = 20, scale = 10)
	# nx.draw(origin_graph,pos, with_labels = False, node_size = 0.1, width = 0.01)
	# plt.show()
	num_clusters = int(sys.argv[2])
	adj_largest_mat, nodes_largest_graph = largest_subgraph_adj(origin_graph)
	nodes_largest_map, nodes_largest_invmap = map_nodes(nodes_largest_graph)
	A_d, A_emb = embedding_adj(adj_largest_mat)
	nodes_of_clusters = spetral_clustering(A_emb, nodes_largest_graph, num_clusters, nodes_largest_map, nodes_largest_invmap)
	draw_every_subgraph(nodes_of_clusters, origin_graph)


	# nodes_of_clusters = collections.defaultdict(list)
	# spt_cluster = cluster.SpectralClustering(n_clusters=num_clusters, affinity='precomputed', n_neighbors)
	# cluster_labels_of_nodes = spt_cluster.fit_predict(A_emb)

	