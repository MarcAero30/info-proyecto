from node import *
from segment import *
import matplotlib.pyplot as plt

class Graph:
    def __init__ (self):
        self.nodes = []
        self.segments = []
#Clase graph con una lista de nodos y segmentos

def AddNode(g,n):
    i=0
    found = False
    while i<len(g.nodes) and not found:
        if n == g.nodes[i]:
            found = True
        i+=1
    if found:
        return False
    else:
        g.nodes.append(n)
        return True
#Funcion que recorre la lista de nodos, si no encuentra el nodo que se desea añadir, se añade y se devuelve True, si ya estaba, solo se devuelve False

def AddSegment(g, nameOriginNode, nameDestinationNode):
    i=0
    found = 0
    while i <len(g.nodes) and found<2:
        if g.nodes[i].name == nameOriginNode:
            OriginNode=g.nodes[i]
            found+=1
        if g.nodes[i].name == nameDestinationNode:
            DestinationNode =g.nodes[i]
            found+=1
        i+=1
    if found == 2:    
        g.segments.append(Segment(nameOriginNode+nameDestinationNode,OriginNode,DestinationNode))
        AddNeighbor(OriginNode,DestinationNode)
        return True
    else:
        return False
#Funcion que recorre la lista de nodos comprovando sus nombres 
#Encuentra los dos seleccionados (origen y destino), devuelve True y añade a la lista de segmentos un segmento:
    #nombre(nombreorigen - nombredestino)
    #Origen, destino
#Si no devuelve False

def GetClosest (g, x,y):
    closest = g.nodes[0]
    punto = Node("punto",x,y)
    for i in g.nodes:
        if Distance(punto,closest)>Distance(punto,i):
            closest = i
    return closest
#Crea un nodo (sin añadirlo a la lista) con nombre "punto" y la posicion que se quiere comparar
#Recorre la lista de nodos, comprobando si la distancia del punto al cercano es mayor o menor a la del punto al nodo a comprobar y si es mayor, el cercano pasa a ser ese nuevo punto

