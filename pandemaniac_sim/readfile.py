#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import sys

#
# This program reads in the JSON file.
# Created by Wen Gu
#

def read_graph(filename):
	'''
	input: filename (type: string)
	output: data (type: dict)
	'''
	data = {}
	with open(filename, 'r') as file:
		data = json.load(file)
	return data

# for test
if __name__ == "__main__":
	filename = sys.argv[1]
	graph_adj = read_graph(filename)
	print(graph_adj)