import pickle as pkl
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
import os

def identify_cascades(GTD_event_dict, id_to_groups, groups_to_id):
	attack_times = defaultdict(list)
	for attack, attack_info in GTD_event_dict.iteritems():
		timestamp = (attack_info['iday']*1.0)/(31.0*365.0) + (attack_info['iyear']-1970) + (attack_info['imonth']/12.0)
		attack_times[(attack_info['weaptype1'], attack_info['attacktype1'], attack_info['targtype1'], attack_info['region'])].append((groups_to_id[attack_info['gname']],timestamp))

	return attack_times

def print_attacks(attack_times, id_to_groups):
	data = open("../../data/full_cascade_fastinf_noun.txt", 'w+')

	for group in id_to_groups:
		# data.write('%d,%s\n' % (group, id_to_groups[group]))
		data.write('%d,%d\n' % (group, group))
	data.write('\n') 

	for casc,timepair in attack_times.iteritems():
		used = set()
		used.add(1741)
		if (len(timepair) < 5): continue
		for val in timepair:
			if val[0] not in used:
				tag = "%d,%f," % (val[0],val[1])
				data.write(str(tag).rstrip('\n'))
				used.add(val[0])
		data.seek(-1, os.SEEK_END)
		data.truncate()
		data.write("\n")	
	data.close()

def main():
	with open("../../data/pkl/GTD_dict.p", 'rb') as f:
		GTD_event_dict = pkl.load(f)
	with open("../../data/pkl/id_to_groups.p") as f:
		id_to_groups = pkl.load(f)
	with open("../../data/pkl/groups_to_id.p") as f:
		groups_to_id = pkl.load(f)

	attack_times = identify_cascades(GTD_event_dict, id_to_groups, groups_to_id)

	print_attacks(attack_times, id_to_groups)

main()