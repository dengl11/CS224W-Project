import snap
import numpy as np
import matplotlib.pyplot as plt

def getDataPointsToPlot(Graph):
    """
    :param - Graph: snap.PUNGraph object representing an undirected graph
    
    return values:
    X: list of degrees
    Y: list of frequencies: Y[i] = fraction of nodes with degree X[i]
    """
    ############################################################################
    # TODO: Your code here!
    X, Y = [], []
    CntV = snap.TIntPrV()

    snap.GetOutDegCnt(Graph, CntV)
    for p in CntV:
        X.append(p.GetVal1())
        Y.append((p.GetVal2()*1.0)/Graph.GetNodes())


    ############################################################################
    print Graph.GetEdges()
    print Graph.GetNodes()
    return X, Y


def GraphFastInf():
    """
    Code for HW1 Q1.1
    """
    pl = snap.LoadEdgeList(snap.PUNGraph, "data/simp_fastinf_loadedgelist.txt")
    exp = snap.LoadEdgeList(snap.PUNGraph,"data/pl_fastinf_loadedgelist.txt")
    simp = snap.LoadEdgeList(snap.PUNGraph,"data/exp_fastinf_loadedgelist.txt")

    x_pl, y_pl = getDataPointsToPlot(pl)
    plt.plot(x_pl, y_pl, color = 'y', label = 'Power Law Network')

    x_exp, y_exp = getDataPointsToPlot(exp)
    plt.plot(x_exp, y_exp, linestyle = 'dashed', color = 'r', label = 'Exponential Network')

    x_simp, y_simp = getDataPointsToPlot(simp)
    plt.plot(x_simp, y_simp, linestyle = 'dotted', color = 'b', label = 'Simple Network')

    plt.xlabel('Node Degree')
    plt.ylabel('Proportion of Nodes with a Given Degree')
    plt.title('Degree Distribution of Power Law, Exponential, and Simple Implementations of NetInf')
    plt.legend()
    plt.show()

GraphFastInf()
