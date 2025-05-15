from node import Distance, ShowNode
class Segment:
    def __init__(self,name,origin,destination,distance=0):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = distance
        if self.cost == 0:
            self.cost = Distance(origin,destination)
#Clase segmento con nombre, un nodo de origen, un nodo de destino y el coste: la distancia entre ambos nodos.

def ShowSegment(s):
    print("Nombre del segmento: ",s.name)
    print("Nodo origen:")
    ShowNode(s.origin)
    print("Nodo destino:")
    ShowNode(s.destination)
    print("Distancia: ",s.cost)
