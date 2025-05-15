from node import *
from segment import *
import matplotlib.pyplot as plt

class Path:
    def __init__(self):
        self.nodes= []
        self.segments = []

def AddNodeToPath(path, node): #Como no sera una funcion que use el usuario, añadiremos siempre los nodos en el orden del camino y siempre con segmentos existentes
    path.nodes.append(node)
    if len(path.nodes)>1:
        origen = path.nodes[-2]
        destino = path.nodes[-1]
        path.segments.append(Segment(origen.name + destino.name,origen,destino)) #Añade el nodo y crea un segmento entre el anterior añadido y este

def ContainsNode (path,node):
    i=0
    found = False
    while i <len(path.nodes):
        if path.nodes[i].name==node.name:
            found= True
        i+=1
    if found:
        return True
    else:
        return False
    
def PathLength(path):
    suma = 0
    for i in path.segments:
        suma+=i.cost
    return suma
    
def CostToNode(path,node):
    if ContainsNode(path,node):
        length=0
        i=0
        found = False
        while i<len(path.segments) and not found:
            length+=path.segments[i].cost
            i+=1
            if path.nodes[i].name == node.name:
                found = True
        return length  #Suma la longitud de todos los segmentos

def PlotPath (g, path):
    for i in g.nodes:
        plt.plot(i.x,i.y,"o",color = "gray",markersize=4)
        plt.text(i.x+0.04,i.y+0.04,str(i.name),color='gray', fontsize=6, weight='bold')    
    for i in path.nodes: 
        plt.plot(i.x,i.y,"o",color = "black",markersize=4)
    for i in path.segments:
        adj = (Distance(i.origin,i.destination)-0.05)/Distance(i.origin,i.destination)
        plt.arrow(i.origin.x,i.origin.y,(i.destination.x-i.origin.x)*adj,(i.destination.y-i.origin.y)*adj, head_width=0.05, head_length=0.05, fc='cyan', ec='cyan')
        for k in g.segments:
            if (k.origin == i.origin and k.destination == i.destination) or (k.origin == i.destination and k.destination == i.origin):
                distancia = str(k.cost//0.01/100) 
                break
        plt.text((i.origin.x+i.destination.x)/2,(i.origin.y+i.destination.y)/2,distancia,color='black', fontsize=6, weight='bold')
    plt.axis("auto")
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Camino mas corto entre '+path.nodes[0].name+" y "+path.nodes[-1].name)
    plt.show()