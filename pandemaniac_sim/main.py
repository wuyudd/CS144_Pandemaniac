#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from centrality_measure import *
from clustering import *
import random
import numpy as np

#
# This program provides several strategies to select nodes and writes out the final result into the final file.
# Created by Yu Wu, import files are created by Sha Sha, Wen Gu, Yu Wu.
#

def select_strategy(strategy_name, graph, cluster_flag, num_seeds, ratio, num_clusters, atmost_nodes_num, out_filename):
	'''
	This function is to choose the corresponding strategy and write out to the final file.
	'''
	rounds = 50
	if cluster_flag == "1": # decides whether to get cluster or not
		graph, max_len = max_cluster(graph, num_clusters, atmost_nodes_num)
		print "final graph size = ", max_len
	
	if strategy_name == "deg":
		final_nodes = degree_only(graph, num_seeds, ratio, rounds)
		write_out(final_nodes, out_filename)
	elif strategy_name == "clo":
		final_nodes = closeness_only(graph, num_seeds, ratio, rounds)
		write_out(final_nodes, out_filename)
	elif strategy_name == "bet":
		final_nodes = betweenness_only(graph, num_seeds, ratio, rounds)
		write_out(final_nodes, out_filename)
	elif strategy_name == "aggr":
		aggregate_centrality(graph, num_seeds, ratio, overlap_ratio, rounds, out_filename)
	elif strategy_name == "union":
		final_nodes = union(graph, num_seeds, ratio, rounds)
		write_out(final_nodes, out_filename)
	else:
		print "no such strategy"


def degree_only(graph, num_seeds, ratio, rounds):
	'''
	This function randomly selects (num_seeds) nodes from the top (num_seeds * ratio) highest degree nodes.
	'''
	select_n = int(num_seeds * ratio)
	selected_n_nodes = degree(graph, select_n)
	final_nodes = random_choice(num_seeds, ratio, selected_n_nodes, rounds)
	return final_nodes

def closeness_only(graph, num_seeds, ratio, rounds):
	'''
	This function randomly selects (num_seeds) nodes from the top (num_seeds * ratio) highest closeness nodes.
	'''
	select_n = int(num_seeds * ratio)
	selected_n_nodes = closeness(graph, select_n)
	final_nodes = random_choice(num_seeds, ratio, selected_n_nodes, rounds)
	return final_nodes

def betweenness_only(graph, num_seeds, ratio, rounds):
	'''
	This function randomly selects (num_seeds) nodes from the top (num_seeds * ratio) highest betweenness nodes.
	'''
	select_n = int(num_seeds * ratio)
	selected_n_nodes = betweenness(graph, select_n)
	final_nodes = random_choice(num_seeds, ratio, selected_n_nodes, rounds)
	return final_nodes

def union(graph, num_seeds, ratio, rounds):
	cl = closeness(graph, int(ratio * num_seeds))
	dg = degree(graph, int(ratio * num_seeds))
	bt = betweenness(graph, int(ratio * num_seeds))
	union_nodes = list(set(cl + dg + bt))
	# print "close: ", cl
	# print "degree: ", dg
	# print "betweenness: ", bt
	# print "union: ", union_nodes, "; len = ", len(union_nodes)
	indices = list(range(len(union_nodes)))
	final_nodes = []
	for i in range(rounds):
		shuffled_indices = np.random.permutation(indices)
		for j in range(num_seeds):
			ind = shuffled_indices[j]
			final_nodes.append(union_nodes[ind])
	return final_nodes


def aggregate_centrality(graph, num_seeds, ratio, overlap_ratio, rounds, out_filename):
	'''
	This function randomly selects (num_seeds) nodes from the union of the above three centrality nodes.
		Considers both overlapped nodes and non_overlapped nodes (with a overlap_ratio to choose)
		Write out to the final file.
	'''
	overlap, non_overlap, union = aggregate(graph, num_seeds, pool_ratio=ratio)
	fid = open(out_filename, 'w')
	for i in range(rounds):
		candidates = pick(overlap, non_overlap,union, num_seeds, overlap_ratio=overlap_ratio)
		for j in range(len(candidates)):
			if (i == rounds-1) and (j == len(candidates)-1):
				fid.write(candidates[j])
			else: 
				fid.write(candidates[j]+'\n')
	fid.close()

def random_choice(num_seeds, ratio, selected_n_nodes, rounds):
	'''
	This function randomly chooses (num_seeds) nodes from the top (num_seeds * ratio) nodes and then iterates for (rounds) rounds.

	'''
	select_n = int(num_seeds * ratio)
	indices = list(range(select_n))
	final_nodes = []
	for i in range(rounds):
		shuffled_indices = np.random.permutation(indices)
		for j in range(num_seeds):
			ind = shuffled_indices[j]
			final_nodes.append(selected_n_nodes[ind])
	return final_nodes

def write_out(final_nodes, out_filename):
	'''
	THis function write out the finally choosed (num_seeds * rounds) nodes.
	'''
	fid = open(out_filename, 'w')
	for i in range(len(final_nodes)):
		if i == len(final_nodes)-1:
			fid.write(final_nodes[i])
		else:
			fid.write(final_nodes[i] + '\n')
	fid.close()

def max_cluster(graph, num_clusters, atmost_nodes_num):
	'''
	This function cut the whole graph and get a max sub_cluster with < (atmost_nodes_num) nodes.
	'''
	num_of_cluster_nodes = float('inf') # clustering at least for once
	while num_of_cluster_nodes >= atmost_nodes_num:
		graph, max_len = get_largest_cluster(graph, num_clusters)
		num_of_cluster_nodes = max_len
	return graph, max_len

if __name__ == "__main__":
	filename = sys.argv[1] # input json filename

	cluster_flag = sys.argv[2] # do clustering or not

	num_seeds = int(filename.split('.')[1])# number of nodes we can select
	
	strategy_name = sys.argv[3] # use which strategy ("deg" / "clo" / "bet" / "aggr")
	final_name = "_".join(filename.split('.')[:-1]) + "_" + strategy_name + ".txt" # output filename
	
	overlap_ratio = float(sys.argv[4]) # choose what ratio of overlapped (intersected of three centrality) nodes
	
	num_clusters = int(sys.argv[5]) # number of clusters from each clustering operation
	
	atmost_nodes_num = int(sys.argv[6]) # at most atmost_nodes_num nodes can be in the final graph
	
	ratio = float(sys.argv[7])

	G = read_graph(filename)
	origin_graph = nx.Graph(G) # create the graph object
	select_strategy(strategy_name, origin_graph, cluster_flag, num_seeds, ratio, num_clusters, atmost_nodes_num, final_name) # get final result
	