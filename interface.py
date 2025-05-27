import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import platform

from graph import (
    Plot,
    AddNode,
    AddSegment,
    LoadGraph,
    PlotNode,
    DeleteNode,
    FindCoordinates,
    PlotReachability,
    Reachability,
    FindShortestPath,
    DeleteSegment,
    CreateGraph_1
)
from LoadAirspace import (
    LoadAirspace,
    ConversionGraph,
    ExportToKML,
    NodeToKML,
    ReachabilityToKML
)

from path import *
from node import *

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Graph Viewer")
ventana.state('zoomed')
ventana.configure(bg="#339fff")

# Variables globales
g = None
x_interface = tk.IntVar()
y_interface = tk.IntVar()

# Sidebar
sidebar = tk.Frame(ventana, bg="#1f2f3f", width=250)
sidebar.pack(side="left", fill="y")

# Main display area placeholder
main_area = tk.Frame(ventana, bg="#339fff")
main_area.pack(side="right", fill="both", expand=True)

# Labels
label = tk.Label(sidebar, text="Selected Node:", bg="#1f2f3f", fg="white", font=("Arial", 10, "bold"))
label.pack(pady=(20, 5), padx=10, anchor="w")

labelClosest = tk.Label(sidebar, text="", bg="#1f2f3f", fg="white")
labelClosest.pack(padx=10, anchor="w")

def select_file():
    global g
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {os.path.basename(file_path)}")
        g = LoadGraph(os.path.basename(file_path))
        Plot(g, main_area, label, x_interface, y_interface)
    else:
        print("No file selected")

def get_neighbors():
    PlotNode(g, label.cget("text").split(": ")[1])

def get_input_delete():
    global g
    n = label.cget("text").split(": ")[1]
    DeleteNode(g,n)
    show_graph(g.name)

def show_graph(g_name):
    global g
    g = LoadGraph(g_name)
    print("Name: ", g.name)
    Plot(g, main_area, label, x_interface, y_interface)

def show_graph_by_g(g):
    Plot(g, main_area, label, x_interface, y_interface)

alcanzables = []
def show_reachability():
    global alcanzables
    nodename = label.cget("text").split(": ")[1]
    alcanzables = Reachability(g, nodename)
    PlotReachability(g, Reachability(g, label.cget("text").split(": ")[1]))

shortest_path = []  

def show_shortest_path():
    global shortest_path
    shortest_path = FindShortestPath(g, entry2.get(), entry3.get())
    if shortest_path is not None:
        PlotPath(g, shortest_path)
    else:
        print("No se encontró camino")

def get_input_delete_s():
    global g
    DeleteSegment(g, entry4.get())
    show_graph_by_g(g)

def crear_nodo(nombre, x, y):
    AddNode(g, Node(nombre, x, y))
    print(g.name)
    show_graph(g.name)

def crear_segment(nombreOrigen, nombreDestino):
    AddSegment(g, nombreOrigen, nombreDestino)
    show_graph(g.name)

def open_create_node_window():
    new_window = tk.Toplevel()
    new_window.title("Nuevo Nodo")
    new_window.geometry("300x200")
    tk.Label(new_window, text="Nombre:").pack(pady=4)
    entry_nombre = tk.Entry(new_window)
    entry_nombre.pack(pady=2)

    # Etiqueta y entrada para X
    tk.Label(new_window, text="X:").pack(pady=4)
    entry_x = tk.Entry(new_window)
    entry_x.pack(pady=4)

    # Etiqueta y entrada para Y
    tk.Label(new_window, text="Y:").pack(pady=4)
    entry_y = tk.Entry(new_window)
    entry_y.pack(pady=2)

    # Botón Crear
    btn_crear = tk.Button(new_window, text="Crear", command=lambda: crear_nodo(entry_nombre.get(), entry_x.get(), entry_y.get()))
    btn_crear.pack(pady=4)

