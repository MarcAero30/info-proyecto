import math
class Node:
    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []
#Clase nodo con nombre, posicion x, posicion y y una lista de vecinos (nodos con los que esta conectado)
def AddNeighbor(n1,n2):
    found = False
    i=0
    while i < len(n1.neighbors) and not found:
        if n1.neighbors[i]==n2:
            found = True
        i+=1
    if found:
        return False
    else: 
        n1.neighbors.append(n2)
        return True
#Recorre la lista de vecinos, si en esta no se encuentra el vecino que se quiere añadir, lo añade y devuelve True, si no, solo devuelve False
def Distance(n1,n2):
    return math.sqrt((n2.x-n1.x)**2+(n2.y-n1.y)**2)
#Distancia euclidiana (teorema de pitagoras) entre nodos
def ShowNode(n):
    print("Nombre: ",n.name)
    print("Posicion x: ",n.x)
    print("Posicion y: ",n.y)