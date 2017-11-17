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

terrorist_group_dict = None
raw_terror_data = None 
months = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:30}

with open('data/gtd_group_dict.pkl', 'rb') as f:
	terrorist_group_dict=pkl.load(f)
f.close()

with open ('data/raw_gtd_data.pkl', 'rb') as f:
	raw_terror_data = pkl.load(f)
f.close()

# print raw_terror_data

def modified_dataset():
	approved_list = []

	for attack in raw_terror_data:
		for i in range(1996,2016):
			if attack['iyear']==str(i):
				if attack['region']=='10':
					approved_list.append(attack)
				break

	return approved_list

def iterate_cascades(terror_data):
	nodes_name = {}
	nodenum = 0
	attack_times = {}

	for attack in terror_data:
		if attack['gname'] not in nodes_name:
			nodes_name[attack['gname']]=nodenum
			nodenum += 1
		timestamp = int(attack['iday']) + (int(attack['iyear']) - 1996)*365 + int(attack['imonth'])*months[int(attack['imonth'])]
		# attack_times[nodes_name[attack['gname']]] = (int(attack['weaptype1']),int(attack['attacktype1']),int(attack['targtype1']),timestamp)
		if (int(attack['weaptype1']),int(attack['attacktype1']),int(attack['targtype1'])) not in attack_times:
			attack_times[(int(attack['weaptype1']),int(attack['attacktype1']),int(attack['targtype1']))] = []
		attack_times[(int(attack['weaptype1']),int(attack['attacktype1']),int(attack['targtype1']))].append((nodes_name[attack['gname']],timestamp))

	return attack_times, nodes_name

def output_cascades(cascades_dict,nodes_name):
	data = open("./data/terror_cascade_1996-2016_ME.txt", 'w+')
	unknown = 0
	for name in nodes_name:
    	if name != 'Unknown':
    		data.write('%d,%s\n' % (nodes_name[name], name))
		else:
			unknown = nodes_name[name]
                        

	for casc in cascades_dict:
		used = []
		for val in cascades_dict[casc]:
			if val[0]!=unknown:
				tag = "%d,%f," % (val[0],val[1])
				data.write(str(tag).rstrip('\n'))
		data.seek(-1, os.SEEK_END)
		data.truncate()
		data.write("\n")
	data.close()




def main():
	terror_data_list = modified_dataset()
	cascades_dict,nodes_name = iterate_cascades(terror_data_list)

	pkl.dump(cascades_dict, open('./data/cascades_list.pkl', 'w+'))
	pkl.dump(nodes_name, open('./data/name_dict.pkl', 'w+'))


	cascades = output_cascades(cascades_dict,nodes_name)


main()




