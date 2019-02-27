#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import readfile
import sim
import heapq
import sys
import collections
import numpy as np
#
# This program implements the randomized node selection via "Degree Centrality".
# Environment: Python 2.7
# Created by Yu Wu
#

'''
How to run degree_centrality.py:
	python degree_centrality.py filename num_seeds
		filename: file path to test graph .json
		num_seeds: number of nodes of top # (num_seeds) in the measurement of degree centrality
Output:
	print out the randomized top # (num_seeds) nodes (node_id, type: string)
'''

def degree_centrality(graph_adj):
	'''
	input: graph information (type: dict)
	output: degree information for each node (type: list of tuples)
			i.e., [(degree_of_node_i, node_i), ...]
			type: 
				degree_of_node_i: float
				node_i: string
	'''
	num_nodes = len(graph_adj)
	# print graph_adj
	degree_info = []
	for key, value in graph_adj.items():
		degree_i = float(len(value)) / (num_nodes - 1)
		degree_info.append((degree_i, str(key)))
	return degree_info

def select_top_k(degree_info, k):
	'''
	input: degree information for each node (type: list of tuples)
	       k: top k in the measurement of degree (type: int)
	output: top k degree nodes (list of string)
	'''
	heapq.heapify(degree_info)
	top_k_info = heapq.nlargest(k, degree_info)
	top_k_nodes = []
	for i in range(len(top_k_info)):
		node_id = top_k_info[i][1]
		top_k_nodes.append(node_id)
	return top_k_nodes

def random_choice_out(rounds, num_seeds, top_k_nodes, final_name):
	indices = list(range(num_seeds))
	fid = open(final_name, 'w')
	for i in range(rounds):
		shuffled_indices = np.random.permutation(indices)
		for j in range(num_seeds):
			ind = shuffled_indices[j]
			if (i == rounds-1) and (j == num_seeds-1):
		   		fid.write(top_k_nodes[ind])
		   	else:
		   		fid.write(top_k_nodes[ind]+'\n')
	fid.close()

def deg_main(graph_adj, num_seeds, ratio, rounds, final_name):
	k = int(num_seeds * ratio)
	degree_info = degree_centrality(graph_adj)
	top_k_nodes = select_top_k(degree_info, k)
	random_choice_out(rounds, num_seeds, top_k_nodes, final_name)

if __name__ == "__main__":

	filename = sys.argv[1]
	num_seeds = int(sys.argv[2])
	final_name = "_".join(filename.split('.')) + "_deg.txt"

	ratio = 1.5
	rounds = 50
	graph_adj = readfile.read_graph(filename)

	deg_main(graph_adj, num_seeds, ratio, rounds, final_name)

	# k = int(num_seeds * ratio)

	# degree_info = degree_centrality(graph_adj)
	# # print "degree: ", degree_info
	# top_k_nodes = select_top_k(degree_info, k)
	# print "top k: ", top_k_nodes

	# indices = list(range(num_seeds))

	# fid = open(final_name, 'w')
	# for i in range(rounds):
	# 	shuffled_indices = np.random.permutation(indices)
	# 	for j in range(num_seeds):
	# 		ind = shuffled_indices[j]
	# 		if (i == rounds-1) and (j == num_seeds-1):
	# 	   		fid.write(top_k_nodes[ind])
	# 	   	else:
	# 	   		fid.write(top_k_nodes[ind]+'\n')
	# fid.close()

	# # write out to "final.txt"
	# out_filename = "final.txt"
	# writefile.write_file(out_filename, top_k_nodes)


	# # for sim test
	# graph = graph_adj
	# nodes = collections.defaultdict(list)
	# nodes["strategy1"] = top_k_nodes
	# # nodes["strategy2"] = top_k_nodes
	# results = sim.run(graph, nodes)
	# print results