def open_create_segment_window():
    new_window = tk.Toplevel()
    new_window.title("Nuevo Segmento")
    new_window.geometry("300x200")
    tk.Label(new_window, text="Nodo de origen:").pack(pady=4)
    entry_nombre = tk.Entry(new_window)
    entry_nombre.pack(pady=2)

    # Etiqueta y entrada para X
    tk.Label(new_window, text="Nodo de destino").pack(pady=4)
    entry_x = tk.Entry(new_window)
    entry_x.pack(pady=4)

    # Botón Crear
    btn_crear = tk.Button(new_window, text="Crear", command=lambda: crear_segment(entry_nombre.get(), entry_x.get()))
    btn_crear.pack(pady=4)
def Google_Earth():
    # Abrir ventana para seleccionar archivo KML
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un archivo KML",
        filetypes=[("Archivos KML", "*.kml")]
    )

    if ruta_archivo:
        try:
            # Detecta el sistema operativo
            sistema = platform.system()

            if sistema == "Windows":
                os.startfile(ruta_archivo)
            elif sistema == "Darwin":  # macOS
                subprocess.call(["open", ruta_archivo])
            else:  # Linux
                subprocess.call(["xdg-open", ruta_archivo])
        except Exception as e:
            print("Error al abrir el archivo:", e)
def show_kml(nombre):
    ruta_archivo = f"{nombre}.kml"
    try:
        sistema = platform.system()
        if sistema == "Windows":
            os.startfile(ruta_archivo)
        elif sistema == "Darwin":  # macOS
            subprocess.call(["open", ruta_archivo])
        else:  # Linux
            subprocess.call(["xdg-open", ruta_archivo])
    except Exception as e:
        print(f"Error al abrir {ruta_archivo}:", e)

def LoadAirpacecat(name):
    global g
    airspace = LoadAirspace(name)
    g = ConversionGraph(airspace)
    Plot(g, main_area, label, x_interface, y_interface)

def LoadAirpacespain(name):
    global g
    airspace = LoadAirspace(name)
    g = ConversionGraph(airspace)
    Plot(g, main_area, label, x_interface, y_interface)

def LoadAirpaceECAC(name):
    global g
    airspace = LoadAirspace(name)
    g = ConversionGraph(airspace)
    Plot(g, main_area, label, x_interface, y_interface)

def reiniciar_y_mostrar_grafo1():
    CreateGraph_1()
    show_graph("graph.txt")

def show_kml_mapas(nombre):
    ruta_archivo = f"{nombre}"
    try:
        sistema = platform.system()
        if sistema == "Windows":
            os.startfile(ruta_archivo)
        elif sistema == "Darwin":  # macOS
            subprocess.call(["open", ruta_archivo])
        else:  # Linux
            subprocess.call(["xdg-open", ruta_archivo])
    except Exception as e:
        print(f"Error al abrir {ruta_archivo}:", e)

def exportar_vecinos_kml():
    nodename = label.cget("text").split(": ")[1]
    subgrafo = NodeToKML(g, nodename)

    if subgrafo is not None:
        filename = f"{nodename}_vecinos"     
        ExportToKML(subgrafo, filename)
        print(f"KML exportado: {filename}.kml")
        show_kml_mapas(filename + ".kml")    
    else:
        print("Nodo no encontrado.")
menubar = tk.Menu(ventana)

def exportar_reachability_kml():
    if not alcanzables:
        print("No se ha generado la lista de alcanzables aún.")
        return

    subgrafo = ReachabilityToKML(g, alcanzables)
    filename = label.cget("text").split(": ")[1] + "_alcanzables"
    ExportToKML(subgrafo, filename)
    print(f"KML exportado: {filename}.kml")
    show_kml_mapas(filename + ".kml")

def exportar_camino_corto_kml():
    if not alcanzables:
        print("No se ha generado la lista de alcanzables aún.")
        return

    subgrafo = ReachabilityToKML(g, alcanzables)
    filename = label.cget("text").split(": ")[1] + "_alcanzables"
    ExportToKML(subgrafo, filename)
    print(f"KML exportado: {filename}.kml")
    show_kml_mapas(filename + ".kml")

