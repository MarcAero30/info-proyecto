from LoadAirspace import *
from graph import*
cat = LoadAirspace()
#for i in cat.points:
 #   print(i.num)
  #  print(i.name)
   # print(i.lat)
    #print(i.lon)

#for i in cat.segments:
 #   print(i.origin)
  #  print(i.destination)
   # print(i.distance)

#for i in cat.airports:
 #   print(i.name)
  #  print(i.sids)
   # print(i.stars)


PlotOG(ConversionGraph(cat))