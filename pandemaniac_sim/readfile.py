import json

def readGraph(filename):
	G = {}
	with open('testgraph1.json') as file:
    	data = json.load(file)
	return G
