import snap
import operator

Graph = snap.LoadEdgeList(snap.PNGraph, "/Users/juliaalison/Desktop/data/fastinf/exp_fastinf_loadedgelist.txt", 0, 1)

print Graph.GetNodes()
print Graph.GetEdges()

OutDegV = snap.TIntPrV()
snap.GetNodeOutDegV(Graph, OutDegV)

deglist = [(x.GetVal1(), x.GetVal2()) for x in OutDegV]

deglist.sort(key=operator.itemgetter(1), reverse=True)

print deglist