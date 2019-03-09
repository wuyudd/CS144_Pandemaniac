#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 
# This program is to cut the graphs into clusters so as to speed up the centrality measurement calculation.
# 

import networkx as nx
from readfile import *
from writefile import *
from sklearn import cluster, manifold
import heapq
import sys
import sim
import collections
import numpy as np
import matplotlib.pyplot as plt

def largest_subgraph_adj(graph):
	'''
	This function is to find the largest connected component subgraph.
	Return: The adjacent matrix and list of nodes of the largest connected component subgraph.
	'''
	largest_graph = graph.subgraph(list(nx.connected_component_subgraphs(graph))[0]) # get largest connected component subgraph
	nodes_largest_graph = list(largest_graph.nodes()) # get all the nodes of the subgraph
	adj_largest_mat = nx.adjacency_matrix(largest_graph)
	return adj_largest_mat, nodes_largest_graph

def map_nodes(nodes_largest_graph):
	'''
	This function is to map node_id with the order.
	Return: map and inverse map of nodes.
	'''
	nodes_largest_map = {}
	nodes_largest_invmap = {}
	for i in range(len(nodes_largest_graph)):
		nodes_largest_map[nodes_largest_graph[i]] = i 
		nodes_largest_invmap[i] = nodes_largest_graph[i]
	return nodes_largest_map, nodes_largest_invmap

def embedding_adj(adj_largest_mat):
	'''
	This function is to do the Laplacian Embedding to 2-D.
	Return: todense matrix A_d and dimension-reduction to 2-D matrix A_emb.
	'''
	A_d = adj_largest_mat.todense() # A_d shape: (n_samples, n_features)
	emb = manifold.SpectralEmbedding(n_components=2, affinity='precomputed')
	A_emb = emb.fit_transform(A_d) # A_emb shape: (n_samples, n_components)
	return A_d, A_emb

def spetral_clustering(A_emb, nodes_largest_graph, num_clusters, nodes_largest_map, nodes_largest_invmap):
	'''
	This function is to do the spetral clustering to divide the original graphs to clusters.
	Return: list of nodes of the correpsonding clusters (identified by label of cluster).
	'''	
	# spt_cluster = cluster.SpectralClustering(n_clusters=num_clusters, eigen_solver='arpack', affinity='nearest_neighbors').fit(A_emb)
	# cluster_labels_of_nodes = spt_cluster.labels_
	nodes_of_clusters = collections.defaultdict(list)

	spt_cluster = cluster.SpectralClustering(n_clusters=num_clusters, affinity='nearest_neighbors')
	#spt_cluster = cluster.SpectralClustering(n_clusters=num_clusters, affinity='precomputed')
	cluster_labels_of_nodes = spt_cluster.fit_predict(A_emb) # return labels : ndarray, shape (n_samples,)
	# print "****************** cluster label ******************"
	# print cluster_labels_of_nodes
	# print len(cluster_labels_of_nodes)

	for i in range(len(cluster_labels_of_nodes)):
		curr_label = cluster_labels_of_nodes[i]
		curr_node = nodes_largest_invmap[i]
		nodes_of_clusters[curr_label].append(curr_node) # int?

	print "****************** clusters information ******************"
	for key, value in nodes_of_clusters.items():
		#print key, value, "length = ", len(value)
		print key, "length = ", len(value)
	print "****************** clusters information end ******************"
 	return nodes_of_clusters

def output_subgraph(nodes_of_clusters, graph):
	'''
	This function is to output the largest subgraph.
	Return nx subgraph.
	'''
	max_len = 0
	for key, value in nodes_of_clusters.items():
		if len(value) > max_len:
			max_len = len(value)
			max_cluster = key
	max_subgraph = graph.subgraph(nodes_of_clusters[max_cluster])
	return max_subgraph, max_len

def draw_every_subgraph(nodes_of_clusters, graph):
	for key, value in nodes_of_clusters.items():
		subgraph = graph.subgraph(nodes_of_clusters[key])
		plt.figure()
		pos=nx.spring_layout(subgraph, k = 0.15, iterations = 20, scale = 10)
		nx.draw(subgraph,pos, with_labels = False, node_size = 0.1, width = 0.01)
		plt.show()

def plot(nodes_of_clusters, A_emb):
	'''
	This function is to plot the clusters (can only used in original graph because of the index issue).
	Return: Nothing to return.
	'''
	print "start!"
	for cluster in nodes_of_clusters.keys():
		print cluster
		new = []
		for i in nodes_of_clusters[cluster]:
			new.append(int(i)-1)
		sub_pos = A_emb[new]
		plt.scatter(sub_pos[:,0],sub_pos[:,1],color = plt.cm.Spectral(cluster / 5.),linewidths = 0.1,alpha=0.1)
	print "end!"
	plt.show()


if __name__ == "__main__":
	filename = sys.argv[1]
	num_clusters = int(sys.argv[2])
	G = read_graph(filename)
	graph = nx.Graph(G)

	# largest connected component: 
	# adj_largest_mat, nodes_largest_graph = largest_subgraph_adj(graph)
	# nodes_largest_map, nodes_largest_invmap = map_nodes(nodes_largest_graph)

	# original graph:
	adj_largest_mat = nx.adjacency_matrix(graph)
	nodes_largest_graph = list(graph.nodes())
	print "adj_largest_mat shape = ", adj_largest_mat.shape
	# map nodes 
	nodes_largest_map, nodes_largest_invmap = map_nodes(nodes_largest_graph)

	# 2-D embedding
	A_d, A_emb = embedding_adj(adj_largest_mat)
	print "A_d shape = ", A_d.shape
	print "A_emb shape = ", A_emb.shape
	
	# spectral clustering 
	nodes_of_clusters = spetral_clustering(A_emb, nodes_largest_graph, num_clusters, nodes_largest_map, nodes_largest_invmap)
	
	#plot(nodes_of_clusters, graph)
	for key, value in nodes_of_clusters.items():
		print "****************** clusters information ******************"
		print key, value, "length = ", len(value)

	# output max_cluster graph
	max_subgraph = output_subgraph(nodes_of_clusters, graph)


	# draw the original graph and the max_cluster graph
	# plt.figure()
	# nx.draw(graph, pos=nx.random_layout(graph), node_color = 'r', edge_color = 'black', with_labels = True, font_size = 8, node_size = 20)
	# plt.show()

	# plt.figure()
	# nx.draw(max_subgraph, pos=nx.random_layout(max_subgraph), node_color = 'g', edge_color = 'black', with_labels = True, font_size =8, node_size=20)
	# plt.show()	



	
	