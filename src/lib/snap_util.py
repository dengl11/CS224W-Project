###########################################
###   Utility functions based on Snap   ###
###########################################

import snap
from collections import Counter
from itertools import combinations
import random 
import numpy as np


def nodes_id_vec(graph):
    """return a vector of node ids 
    Args:
        graph: 

    Return: 
    """
    Nodes = snap.TIntV()
    for x in graph.Nodes():
        Nodes.Add(x.GetId())
    return Nodes 

def nReciporcalEdges(graph):
    """ get number of reciprocal edges in graph 
    Return: 
    """
    count = 0 # count of edges who point to or from the same node 
    for x in graph.Nodes():
        count += len(set(x.GetOutEdges()) & set(x.GetInEdges()))
    return count / 2 

def nodes_by_condition(graph, condition):
    """return the nodes satisfying condition
    condition: lambda funtion returning true/false 
    """
    return [x for x in graph.Nodes() if condition(x)]


def nodes_count_by_out(nodes):
    """compute the count of nodes by out degree 
    Args:
        nodes: Graph.Nodes() 

    Return:  (out_deg, node count)
    """
    out_count = Counter() # out_deg -> count of nodes
    for x in nodes:
        out = x.GetOutDeg()
        if out == 0: continue
        out_count[out] += 1

    outdges = sorted(out_count.keys())
    nnodes = [out_count[x] for x in outdges ]
    return (outdges, nnodes)


def add_random_undir_edges(graph, E):
    """add E randome undirected edges to graph 
    Args:
        graph: 
        E:    # of edges

    Return: 
    """
    all_edges = list(combinations([x.GetId() for x in graph.Nodes()], 2))
    for (n1, n2) in random.sample(all_edges, E):
        graph.AddEdge(n1, n2)


def node_deg_count_vec(graph):
    """return a vector of dimension MaxDeg for undirected graph
    Args:
        graph: 

    Return: np array [count of nodes with deg = i] 
    """
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(graph, DegToCntV)
    counts = [(item.GetVal1(), item.GetVal2()) for item in DegToCntV] # [(deg, count)
    max_deg = max(x[0] for x in counts)
    ans = np.zeros(max_deg)
    for d, c in counts:
        ans[d-1] = c 
    return ans 
    

def node_deg_dist_vec(graph):
    """return a vector of distribution of nodes by degree for undirected graph 
    Args:
       graph: 

    Return: 
    """
    deg_vec = node_deg_count_vec(graph) # [count]
    return deg_vec/float(graph.GetNodes())

def expected_degree_undirected(graph):
    """get the expected degreee of undirected graph 
    Args:
        graph: snap.PUNGraph object representing an undirected graph

    Return: 
    """
    n = graph.GetNodes() # number of nodes
    return sum(x.GetDeg() for x in graph.Nodes())/float(n)




def edges_among_nodes(Graph, nodes):
    """return list of edges connecting nodes in undirected graph 
    Args:
        Graph: 
        nodes: [node_id]

    Return: 
    """
    return [(n1, n2) for (n1, n2) in combinations(nodes, 2) if Graph.IsEdge(n1, n2)]


def clustering_coefficient_for_node(Graph, node):
    """return the clustering coeffient for node 
    Args:
        Graph: 
        node: snap Node Instance 

    Return: 
    """
    deg = node.GetDeg() 
    if deg < 2: return 0
    nbrs = node.GetOutEdges()
    return 2. * len(edges_among_nodes(Graph, nbrs)) / (deg * (deg - 1))


def cluster_coefficient(Graph):
    """ get the average clustering coefficient 
    :param - Graph: snap.PUNGraph object representing an undirected graph

    return type: float
    returns: clustering coeffient of Graph 
    """    
    return np.mean([clustering_coefficient_for_node(Graph, x) for x in Graph.Nodes()])


def random_pairs(Graph, n):
    """return n random pairs of nodes from Graph
    Args:
        Graph: 
        n: 

    Return: iterator of (node_id_1, node_id_2)
    """
    nodes = set(x.GetId() for x in Graph.Nodes())
    nodes_1 = random.sample(nodes, n)
    nodes_2 = [random.sample(nodes - {x}, 1)[0] for x in nodes_1]
    return zip(nodes_1, nodes_2)
    
