from NavAirport import *
from NavPoint import *
from NavSegment import*
from AirSpace import*

from graph import *
from node import *
from segment import*

def LoadAirspace(name, place):
    air = AirSpace(name)
    F = open(place+"_nav.txt")
    linea = F.readline()
    while linea != "":
        trozos = linea.rstrip().split(" ")
        air.points.append(NavPoint(trozos[0],trozos[1],trozos[2],trozos[3]))
        linea = F.readline()    #Lee la lines y el primer elemento es el numero identificativo, el nombre, la latitud y la longitud
    
    F = open(place+"_seg.txt")
    linea = F.readline()
    while linea != "":
        trozos = linea.rstrip().split(" ")
        air.segments.append(NavSegment(trozos[0],trozos[1],float(trozos[2])))
        linea = F.readline()    #Lee la lines y el primer elemento es origen, el destino y la distancia

    F = open(place+"_aer.txt")
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

def ExportToKML(g, filename): #Creamos un nuevo archivo con el nombre dado y se escriben todos los datos con el formato dado en atenea
    F= open(filename+".kml","w")

    F.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    F.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
    F.write("  <Document>\n")

    for node in g.nodes:
        F.write("    <Placemark>\n")
        F.write(f"      <name>{node.name}</name>\n")
        F.write("      <Point>\n")
        F.write(f"        <coordinates>{node.x},{node.y},0</coordinates>\n")
        F.write("      </Point>\n")
        F.write("    </Placemark>\n")

    for seg in g.segments:
        F.write("    <Placemark>\n")
        F.write(f"      <name>{seg.name}</name>\n")
        F.write("      <LineString>\n")
        F.write("        <tessellate>1</tessellate>\n")
        F.write("        <coordinates>\n")
        F.write(f"          {seg.origin.x},{seg.origin.y},0 {seg.destination.x},{seg.destination.y},0\n")
        F.write("        </coordinates>\n")
        F.write("      </LineString>\n")
        F.write("    </Placemark>\n")

    F.write("  </Document>\n")
    F.write("</kml>\n")
    F.close()

def NodeToKML(g,nodename): #Crear un grafo con un nodo y sus vecinos
    nodeGraph = Graph(g.name+"_"+nodename)
    for i in g.nodes:
        if i.name==nodename:
            node=i
            break

    if node == None:
        return None

    nodeGraph.nodes.append(node)
    for i in node.neighbors:
        nodeGraph.nodes.append(i)

    for seg in g.segments:
        if (seg.origin == node and seg.destination in node.neighbors) or (seg.destination == node and seg.origin in node.neighbors):nodeGraph.segments.append(seg)

    return nodeGraph


def ReachabilityToKML(g,reach): #Para pasar de la lista de nodos alcanzables a un grafo con dicha lista y sus segmentos
    KMLreach = Graph(g.name + "reach")
    KMLreach.nodes = reach

    node_names = []
    for n in reach:
        node_names.append(n.name)   

    for seg in g.segments:
        if seg.origin.name in node_names and seg.destination.name in node_names:
            KMLreach.segments.append(seg)
    return KMLreach