def export_shortest_path_kml():
    start = entry2.get()
    end = entry3.get()
    path_obj = FindShortestPath(g, start, end)
    if not path_obj:
        print("No hay camino encontrado")
        return

 
    node_list = path_obj.nodes 

    path_graph = type(g)(g.name + "_shortestpath")
    path_graph.nodes = node_list

    node_names = [n.name for n in node_list]
    
    for seg in g.segments:
        if seg.origin.name in node_names and seg.destination.name in node_names:
            path_graph.segments.append(seg)

    filename = f"Shortest_{start}-{end}"
    ExportToKML(path_graph, filename)
    print(f"KML exportado: {filename}.kml")
    show_kml_mapas(f"{filename}.kml")

menubar = tk.Menu(ventana)

# Menú Archivo
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Mostrar Graph 1", command=lambda: show_graph("graph.txt"))
file_menu.add_command(label="Mostrar Graph 2", command=lambda: show_graph("graph2.txt"))
file_menu.add_command(label="Abrir archivo", command=select_file)
menubar.add_cascade(label="Archivo", menu=file_menu)

# Menú MAPAS
mapas_menu = tk.Menu(menubar, tearoff=0)
mapas_menu.add_command(label="CATALUÑA", command=lambda: show_kml("cat"))
mapas_menu.add_command(label="ESPAÑA", command=lambda: show_kml("Spain"))
mapas_menu.add_command(label="EUROPA", command=lambda: show_kml("ECAC"))
mapas_menu.add_command(label="Abrir archivos kml", command=Google_Earth)
mapas_menu.add_command(label="Grafo Cataluña", command=lambda: LoadAirpacecat("Cat"))
mapas_menu.add_command(label="Grafo España", command=lambda: LoadAirpacespain("Spain"))
mapas_menu.add_command(label="Grafo Europa", command=lambda: LoadAirpaceECAC("ECAC"))
menubar.add_cascade(label="MAPAS", menu=mapas_menu)

# Menú Crear
create_menu = tk.Menu(menubar, tearoff=0)
create_menu.add_command(label="Crear nodo", command=open_create_node_window)
create_menu.add_command(label="Crear segmento", command=open_create_segment_window)
menubar.add_cascade(label="Crear", menu=create_menu)

ventana.config(menu=menubar)

# Botones con estilo
boton_style = {
    "width": 20,
    "height": 2,
    "bg": "#b04c0b",
    "fg": "white",
    "font": ("Arial", 10, "bold"),
    "bd": 0,
    "activebackground": "#d65a1f"
}

tk.Button(sidebar, text="Buscar nodos vecinos", command=get_neighbors, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Eliminar nodo", command=get_input_delete, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Alcance", command=show_reachability, **boton_style).pack(pady=5)
tk.Label(sidebar, text="Nodo 1:", bg="#1f2f3f", fg="white").pack(pady=(15, 5), padx=10, anchor="w")
entry2 = tk.Entry(sidebar, width=25)
entry2.pack(pady=5, padx=10)
tk.Label(sidebar, text="Nodo 2:", bg="#1f2f3f", fg="white").pack(pady=(15, 5), padx=10, anchor="w")
entry3 = tk.Entry(sidebar, width=25)
entry3.pack(pady=5, padx=10)
tk.Button(sidebar, text="Camino más corto", command=show_shortest_path, **boton_style).pack(pady=5)

tk.Label(sidebar, text="Nombre del Segmento a eliminar:", bg="#1f2f3f", fg="white").pack(pady=(15, 5), padx=10, anchor="w")
entry4 = tk.Entry(sidebar, width=25)
entry4.pack(pady=3.5, padx=10)

tk.Button(sidebar, text="Eliminar Segment", command=get_input_delete_s, **boton_style).pack(pady=5)

tk.Button(sidebar, text="Reiniciar Grafo 1", command=reiniciar_y_mostrar_grafo1, **boton_style).pack(pady=5)

tk.Button(sidebar, text="Vecinos en Google Earth", command=exportar_vecinos_kml, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Alcance en Google Earth", command=exportar_reachability_kml, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Ruta en Google Earth", command=export_shortest_path_kml, **boton_style).pack(pady=5)
# Loop
ventana.mainloop()
