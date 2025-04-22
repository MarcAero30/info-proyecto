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
        origen = path.nodes[len(path.nodes)-2]
        destino = path.nodes[len(path.nodes)-1]
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
        return length
    else:
        return -1 #Suma la longitud de todos los segmentos

def PlotPath (g, path):
    for i in g.nodes: #Igual que en PlotNode
        plt.plot(i.x,i.y,"o",color = "gray",markersize=4)
        plt.text(i.x+0.5,i.y+0.5,str(i.name),color='black', fontsize=6, weight='bold')
    for i in g.segments: #Igual que en Plot
        adj = (Distance(i.origin,i.destination)-0.6)/Distance(i.origin,i.destination)
        plt.arrow(i.origin.x,i.origin.y,(i.destination.x-i.origin.x)*adj,(i.destination.y-i.origin.y)*adj, head_width=0.5, head_length=0.6, fc='gray', ec='gray')
        plt.text((i.origin.x+i.destination.x)/2,(i.origin.y+i.destination.y)/2,str(Distance(i.origin,i.destination)//0.01/100),color='black', fontsize=6, weight='bold')
    for i in path.nodes: 
        plt.plot(i.x,i.y,"o",color = "blue",markersize=4)
    for i in path.segments:
        adj = (Distance(i.origin,i.destination)-0.6)/Distance(i.origin,i.destination)
        plt.arrow(i.origin.x,i.origin.y,(i.destination.x-i.origin.x)*adj,(i.destination.y-i.origin.y)*adj, head_width=0.5, head_length=0.6, fc='blue', ec='blue')
    plt.axis([-5,25,-5,25])
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Camino')
    plt.show()