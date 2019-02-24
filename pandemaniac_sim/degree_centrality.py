#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import readfile
import heapq
import sys
#
# This program implements the node selection via "Degree Centrality".
#

'''
How to run degree_centrality.py:
	python3 degree_centrality.py filename k
		filename: file path to test graph .json
		k: number of nodes of top k in the measurement of degree centrality
Output:
	print out the top k nodes (node_id, type: string)
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
	# print(graph_adj)
	degree_info = []
	for key, value in graph_adj.items():
		degree_i = len(value) / (num_nodes - 1)
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

if __name__ == "__main__":
	filename = sys.argv[1]
	k = int(sys.argv[2])
	graph_adj = readfile.read_graph(filename)
	degree_info = degree_centrality(graph_adj)
	# print("degree: ", degree_info)
	top_k_nodes = select_top_k(degree_info, k)
	print("top k: ", top_k_nodes)
