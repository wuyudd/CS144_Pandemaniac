def writefile(lst):
	file = open(“final.txt”, “w”)
	for i in range(50):
		for node in lst:
			file.write(node+'\n')
	file.close()
	return


