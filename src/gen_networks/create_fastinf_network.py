import snap
import pickle as pkl
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
import os


def gen_ground(related_groups, Graph, id_to_groups):
	edges = open("../../data/full_edge_list_netinf.txt", 'w+')
	# edges_name = open("../../data/full_edge_list_names.txt", 'w+')
	for group, relateds in related_groups.iteritems():
		for related in relateds:
			if group != related:
				Graph.AddEdge(group, related)
				edges.write('%d;%d\n' % (group,related))
				# edges_name.write('%s | %s\n' % (id_to_groups[group],id_to_groups[related]))

	edges.close()
	# edges_name.close()

def add_nodes(Graph, groups):
	namelist = open("../../data/name_list.txt", 'w+')
	for group in groups:
		Graph.AddNode(group)
		namelist.write('%d,%s\n' % (group, groups[group]))
	namelist.close()

def processNetwork(Graph, id_to_groups):
	with open("../../data/fastinf_graph_noweights_features.txt", "w+") as f:
		f.write("RELATED GROUPS GRAPH:\n")
		f.write('Edges: %d\n' % Graph.GetEdges())
		f.write('Nodes: %d\n\n' % Graph.GetNodes())

		MxWcc = snap.GetMxWcc(Graph)
		f.write("MAX WCC:\n")
		f.write('Edges: %f ' % MxWcc.GetEdges())
		f.write('Nodes: %f \n' % MxWcc.GetNodes())
		f.write('Node List: ')
		for node in MxWcc.Nodes(): f.write('%d, ' % node.GetId())
		f.write('\n')
		for node in MxWcc.Nodes(): f.write('%s, ' % id_to_groups[node.GetId()])

		f.write("\n\nALL WCCs:")
		Components = snap.TCnComV()
		snap.GetWccs(Graph, Components)
		for i,CnCom in enumerate(Components):
			if CnCom.Len() < 10: continue
			f.write('\nWcc%d: ' % i)
			for nodeid in CnCom:
				f.write('%d, ' % nodeid) 

		MxScc = snap.GetMxScc(Graph)
		f.write("\n\nMAX SCC:\n")
		f.write('Edges: %f ' % MxScc.GetEdges())
		f.write('Nodes: %f \n' % MxScc.GetNodes())
		f.write('Node List: ')
		for node in MxScc.Nodes(): f.write('%d, ' % node.GetId())
		f.write('\n')
		for node in MxScc.Nodes(): f.write('%s, ' % id_to_groups[node.GetId()])

		f.write("\n\nALL SCCs:")
		Components = snap.TCnComV()
		snap.GetSccs(Graph, Components)
		for i,CnCom in enumerate(Components):
			if CnCom.Len() < 10: continue
			f.write('\nScc%d: ' % i)
			for nodeid in CnCom:
				f.write('%d, ' % nodeid) 

		f.write('\n\nCLUSTERING AND COMMUNITIES:\n')
		f.write('Clustering coefficient: %f\n' % snap.GetClustCf(Graph, -1))
		f.write('Num Triads: %d\n' % snap.GetTriads(Graph, -1))
		Nodes = snap.TIntV()
		for node in Graph.Nodes(): Nodes.Add(node.GetId())
		f.write('Modularity: %f' % snap.GetModularity(Graph, Nodes))


def main():
	with open("../../data/pkl/related_groups.p", "rb") as f:
		related_groups = pkl.load(f)

	with open("../../data/pkl/related_groups_weighted.p", "rb") as f:
		related_groups_weighted = pkl.load(f)
	
	with open("../../data/pkl/id_to_groups.p", "rb") as f:
		id_to_groups = pkl.load(f)

	Graph = snap.LoadEdgeList(snap.PNGraph, "../../data/final_graphs/full_terrorism_k300.txt", 0, 1)
	# add_nodes(Graph, id_to_groups)
	# gen_ground(related_groups, Graph, id_to_groups)

	processNetwork(Graph, id_to_groups)

main()

