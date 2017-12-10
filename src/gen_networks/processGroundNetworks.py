
import pickle as pkl
import numpy as np 
from collections import defaultdict
import os
import sys

def map_groups_to_idnum(terror_attack_data_raw):
	groups = set()
	groups_to_id = {}
	id_to_groups = {}
	for attack in terror_attack_data_raw:
		group = attack['gname']
		groups.add(group)

		if attack['gname2']:
			groups.add(attack['gname2'])

		if attack['gname3']:
			groups.add(attack['gname3'])

	id_count = 0
	for group in groups:
		groups_to_id[group] = id_count
		id_to_groups[id_count] = group
		id_count += 1

	# print groups_to_id,id_to_groups
	return groups_to_id, id_to_groups

def list_of_attacks_by_group(terror_attack_data_raw, groups_to_id):
	attacks_by_group = defaultdict(list)
	attack_perpetrators = {}
	attack_related_neighbors = {}
	for attack in terror_attack_data_raw:
		group = attack['gname']
		gid = groups_to_id[group]
		attacks_by_group[gid].append(attack['eventid'])
		attack_perpetrators[attack['eventid']] = [gid]
		if attack['gname2']:
			gid2 = groups_to_id[attack['gname2']]
			attacks_by_group[gid2].append(attack['eventid'])
			attack_perpetrators[attack['eventid']].append(gid2)
		if attack['gname3']:
			gid3 = groups_to_id[attack['gname3']]
			attacks_by_group[gid3].append(attack['eventid'])
			attack_perpetrators[attack['eventid']].append(gid3)

		if group == 'Unknown': continue
		if attack['related']:
			neighbors = [int(x) for x in attack['related'].replace('and', ',').replace('\\', '').replace(' ', ',').split(',') if x]
			attack_related_neighbors[attack['eventid']] = neighbors
	
	# print attack_perpetrators, attacks_by_group
	return attacks_by_group, attack_perpetrators, attack_related_neighbors

def find_related_groups(attack_perpetrators, attack_related_neighbors):
	group_network = defaultdict(set)
	group_network_weighted = defaultdict(list)

	for attack in attack_perpetrators:
		perps = attack_perpetrators[attack]
		for perp in perps:
			for perp2 in perps:
				if perp != perp2:
					group_network[perp].add(perp2)
					group_network_weighted[perp].append(perp2)

	for attack in attack_related_neighbors:
		perps = attack_perpetrators[attack]
		for related in attack_related_neighbors[attack]:
			if related in attack_perpetrators:
				related_perps = attack_perpetrators[related]
				for related_perp in related_perps:
					for perp in perps:
						if perp!=related_perp:
							group_network[perp].add(related_perp)
							group_network_weighted[perp].append(related_perp)

	return group_network, group_network_weighted

def main():
	with open("../../data/pkl/GTD_raw.p", 'rb') as f:
		terror_attack_data_raw = pkl.load(f)
	groups_to_id, id_to_groups = map_groups_to_idnum(terror_attack_data_raw)
	attacks_by_group, attack_perpetrators, attack_related_neighbors = list_of_attacks_by_group(terror_attack_data_raw, groups_to_id)
	related_groups, related_groups_weighted = find_related_groups(attack_perpetrators, attack_related_neighbors)

	pkl.dump(groups_to_id, open("../../data/pkl/groups_to_id.p", "wb"))
	pkl.dump(id_to_groups, open("../../data/pkl/id_to_groups.p", "wb"))
	pkl.dump(attacks_by_group, open("../../data/pkl/attacks_by_group.p", "wb"))
	pkl.dump(attack_perpetrators, open("../../data/pkl/attack_perpetrators.p", "wb"))
	pkl.dump(related_groups, open("../../data/pkl/related_groups.p", "wb"))
	pkl.dump(related_groups_weighted, open("../../data/pkl/related_groups_weighted.p", "wb"))
main()


