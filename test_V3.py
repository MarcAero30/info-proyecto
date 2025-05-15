from LoadAirspace import *
from graph import*
cat = LoadAirspace("cat")
#for i in cat.points:
 #   print(i.num)
  #  print(i.name)
   # print(i.lat)
    #print(i.lon)

#for i in cat.segments:
 #   print(i.origin)
  #  print(i.destination)
   # print(i.cost)

#for i in cat.airports:
 #   print(i.name)
  #  print(i.sids)
   # print(i.stars)


G= ConversionGraph(cat)
PlotOG(G)
PlotNode(G,"GODOX")
PlotReachability(G,Reachability(G,"GODOX"))
PlotPath(G,FindShortestPath(G,"CAVES","ZZA"))