from NavAirport import *
from NavPoint import *
from NavSegment import*
from AirSpace import*

from graph import *
from node import *
from segment import*

def LoadAirspace(name):
    air = AirSpace(name)
    F = open("Cat_nav.txt")
    linea = F.readline()
    while linea != "":
        trozos = linea.rstrip().split(" ")
        air.points.append(NavPoint(trozos[0],trozos[1],trozos[2],trozos[3]))
        linea = F.readline()    #Lee la lines y el primer elemento es el numero identificativo, el nombre, la latitud y la longitud
    
    F = open("Cat_seg.txt")
    linea = F.readline()
    while linea != "":
        trozos = linea.rstrip().split(" ")
        air.segments.append(NavSegment(trozos[0],trozos[1],float(trozos[2])))
        linea = F.readline()    #Lee la lines y el primer elemento es origen, el destino y la distancia

    F = open("Cat_aer.txt")
    linea = F.readline()
    while linea != "":
        airport = NavAirport (linea.rstrip()) #Añade el nombre del aeropuerto
        linea=F.readline()
        sid = linea.rstrip().split(".")
        while sid[-1] == "D": #Todos los sids tienen una D tras un punto, y los stars una A, por lo que mientras encuentre una D sera un sid, una A un star, y nada un nuevo aeropuerto
            airport.sids.append(".".join(sid))
            linea = F.readline()
            sid = linea.rstrip().split(".")
        while sid[-1] == "A":
            airport.stars.append(".".join(sid))
            linea = F.readline()
            sid = linea.rstrip().split(".")
        air.airports.append(airport)
    return air

def ConversionGraph(airspace):
    g = Graph(airspace.name)
    
    num_to_node = {}
    
    for nav_point in airspace.points:
        node = Node(nav_point.name,float(nav_point.lon),float(nav_point.lat))
        g.nodes.append(node)

        num_to_node[nav_point.num] = node
    
    for nav_segment in airspace.segments:
        origin_node = num_to_node.get(nav_segment.origin)
        destination_node = num_to_node.get(nav_segment.destination)
        if origin_node and destination_node:
            segment = Segment(origin_node.name+destination_node.name,origin_node,destination_node,distance=nav_segment.cost)
            g.segments.append(segment)
            AddNeighbor(origin_node,destination_node)
    
    return g