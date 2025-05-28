from node import *
from segment import *
from path import *
import matplotlib.pyplot as plt
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class Graph:
    def __init__ (self, name):
        self.nodes = []
        self.segments = []
        self.selected_node = None
        self.name = name
#Clase graph con una lista de nodos y segmentos

def FindCoordinates(g,n):
    i=0
    found = False
    while i<len(g.nodes) and not found:
        if n == g.nodes[i].name:
            found = True
        else:
            i+=1
    return [g.nodes[i].x, g.nodes[i].y]

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
        SaveGraph(g)
        return True
#Funcion que recorre la lista de nodos, si no encuentra el nodo que se desea añadir, se añade y se devuelve True, si ya estaba, solo se devuelve False

def CreateNode(g,n,x,y):
    i=0
    found = False
    while i<len(g.nodes) and not found:
        if n == g.nodes[i]:
            found = True
        i+=1
    if not found:
        AddNode(g,Node(n,x,y))
    else:
        print("ya existe un nodo con ese nombre")

def DeleteNode(g,n):
    i=0
    found = False
    while i<len(g.nodes) and not found:
        if n == g.nodes[i].name:
            found = True
        else:
            i+=1
    if found:
        print("Longitud de nodes: ", len(g.nodes))
        g.nodes.pop(i)
        print("Longitud de nodes: ", len(g.nodes))
        SaveGraph(g)

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
        SaveGraph(g)
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

def GetClosestNeightbor(g, x,y):
    closest = g.nodes[0]
    punto = Node("punto",x,y)
    for i in g.nodes:
        if Distance(punto,closest)>Distance(punto,i) and Distance(punto,i) >= 0.1:
            print(i.name)
            print(Distance(punto, i))
            closest = i
    return closest
#Crea un nodo (sin añadirlo a la lista) con nombre "punto" y la posicion que se quiere comparar
#Recorre la lista de nodos, comprobando si la distancia del punto al cercano es mayor o menor a la del punto al nodo a comprobar y si es mayor, el cercano pasa a ser ese nuevo punto

def on_click(event, g, label, x_interface, y_interface):
    x, y = event.xdata, event.ydata
    if x is not None and y is not None:
        closest_node = GetClosest(g, x, y)
        g.selected_node = closest_node
        print(f"Clicked at: ({x}, {y})")
        print(f"Closest node: {closest_node.name}")
        x_interface.set(x)
        y_interface.set(y)
        label.config(text=f"Selected Node: {closest_node.name}")

