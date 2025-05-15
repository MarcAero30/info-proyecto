from NavAirport import *
from NavPoint import *
from NavSegment import*
from AirSpace import*

from graph import *
from node import *
from segment import*

def LoadAirspace():
    air = AirSpace()
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
        air.segments.append(NavSegment(trozos[0],trozos[1],trozos[2]))
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

def ConversionGraph(AirSpace):
    g=Graph()
    for i in AirSpace.points:
        g.nodes.append(Node(i.name,i.lat,i.lon))
    for i in AirSpace.segments:
        g.segments.append(Segment(i.origin+i.destination,i.origin,i.destination,i.distance))
        
    return g