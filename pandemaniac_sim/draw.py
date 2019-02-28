#!/usr/bin/env python
# -*- coding: UTF-8 -*-

if __name__ == "__main__":
	filename = sys.argv[1] # input json filename
	G = read_graph(filename)
	origin_graph = nx.Graph(G) # create the graph object
	# select_strategy(strategy_name, origin_graph, cluster_flag, num_seeds, ratio, num_clusters, atmost_nodes_num, final_name) # get final result
	# draw the original graph and the max_cluster graph
	pos=nx.spring_layout(origin_graph, k = 0.15, iterations = 20, scale = 10)
	nx.draw(origin_graph,pos, with_labels = False, node_size = 0.1, width = 0.01)
	plt.show()