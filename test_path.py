from test_graph import G
from path import *
camino =  Path()
AddNodeToPath(camino, G.nodes[0])
AddNodeToPath(camino, G.nodes[1])
AddNodeToPath(camino, G.nodes[2])
AddNodeToPath(camino, G.nodes[3])

print(ContainsNode(camino,G.nodes[2]))
print(ContainsNode(camino,G.nodes[5]))

print(PathLength(camino))
print(CostToNode(camino,G.nodes[2]))

PlotPath(G,camino)