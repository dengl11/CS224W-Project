import snap
import csv
import pickle as pkl

# GTD graph group by org, year
gtd_graph_by_group_year = snap.TUNGraph.New()

# GTD graph group by org, year, month
gtd_graph_by_group_year_month = snap.TUNGraph.New()

# Raw GTD Tuples
raw_gtd_data = []

# Group Year Month Dictionary
gtd_group_dict = {}

with open('../../data/GTD/globalterrorismdb_0617dist.csv', 'rb') as f:
	reader = csv.DictReader(f)
	index = 0
	for row in reader:
		print index
		raw_gtd_data += [row]

		gtd_graph_by_group.AddNode(index)
		gtd_graph_by_group_year.AddNode(index)
		gtd_graph_by_group_year_month.AddNode(index)

		org_name = row['gname']
		year = row['iyear']
		month = row['imonth']

		if org_name in gtd_group_dict:

			if year in gtd_group_dict[org_name]:
				# build group, year network
				for i in range(1, 13):
					mo = str(i)
					if mo in gtd_group_dict[org_name][year]:
						for event_index in gtd_group_dict[org_name][year][mo]:
							gtd_graph_by_group_year.AddEdge(event_index, index)

				if month in gtd_group_dict[org_name][year]:
					# build group, year, month network
					for event_index in gtd_group_dict[org_name][year][month]:
						gtd_graph_by_group_year_month.AddEdge(event_index, index)

					gtd_group_dict[org_name][year][month] += [index]

				else:
					gtd_group_dict[org_name][year][month] = [index]

			else:
				gtd_group_dict[org_name][year] = {}
				gtd_group_dict[org_name][year][month] = [index]

		else:
			gtd_group_dict[org_name] = {}
			gtd_group_dict[org_name][year] = {}
			gtd_group_dict[org_name][year][month] = [index]

		index += 1

pkl.dump(gtd_group_dict, open('gtd_group_dict.pkl', 'wb'))
pkl.dump(raw_gtd_data, open('raw_gtd_data.pkl', 'wb'))

snap.SaveEdgeList(gtd_graph_by_group_year, 'gtd_graph_by_group_year.txt')
snap.SaveEdgeList(gtd_graph_by_group_year_month, 'gtd_graph_by_group_year_month.txt')
