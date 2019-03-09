1. If you want to know what the graph look like:

python draw.py filename num_clusters

filename:
	2.10.10.json
num_clusters:
	if num_clusters == 1, draw the whole graph
	if num_clusters > 1, draw all the subgraphs of the origin graph by clustering method.

2. If you want to choose different strategy to get the final (num_seeds * rounds) nodes in a txt file:

python main.py filename cluster_flag strategy_name overlap_ratio n_cluster at_most_num_nodes pool_ratio

filename: 
	e.g., 2.10.10.json
cluster_flag: 
	0 or 1, whether to cut the graph to clusters or not
strategy_name: deg / clo / bet / aggr / union
	deg: highest degree
	clo: highest closeness
	bet: highest betweenness
	aggr: aggregate the above three with overlap_ratio
	union: union the first three
overlap_ratio: 
	used for strategy "aggr", define the ratio of nodes selected from the overlapped area (all three).
	If you don't choose the "aggr" strategy, then just set overlap_ratio as a float number.
n_clusters: 
	used when cluster_flag = 1, define the number of clusters for each cut operation. e.g., if n_clusters = 2, if the #_nodes of the largest cluster <= at_most_num_nodes, then we will take this largest cluster as the graph.
at_most_num_nodes: 
	used when cluster_flag = 1, the largest number of nodes the graph can have.
	If the cluster_flag = 0, then just set at_most_num_nodes as an int number.
pool_ratio: 
	redundancy when choosing candidate nodes. Usually we set it as a floag number > 1.0.