def Plot(g):
    for i in g.nodes:
        plt.plot(i.x,i.y,"o",color = "red",markersize=4)
        plt.text(i.x+0.5,i.y+0.5,str(i.name),color='green', fontsize=6, weight='bold')
    for i in g.segments:
        adj = (Distance(i.origin,i.destination)-0.6)/Distance(i.origin,i.destination)
        plt.arrow(i.origin.x,i.origin.y,(i.destination.x-i.origin.x)*adj,(i.destination.y-i.origin.y)*adj, head_width=0.5, head_length=0.6, fc='blue', ec='blue')
        plt.text((i.origin.x+i.destination.x)/2,(i.origin.y+i.destination.y)/2,str(Distance(i.origin,i.destination)//0.01/100),color='black', fontsize=6, weight='bold')
    plt.axis([-5,25,-5,25])
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Grafico con nodos y segmentos')
    plt.show()
#muestra los nodos y su nombre arriba a la derecha
#Muestra los segmentos como flechas y la longitud de estos en el centro

def PlotNode(g,nameOrigin):
    for i in g.nodes:
        plt.plot(i.x,i.y,"o",color = "gray",markersize=4)
        plt.text(i.x+0.5,i.y+0.5,str(i.name),color='black', fontsize=6, weight='bold')
    i=0
    found = False
    while i<len(g.nodes) and not found:
        if nameOrigin == g.nodes[i].name:
            found = True
            i-=1
        i+=1
    if found:
        plt.plot(g.nodes[i].x,g.nodes[i].y,"o",color = "blue",markersize=4)
        plt.text(g.nodes[i].x+0.5,g.nodes[i].y+0.5,str(g.nodes[i].name),color = "black", fontsize=6, weight='bold')
    for j in g.nodes[i].neighbors:
        adj = (Distance(g.nodes[i],j)-0.6)/Distance(g.nodes[i],j)
        plt.plot(j.x,j.y,"o",color = "green",markersize=4)
        plt.arrow(g.nodes[i].x,g.nodes[i].y,(j.x-g.nodes[i].x)*adj,(j.y-g.nodes[i].y)*adj, head_width=0.5, head_length=0.6, fc='red', ec='red')
        plt.text((g.nodes[i].x+j.x)/2,(g.nodes[i].y+j.y)/2,str(Distance(g.nodes[i],j)//0.01/100),color='black', fontsize=6, weight='bold')
        plt.text(j.x+0.5,j.y+0.5,j.name,color = "black", fontsize=6, weight='bold')
    plt.axis([-5,25,-5,25])
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Grafico con nodos y segmentos')
    plt.show()
#Busca el nombre del nodo seleccionado en la lista de nodos y la posicion de este pasa a ser i
#Plot del nodo y nombre
#plot de los vecionos, nombre, y segmentos del origen a sus vecinos

def SaveGraph(g,filename):
    F = open(filename,"w")
    for i in g.nodes:
        F.write(str(i.name)+"\n")
        F.write(str(i.x)+"\n")
        F.write(str(i.y)+"\n")

    F.write("\n")
    for i in g.segments:
        F.write(str(i.name)+"\n")
        F.write(str(i.origin.name)+"\n")
        F.write(str(i.destination.name)+"\n")
    F.close()
#Guarda los nodos como:
#-nombre
#-x
#-y
#Antes de mostrar los segmentos, hace un \n para a la hora de leer, distinguir entre nodos y segmentos.
#Guarda los segmentos como:
#-nombre
#-nombre nodo origen
#-nombre nodo destino

def LoadGraph(filename):
    g=Graph()
    F=open(filename)
    linea = F.readline().rstrip()
    while linea != "":
        name = linea
        linea = F.readline().rstrip()
        x =  float(linea)
        linea = F.readline().rstrip()
        y = float(linea)
        linea = F.readline().rstrip()
        g.nodes.append(Node(name,x,y))
    linea = F.readline().rstrip()
    while linea != "":
        name = linea
        linea = F.readline().rstrip()
        origin=linea
        linea = F.readline().rstrip()
        destination=linea
        linea = F.readline().rstrip()
        AddSegment(g, origin, destination)
    F.close()
    return g
#Lee tres lineas, correspondientes a los tres parametros de nodes y añade el node, asi hasta encontrarse una linea en blanco, que significa que a partir de ahi estamos hablande de segmentos
#Lee tres lineas, correspondientes a los tres parametros de segments y añade el segmento mediante la funcion Addsegment, lo que a su misma vez añade los vecinos y las distancias de los nodos y segmentos correspondientemente

def Reachability(g,nodename):
    i=0
    found = False
    while i <len(g.nodes):
        if g.nodes[i].name==nodename:
            found= True
        i+=1       #Busca el nodo que queremos y lo añade a la lista de los nodos a los que llega
    i-=1
    if found:
        reach =[g.nodes[i]]
        new = True
        while new:
            new = False
            for nodo in reach:
                for vecino in nodo.neighbors:
                    if vecino not in reach:
                        reach.append(vecino)
                        new = True

        return reach
    #Pasa por la lista de los nodos a los que llega y añade los vecinos (los nodos a los que se puede llegar directamente) de los nodos de esta lista si no estan ya en ella.
    #Si hace una pasada y no consigue añadir ningun nodo, habra añadido todos a los que se puede llegar y para

    else:
        print("No se ha encontrado dicho nodo.")

def PlotReachability(g,reach):
    for i in g.nodes: #Igual que en PlotNode
        plt.plot(i.x,i.y,"o",color = "gray",markersize=4)
        plt.text(i.x+0.5,i.y+0.5,str(i.name),color='black', fontsize=6, weight='bold')
    for i in g.segments: #Igual que en Plot
        adj = (Distance(i.origin,i.destination)-0.6)/Distance(i.origin,i.destination)
        plt.arrow(i.origin.x,i.origin.y,(i.destination.x-i.origin.x)*adj,(i.destination.y-i.origin.y)*adj, head_width=0.5, head_length=0.6, fc='gray', ec='gray')
        plt.text((i.origin.x+i.destination.x)/2,(i.origin.y+i.destination.y)/2,str(Distance(i.origin,i.destination)//0.01/100),color='black', fontsize=6, weight='bold')
    for j in reach: #Similar a PlotNode pero con todos los elementos de la lista
        plt.plot(j.x,j.y,"o",color = "green",markersize=4)
        plt.text(j.x+0.5,j.y+0.5,j.name,color = "black", fontsize=6, weight='bold')
        for i in j.neighbors:
            adj = (Distance(i,j)-0.6)/Distance(i,j)
            plt.arrow(i.x,i.y,(j.x-i.x)*adj,(j.y-i.y)*adj, head_width=0.5, head_length=0.6, fc='green', ec='green')
            plt.text((i.x+j.x)/2,(i.y+j.y)/2,str(Distance(i,j)//0.01/100),color='black', fontsize=6, weight='bold')
    plt.axis([-5,25,-5,25])
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Grafico del alcance de '+reach[0].name)
    plt.show()