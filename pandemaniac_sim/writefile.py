#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
#
# This program writes out the .txt file.
#

def write_file(filename, selected_nodes):
	'''
	input: list of selected nodes (type: list of string)
	output: write out to the "final.txt" file with 50 rounds of nodes separate by "\n"
			i.e.
			1
			2
			3
			1
			2
			3
			.
			.
			.
	'''
	round = 50 # number of rounds
	with open(filename, 'w') as file:
		for i in range(round):
			for node in selected_nodes:
				file.write(node + "\n")
	return

