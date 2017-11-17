import pickle
import snap
import plotly.plotly as py
from geopy.geocoders import Nominatim

raw_gtd_data = pickle.load(open('raw_gtd_data.pkl', 'rb'))
airports = open('airports.dat', 'r')
routes = open('routes.dat', 'r')
airport_dict = {}
country_list = []
city_list = []
country_node_dict = {}
city_node_dict = {}

gtd_id_dict = {}

country_network_by_relation = snap.TUNGraph.New()
city_network_by_traffic = snap.TUNGraph.New()

for i in range(len(raw_gtd_data)):
	gtd_id_dict[raw_gtd_data[i]['eventid']] = [raw_gtd_data[i]['country_txt'],raw_gtd_data[i]['city'], raw_gtd_data[i]['latitude'], raw_gtd_data[i]['longitude'], raw_gtd_data[i]['related']]

	if raw_gtd_data[i]['country_txt'] not in country_list:
		country_list += [raw_gtd_data[i]['country_txt']]
		country_network_by_relation.AddNode(len(country_list)-1)
		country_node_dict[raw_gtd_data[i]['country_txt']] = len(country_list)-1

for line in airports:
	values = line.split(',')
	airport_dict[values[0]] = values[2][1:len(values[2])-1]

	if airport_dict[values[0]] not in city_list:
		city_list += [airport_dict[values[0]]]
		city_network_by_traffic.AddNode(len(city_list)-1)
		city_node_dict[airport_dict[values[0]]] = len(city_list)-1
print 1
for line in routes:
	values = line.split(',')
	if values[3] in airport_dict and values[5] in airport_dict:
		city_network_by_traffic.AddEdge(city_node_dict[airport_dict[values[3]]], city_node_dict[airport_dict[values[5]]])
print 2
for key, value in gtd_id_dict.iteritems():
	related_event = value[4]
	if related_event == '':
		continue
	all_related = related_event.split(',')
	for eventid in all_related:
		if eventid in country_node_dict:
			country_network_by_relation.AddEdge(country_node_dict[value[0]], country_node_dict[gtd_id_dict[eventid][0]])
print 3
snap.SaveEdgeList(city_network_by_traffic, 'city_network_by_traffic.txt')
snap.SaveEdgeList(country_network_by_relation, 'country_network_by_relation.txt')