def PlotOG(g):
    min_x = min(node.x for node in g.nodes)
    max_x = max(node.x for node in g.nodes)
    min_y = min(node.y for node in g.nodes)
    max_y = max(node.y for node in g.nodes)
    width = max_x - min_x
    height = max_y - min_y
    arrow = max(width, height) * 0.015

    for i in g.segments:
        adj = (Distance(i.origin,i.destination)-arrow)/Distance(i.origin,i.destination)
        plt.arrow(i.origin.x,i.origin.y,(i.destination.x-i.origin.x)*adj,(i.destination.y-i.origin.y)*adj, head_width=arrow, head_length=arrow, fc='blue', ec='blue')
        plt.text((i.origin.x+i.destination.x)/2,(i.origin.y+i.destination.y)/2,str(i.cost//0.01/100),color='black', fontsize=6, weight='bold')
    for i in g.nodes:
        plt.plot(i.x,i.y,"o",color = "black",markersize=4)
        plt.text(i.x+0.04,i.y+0.04,str(i.name),color='black', fontsize=6, weight='bold')
    plt.axis('auto')
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Grafico con nodos y segmentos')
    plt.show()
 #muestra los nodos y su nombre arriba a la derecha
 #Muestra los segmentos como flechas y la longitud de estos en el centro

def Plot(g, root=None, label=None, x_interface=None, y_interface=None):
    fig, ax = plt.subplots(figsize=(10, 10))  # Reasonable default, will scale with window
    if g.nodes != []:
        min_x = min(node.x for node in g.nodes)
        max_x = max(node.x for node in g.nodes)
        min_y = min(node.y for node in g.nodes)
        max_y = max(node.y for node in g.nodes)
        width = max_x - min_x
        height = max_y - min_y
        arrow = max(width, height) * 0.015

    # Plot nodes
    for i in g.nodes:
        ax.plot(i.x, i.y, "o", color="black", markersize=4)
        ax.text(i.x + 0.04, i.y + 0.04, str(i.name), color='black', fontsize=6, weight='bold')

    # Plot segments
    for i in g.segments:
        adj = (Distance(i.origin, i.destination) - arrow) / Distance(i.origin, i.destination)
        ax.arrow(i.origin.x, i.origin.y,
                 (i.destination.x - i.origin.x) * adj,
                 (i.destination.y - i.origin.y) * adj,
                 head_width=arrow, head_length=arrow, fc='blue', ec='blue')
        ax.text((i.origin.x + i.destination.x) / 2,
                (i.origin.y + i.destination.y) / 2,
                str(i.cost//0.01/100),
                color='black', fontsize=6, weight='bold')

    # Set axis limits and appearance
    ax.axis('auto')
    ax.grid(color='red', linestyle='dashed', linewidth=0.5)
    ax.set_title('Grafico con nodos y segmentos')

    if root is not None:
        fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, g, label, x_interface, y_interface))

        # Embed and expand the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.grid(row=6, column=3, sticky='nsew')  # Expand to fill grid cell

        # Make row 6 and column 3 expandable
        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(3, weight=1)

    plt.close(fig)


def PlotNode(g,nameOrigin):
    min_x = min(node.x for node in g.nodes)
    max_x = max(node.x for node in g.nodes)
    min_y = min(node.y for node in g.nodes)
    max_y = max(node.y for node in g.nodes)
    width = max_x - min_x
    height = max_y - min_y
    arrow = max(width, height) * 0.015

    for i in g.nodes:
        plt.plot(i.x,i.y,"o",color = "gray",markersize=4)
        plt.text(i.x+0.04,i.y+0.04,str(i.name),color='gray', fontsize=6, weight='bold')
    i=0
    found = False
    while i<len(g.nodes) and not found:
        if nameOrigin == g.nodes[i].name:
            found = True
        else:
            i+=1
    if found:
        plt.plot(g.nodes[i].x,g.nodes[i].y,"o",color = "red",markersize=4)
        plt.text(g.nodes[i].x+0.04,g.nodes[i].y+0.04,str(g.nodes[i].name),color = "red", fontsize=6, weight='bold')
    for j in g.nodes[i].neighbors:
        adj = (Distance(g.nodes[i],j)-arrow)/Distance(g.nodes[i],j)
        plt.arrow(g.nodes[i].x,g.nodes[i].y,(j.x-g.nodes[i].x)*adj,(j.y-g.nodes[i].y)*adj, head_width=arrow, head_length=arrow, fc='blue', ec='blue')
        for k in g.segments:
            if (k.origin == g.nodes[i] and k.destination == j) or (k.origin == j and k.destination == g.nodes[i]):
                distancia = str(k.cost//0.01/100) 
                break
        plt.text((g.nodes[i].x+j.x)/2,(g.nodes[i].y+j.y)/2,str(distancia),color='black', fontsize=6, weight='bold')
    plt.axis("auto")
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Grafico con los vecinos del nodo '+nameOrigin)
    plt.show()
#Busca el nombre del nodo seleccionado en la lista de nodos y la posicion de este pasa a ser i
#Plot del nodo y nombre
#plot de los vecionos, nombre, y segmentos del origen a sus vecinos

def SaveGraph(g):
    F = open(g.name,"w")
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
    g=Graph(filename)
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

def Reachability(g,nodename, max_dist=1000):
    i=0
    found = False
    while i <len(g.nodes) and not found:
        if g.nodes[i].name==nodename:
            origin = g.nodes[i]
            found= True
        else:
            i+=1       #Busca el nodo que queremos y lo añade a la lista de los nodos a los que llega
    
    if found:
        reach =[origin]
        new = True
        while new:
            new = False
            for nodo in reach:
                for vecino in nodo.neighbors:
                    if vecino not in reach:
                        for segment in g.segments:
                            if segment.origin == nodo and segment.destination == vecino:
                                print(segment.origin)
                                print(segment.cost)
                                if(segment.cost <= max_dist):
                                    print(vecino.name)
                                    reach.append(vecino)
                                    new = True
        print(reach)
        return reach
    #Pasa por la lista de los nodos a los que llega y añade los vecinos (los nodos a los que se puede llegar directamente) de los nodos de esta lista si no estan ya en ella.
    #Si hace una pasada y no consigue añadir ningun nodo, habra añadido todos a los que se puede llegar y para

    else:
        print("No se ha encontrado dicho nodo.")

def PlotReachability(g,reach, max_dist=1000):
    min_x = min(node.x for node in g.nodes)
    max_x = max(node.x for node in g.nodes)
    min_y = min(node.y for node in g.nodes)
    max_y = max(node.y for node in g.nodes)
    width = max_x - min_x
    height = max_y - min_y
    arrow = max(width, height) * 0.015

    for i in g.segments:
        adj = (Distance(i.origin,i.destination)-arrow)/Distance(i.origin,i.destination)
        plt.arrow(i.origin.x,i.origin.y,(i.destination.x-i.origin.x)*adj,(i.destination.y-i.origin.y)*adj, head_width=arrow, head_length=arrow, fc='gray', ec='gray')
        plt.text((i.origin.x+i.destination.x)/2,(i.origin.y+i.destination.y)/2,str(i.cost//0.01/100),color='gray', fontsize=6, weight='bold')
    for i in g.nodes:
        plt.plot(i.x,i.y,"o",color = "gray",markersize=4)
        plt.text(i.x+0.04,i.y+0.04,str(i.name),color='gray', fontsize=6, weight='bold')
    for i in reach: #Similar a PlotNode pero con todos los elementos de la lista que devuelve reach
        plt.plot(i.x,i.y,"o",color = "black",markersize=4)
        plt.text(i.x+0.04,i.y+0.04,i.name,color = "black", fontsize=6, weight='bold')
        for j in i.neighbors:
            if max_dist >= Distance(i, j):
                adj = (Distance(i,j)-arrow)/Distance(i,j)
                plt.arrow(i.x,i.y,(j.x-i.x)*adj,(j.y-i.y)*adj, head_width=0.05, head_length=0.05, fc='blue', ec='blue')
                for k in g.segments:
                    if (k.origin == i and k.destination == j) or (k.origin == j and k.destination == i):
                        distancia = str(k.cost//0.01/100) 
                        break
                plt.text((i.x+j.x)/2,(i.y+j.y)/2,str(distancia),color='black', fontsize=6, weight='bold')
    plt.axis("auto")
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Grafico del alcance de '+reach[0].name)
    plt.show()

def FindShortestPath(g, originName, destinationName):  # Se ha seguido el algoritmo sugerido en atenea
    origin = None
    destination = None
    found = 0
    i = 0

    while i < len(g.nodes) and found < 2:
        if originName == g.nodes[i].name:
            found += 1
            origin = g.nodes[i]
        elif destinationName == g.nodes[i].name:
            found += 1
            destination = g.nodes[i]
        i += 1

    # Si no se encontraron ambos nodos, retorna None
    if origin is None or destination is None:
        print(f"Error: Nodo origen '{originName}' o destino '{destinationName}' no encontrado en el grafo.")
        return None

    paths = [Path()]
    AddNodeToPath(paths[0], origin)

    while len(paths) > 0:
        lowest = paths[0]
        for path in paths:
            if PathLength(path) + Distance(path.nodes[-1], destination) < PathLength(lowest) + Distance(lowest.nodes[-1], destination):
                lowest = path
        paths.remove(lowest)  # Busca el nodo con la menor distancia estimada y lo guarda aparte

        for neighbor in lowest.nodes[-1].neighbors:
            if neighbor == destination:
                AddNodeToPath(lowest, neighbor)  # Si ya ha llegado al destino
                return lowest
            elif neighbor not in lowest.nodes:  # Evita ciclos
                iteraciones = 0
                coste = PathLength(lowest) + Distance(lowest.nodes[-1], neighbor)
                for p in paths:
                    if neighbor in p.nodes:
                        if coste >= PathLength(p):
                            iteraciones += 1
                        else:
                            paths.remove(p)

                if iteraciones < 1:
                    new_path = Path()
                    new_path.nodes = list(lowest.nodes)
                    new_path.segments = list(lowest.segments)
                    AddNodeToPath(new_path, neighbor)
                    paths.append(new_path)
    # Si no se encontró camino
    return None

def DeleteSegment(g, s):
    i = 0
    found = False
    while i < len(g.segments) and not found:
        if s == g.segments[i].name:
            found = True
        else:
            i += 1
    if found:
        print("Longitud de segments:", len(g.segments))
        origin = g.segments[i].origin
        destination = g.segments[i].destination
        g.segments.pop(i)
        if destination in origin.neighbors:
            origin.neighbors.remove(destination)
        print("Longitud de segments:", len(g.segments))
        SaveGraph(g)

def CreateGraph_1 ():
    G = Graph("graph.txt")
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddSegment(G,"A","B")
    AddSegment(G,"A","E")
    AddSegment(G,"A","K")
    AddSegment(G,"B","A")
    AddSegment(G,"B","C")
    AddSegment(G,"B","F")
    AddSegment(G,"B","K")
    AddSegment(G,"B","G")
    AddSegment(G,"C","D")
    AddSegment(G,"C","G")
    AddSegment(G,"D","G")
    AddSegment(G,"D","H")
    AddSegment(G,"D","I")
    AddSegment(G,"E","F")
    AddSegment(G,"F","L")
    AddSegment(G,"G","B")
    AddSegment(G,"G","F")
    AddSegment(G,"G","H")
    AddSegment(G,"I","D")
    AddSegment(G,"I","J")
    AddSegment(G,"J","I")
    AddSegment(G,"K","A")
    AddSegment(G,"K","L")
    AddSegment(G,"L","K")
    AddSegment(G,"L","F")
    return G

def filtrar_por_distancia(grafo, min_dist, max_dist):

    fig, ax = plt.subplots(figsize=(10, 10))

    arrow_size = 0.015 * max(
        max(node.x for node in grafo.nodes) - min(node.x for node in grafo.nodes),
        max(node.y for node in grafo.nodes) - min(node.y for node in grafo.nodes)
    )

    # Dibujar todos los nodos
    for node in grafo.nodes:
        ax.plot(node.x, node.y, "o", color="gray", markersize=4)
        ax.text(node.x + 0.04, node.y + 0.04, node.name, color='gray', fontsize=6)

    # Dibujar solo los segmentos en el rango de distancia
    for seg in grafo.segments:
        if min_dist <= seg.cost <= max_dist:
            adj = (seg.cost - arrow_size) / seg.cost
            ax.arrow(
                seg.origin.x, seg.origin.y,
                (seg.destination.x - seg.origin.x) * adj,
                (seg.destination.y - seg.origin.y) * adj,
                head_width=arrow_size, head_length=arrow_size,
                fc='blue', ec='blue'
            )
            ax.text(
                (seg.origin.x + seg.destination.x) / 2,
                (seg.origin.y + seg.destination.y) / 2,
                f"{seg.cost:.1f}",
                color='black', fontsize=6
            )

    ax.grid(color='red', linestyle='dashed', linewidth=0.5)
    ax.set_title(f"Segmentos entre {min_dist} y {max_dist} unidades")
    plt.axis('auto')
    plt.show()