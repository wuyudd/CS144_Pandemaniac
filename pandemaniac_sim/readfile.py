import json

def readGraph(filename):
	G = {}
	with open(filename) as file:
    	data = json.load(file)
	return G
