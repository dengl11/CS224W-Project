import snap
import pickle as pkl
import numpy as np
import numpy.linalg as linalg
from numpy.random import uniform 
from numpy.random import randn
import scipy.stats
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
import os
from copy import deepcopy


raw_terror_data = None 

def defaultgname():
	return 'Unknown'

def clean_data():
	global raw_terror_data
	cleaned_data = deepcopy(raw_terror_data)
	for attack in raw_terror_data:
		if attack['gname'] != 'Unknown' and attack['gname'] != '':
			cleaned_data.remove(attack)

	with open('data/cleaned_terror_raw.pkl', 'w+b') as f2:
		pkl.dump(cleaned_data,f2)
	raw_terror_data = cleaned_data

def id_group_dict():
	global raw_terror_data
	group_name = {}
	nodenum = 0
	nodes_name = {}
	name_nodes = {}

	for attack in raw_terror_data:
		print attack['gname']
		group_name[attack['eventid']] = attack['gname']
		if attack['gname'] not in name_nodes:
			name_nodes[attack['gname']]=nodenum
			nodes_name[nodenum] = attack['gname']
			nodenum += 1
	with open('./data/gname_attackid.pkl', 'w+b') as f:
		pkl.dump(group_name, f)
	with open('./data/gname_nodenum.pkl', 'w+b') as f:
		pkl.dump(name_nodes, f)
	with open('./data/nodenum_gname.pkl', 'w+b') as f:
		pkl.dump(nodes_name, f)

	return group_name, name_nodes, nodes_name


def find_related(group_name, name_nodes):
	global raw_terror_data
	used = set()
	related_groups = defaultdict(list)
	for attack in raw_terror_data:
		related_string = attack['related']
		related = [x for x in related_string.split(',')]
		print attack['gname']
		print related
		groupnum = name_nodes[attack['gname']]
		for r in related:
			if r=='':
				pass
			if (attack['eventid'],r) not in used:
				if r in group_name:
					r_name = group_name[r]
					num = name_nodes[r_name]
					if groupnum != num:
						related_groups[groupnum].append(num)
					used.add((attack['eventid'],r))
	with open('./data/related_groups.pkl', 'w+b') as f:
		pkl.dump(related_groups, f)

	return related_groups


def make_txt(related_groups, nodes_name):
	data = open('./data/related_groups.txt', 'w+b')
	data2 = open('./data/related_groups_names.txt','w+b')
	for group in related_groups:
		for related_group in related_groups[group]:
			data.write('%d,%d\n' % (group,related_group))
			print "added: %d, %d" % (group,related_group)
			data2.write('%s,%s\n' % (nodes_name[group],nodes_name[related_group]))
			print "added: %s,%s" % (nodes_name[group],nodes_name[related_group])
	data.close() 
	data2.close()

def main():
	global raw_terror_data
	with open ('data/raw_gtd_data.pkl', 'rb') as f:
		raw_terror_data = pkl.load(f)
	clean_data()
	# with open('data/cleaned_terror_raw.pkl', 'rb') as f:
	# 	raw_terror_data = pkl.load(f)
	group_name, name_nodes, nodes_name = id_group_dict()
	related_groups = find_related(group_name, name_nodes)

	make_txt(related_groups,nodes_name)

main()
