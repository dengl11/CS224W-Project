#####
#Based on FastInf Algorithm by Altan Alpay, Deniz Demir, Jie Yang for their CS 224W Project (2011)

import snap
import pickle as pkl
import numpy as np
import sys
from collections import defaultdict
import os
import math
import operator

k=300
d=1000000
alpha=1

def readfile(filename):
	cascades_list = []
	with open(filename) as fp:
		for line in fp:
			cascades_list.append(line)

	cascades_arr = []

	for casc in cascades_list:
		linesplit = [x for x in casc.split(',')]
		nodes = []
		for node in range(0,len(linesplit),2):
			nodes.append((int(linesplit[node]),float(linesplit[node+1])))
		cascades_arr.append(nodes)

	# print cascades_arr
	return cascades_arr

def fastInf(C):
	E_exp = {}
	E_pl = {}
	E_simple = {}
	for cascade in C:
		for i in range(0,len(cascade)):
			for j in range(i+1, min(i+1+d, len(cascade))):
				ni = cascade[i][0]
				nj = cascade[j][0]
				if (ni,nj) not in E_exp:
					E_exp[(ni,nj)] = 0
					E_simple[(ni,nj)]=0
					E_pl[(ni,nj)]=0
				E_exp[(ni,nj)] += calc_weight_exponential(cascade,i,j)
				E_pl[(ni,nj)] += calc_weight_powerlaw(cascade,i,j)
				E_simple[(ni,nj)] += calc_weight(i,j)

	return E_exp,E_pl,E_simple

def calc_weight(i,j):
	return 1.0/(j-i)

def calc_weight_exponential(cascade,i,j):
	if cascade[j][1]-cascade[i][1] != 0:
		num = np.exp(alpha*(cascade[j][1]-cascade[i][1])/100)
	else:
		return 0.0
	denom = 0.0
	for n in range(0,j):
		if cascade[j][1]-cascade[n][1] != 0:
			denom += np.exp(alpha*(cascade[j][1]-cascade[n][1])/100)

	return (num*1.0)/(denom*1.0)

def calc_weight_powerlaw(cascade,i,j):
	if cascade[j][1]-cascade[i][1] != 0:
		num = (cascade[j][1]-cascade[i][1])**(-1.0*alpha)
	else: 
		return 0.0
	denom = 0.0
	for n in range(0,j):
		if cascade[j][1]-cascade[n][1] != 0:
			denom += (cascade[j][1]-cascade[n][1])**(alpha*-1.0)
	return (num*1.0)/(denom*1.0)

def output_network(E_exp,E_pl,E_simple):
	E_exp_s = sorted(E_exp.items(), key=operator.itemgetter(1), reverse=True)
	E_simple_s = sorted(E_simple.items(), key=operator.itemgetter(1), reverse=True)
	E_pl_s = sorted(E_pl.items(), key=operator.itemgetter(1), reverse=True)
	f_exp = open('../../data/fastinf/exp_fastinf_edges.txt','w+')
	f_simp = open('../../data/fastinf/powerlaw_fastinf_edges.txt','w+')
	f_pl = open('../../data/fastinf/simple_fastinf_edges.txt', 'w+')
	f2_exp = open('../../data/fastinf/exp_fastinf_loadedgelist.txt', 'w+')
	f2_pl = open('../../data/fastinf/pl_fastinf_loadedgelist.txt', 'w+')
	f2_simp = open('../../data/fastinf/simp_fastinf_loadedgelist.txt', 'w+')




	for i in range(0,k):
		f_pl.write('%s\n' % str(E_pl_s[i]))
		f_exp.write('%s\n' % str(E_exp_s[i]))
		f_simp.write('%s\n' % str(E_simple_s[i]))

		f2_pl.write('%s %s\n' % (str(E_pl_s[i][0][0]), str(E_pl_s[i][0][1])))
		f2_exp.write('%s %s\n' % (str(E_exp_s[i][0][0]), str(E_exp_s[i][0][1])))
		f2_simp.write('%s %s\n' % (str(E_simple_s[i][0][0]), str(E_simple_s[i][0][1])))


	f_exp.close()
	f_pl.close()
	f_simp.close()


def main():
	C = readfile("../../data/full_cascade_fastinf_noun.txt")
	E_exp,E_pl,E_simple = fastInf(C)
	output_network(E_exp,E_pl,E_simple)



main()