import pickle as pkl
import numpy as np
import sys
from collections import defaultdict
import os


# def calc_network(node_vectors):
# 	similarity_vector = {}
# 	for node, v0 in node_vectors.iteritems():
# 		for node2, v1 in node_vectors.iteritems():
# 			if node == node2: continue
# 			if node < node2: continue
# 			similarity = 0.0
# 			for i in range(0,5):
# 				if v1[i] and v0[i]:
# 					similarity += max((min(v1[i], v0[i])*1.0/max(v1[i], v0[i])*1.0),-(min(v1[i], v0[i])*1.0/max(v1[i], v0[i])*1.0))
# 			for i in range(5, len(v1)):
# 				if v1[i] == v0[i] and v1[i] is not None:
# 					similarity += 1
# 			similarity_vector[(node, node2)] = similarity
# 	print similarity_vector 
# 	return similarity_vector

def similarity_network(similarity_vector):
	with open('similarity.txt', 'wb+') as f:
		f.write('Happening')
		for nodes in similarity_vector:
			if similarity_vector[nodes]>10:
				print "met"
				f.write('%d %d\n' % (nodes[1], nodes[0]))


def main():
	# with open("../../data/pkl/vectors_by_id.p", "rb") as f:
	# 	node_vectors = pkl.load(f)

	# sim_vector = calc_network(node_vectors)
	# pkl.dump(sim_vector, open("../../data/pkl/sim_vector.p", "wb"))
	with open("../../data/pkl/sim_vector.p", "rb") as f:
		sim_vector = pkl.load(f)
	similarity_network(sim_vector)

main()