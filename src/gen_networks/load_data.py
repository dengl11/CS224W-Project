import pickle as pkl
import numpy as np 
from collections import defaultdict
import os
import sys


with open("../../data/pkl/GTD_raw.p", 'rb') as f:
	terror_attack_data_raw = pkl.load(f)

# print terror_attack_data_raw[0]

def correct_ints():
	newlist = []
	for row in terror_attack_data_raw:
		newrow = {}
		for key in row:
			if row[key]:
				try:
					newint = int(float(row[key]))
					newrow[key] = newint
				except (AttributeError, TypeError, ValueError):
					newrow[key] = row[key]
					pass
			elif row[key] is not None:
				if str(row[key]) == '0L' or str(row[key]) == '0':
					newrow[key] = 0
			else:
				newrow[key] = row[key]
		newlist.append(newrow)
	pkl.dump(newlist, open("../../data/pkl/GTD_raw2.p", 'wb'))

correct_ints()

with open("../../data/pkl/baad.p", 'rb') as f:
	terror_group_features = pkl.load(f)

# print terror_group_features
