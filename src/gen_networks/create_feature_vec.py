import pickle as pkl
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
import os

def process_attacks(attacks_by_group, event_terror_info):
	group_features = defaultdict(list)
	features = ['latitude', 'longitude', 'nwound', 'propvalue', 'nkill', 'country', 'region', 'propextent', 'property', 'claimed']
	multifeatures = ['attacktype', 'targtype', 'targsubtype', 'natlty', 'weaptype', 'weapsubtype']
	for group, attacks in attacks_by_group.iteritems():
		if group == 0: continue
		for feature in features:
			group_features[group].append([r for r in (event_terror_info[attack][feature] for attack in attacks) if r is not None])
		for i, feature in enumerate(multifeatures):
			if i < 4:
				group_features[group].append([r for r in (event_terror_info[attack][feature + '1'] for attack in attacks) if r is not None] + 
					[r for r in (event_terror_info[attack][feature + '2'] for attack in attacks) if r is not None] + 
					[r for r in (event_terror_info[attack][feature + '3'] for attack in attacks) if r is not None]) 
			else:
				group_features[group].append([r for r in (event_terror_info[attack][feature + '1'] for attack in attacks) if r is not None] + 
					[r for r in (event_terror_info[attack][feature + '2'] for attack in attacks) if r is not None] + 
					[r for r in (event_terror_info[attack][feature + '3'] for attack in attacks) if r is not None] +
					[r for r in (event_terror_info[attack][feature + '4'] for attack in attacks) if r is not None])
		group_features[group].append([1 if event_terror_info[attack]['country']==event_terror_info[attack]['natlty1'] else 0 for attack in attacks]) 
	return group_features

def process_vecs(list_group_features):
	vectors_dict = {}
	for group,features in list_group_features.iteritems():
		# print features
		vectors_dict[group] = [np.nanmean(feature) if i < 5 and len(feature)>0 else None for i, feature in enumerate(features)] + [max(feature, key=feature.count) if len(feature) -1 > i > 4 and len(feature)>0 else None for i, feature in enumerate(features)] + [(sum(features[len(features)-1])*1.0)/(len(features[len(features)-1]))]
	return vectors_dict

def main():
	with open("../../data/pkl/GTD_dict.p", "rb") as f:
		event_terror_info = pkl.load(f)
	with open("../../data/pkl/attacks_by_group.p", "rb") as f:
		attacks_by_group = pkl.load(f)
	with open("../../data/pkl/id_to_groups.p", "rb") as f:
		id_to_groups = pkl.load(f)

	list_group_features = process_attacks(attacks_by_group, event_terror_info)
	vectors_by_id = process_vecs(list_group_features)
	pkl.dump(vectors_by_id, open("../../data/pkl/vectors_by_id.p", "wb"))

main()
