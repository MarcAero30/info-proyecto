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
    try:
        global g
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Selected file: {os.path.basename(file_path)}")
            g = LoadGraph(os.path.basename(file_path))
            Plot(g, main_area, label, x_interface, y_interface)
        else:
            print("No file selected")
            messagebox.showerror("Error", "No file selected")
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def get_neighbors():
    try:
        PlotNode(g, label.cget("text").split(": ")[1])
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def get_input_delete():
    global g
    n = label.cget("text").split(": ")[1]
    DeleteNode(g,n)
    show_graph(g.name)

def show_graph(g_name):
    try:
        global g
        g = LoadGraph(g_name)
        print("Name: ", g.name)
        Plot(g, main_area, label, x_interface, y_interface)
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def show_graph_by_g(g):
    try:
        Plot(g, main_area, label, x_interface, y_interface)
    except:
        messagebox.showerror("Error", "Ha surgido un error")

alcanzables = []
def show_reachability():
    try:
        global alcanzables
        nodename = label.cget("text").split(": ")[1]
        alcanzables = Reachability(g, nodename)
        PlotReachability(g, Reachability(g, label.cget("text").split(": ")[1]))
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def open_filter_window():
    try:
        new_window = tk.Toplevel()
        new_window.title("Filtrar por distancia máxima")
        new_window.geometry("300x100")
        tk.Label(new_window, text="Distancia máxima entre puntos:").pack(pady=4)
        entry_dist = tk.Entry(new_window)
        entry_dist.pack(pady=2)

        # Botón Filtrar
        btn_filter = tk.Button(new_window, text="Filtrar", command=lambda: filter_distance(float(entry_dist.get())))
        btn_filter.pack(pady=4)
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def filter_distance(dist):
    try:
        PlotReachability(g, Reachability(g, label.cget("text").split(": ")[1], dist), dist)
    except:
        messagebox.showerror("Error", "Ha surgido un error")
shortest_path = []  

def show_shortest_path():
    try:
        global shortest_path
        shortest_path = FindShortestPath(g, entry2.get(), entry3.get())
        if shortest_path is not None:
            PlotPath(g, shortest_path)
        else:
            print("No se ha encontrado el camino")
            messagebox.showerror("Error", "No se ha encontrado el camino")
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def get_input_delete_s():
    try:
        global g
        DeleteSegment(g, entry4.get())
        show_graph_by_g(g)
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def crear_nodo(nombre, x, y):
    try:
        AddNode(g, Node(nombre, x, y))
        print(g.name)
        show_graph(g.name)
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def crear_segment(nombreOrigen, nombreDestino):
    try:
        AddSegment(g, nombreOrigen, nombreDestino)
        show_graph(g.name)
    except:
        messagebox.showerror("Error", "Ha surgido un error")

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
            messagebox.showerror("Error","Error al abrir el archivo:"+ e)

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
        messagebox.showerror("Error",f"Error al abrir {ruta_archivo}:"+ e)

def cargar_espacio_aereo(nombre):
    try:
        global g
        airspace = LoadAirspace(nombre)
        g = ConversionGraph(airspace)
        Plot(g, main_area, label, x_interface, y_interface)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el espacio aéreo '{nombre}':\n{str(e)}")

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
        messagebox.showerror("Error",f"Error al abrir {ruta_archivo}:"+ e)

def exportar_vecinos_kml():
    try:
        nodename = label.cget("text").split(": ")[1]
        subgrafo = NodeToKML(g, nodename)

        if subgrafo is not None:
            filename = f"{nodename}_vecinos"     
            ExportToKML(subgrafo, filename)
            print(f"KML exportado: {filename}.kml")
            show_kml_mapas(filename + ".kml")    
        else:
            print("Nodo no encontrado")
            messagebox.showerror("Error", "Nodo no encontrado")
    except:
        messagebox.showerror("Error", "Ha surgido un error")
menubar = tk.Menu(ventana)

def exportar_reachability_kml():
    try:
        if not alcanzables:
            print("No se ha podido generar la lista de alcanzables")
            messagebox.showerror("Error", "No se ha podido generar la lista de alcanzables")
            return

        subgrafo = ReachabilityToKML(g, alcanzables)
        filename = label.cget("text").split(": ")[1] + "_alcanzables"
        ExportToKML(subgrafo, filename)
        print(f"KML exportado: {filename}.kml")
        show_kml_mapas(filename + ".kml")
    except:
        messagebox.showerror("Error", "Ha surgido un error")

def export_shortest_path_kml():
    try:
        start = entry2.get()
        end = entry3.get()
        path_obj = FindShortestPath(g, start, end)
        if not path_obj:
            print("No se ha encontrado el camino")
            messagebox.showerror("Error", "No se ha encontrado el camino")
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
    except:
        messagebox.showerror("Error", "Ha surgido un error")
        
GRAPH_VACIO_FILE = "graph_vacio.txt"

def crear_grafo_vacio():
    print("Se está ejecutando crear_grafo_vacio()")
    global g
    from graph import Graph  # O la clase correcta de grafo que usas
    
    g = Graph("graph_vacio")  # Crear grafo vacío con ese nombre
    
    # Crear archivo vacío o reiniciarlo
    with open(GRAPH_VACIO_FILE, "w") as f:
        f.write(f"Nombre del grafo: {g.name}\nNodos:\nSegmentos:\n")
    
    # Mostrar grafo vacío en la interfaz
    show_graph_by_g(g)

def mostrar_grafo_en_google_earth():
    if g is None:
        print("No hay grafo cargado.")
        messagebox.showerror("Error", "No hay grafo cargado")
        return

    filename = g.name + "_visual"
    ExportToKML(g, filename)
    show_kml_mapas(filename + ".kml")

from tkinter import filedialog

def guardar_grafo_en_archivo():
    global g
    if g is None:
        print("No hay grafo cargado.")
        messagebox.showerror("Error", "No hay grafo cargado")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivo de texto", "*.txt")],
        title="Guardar grafo como..."
    )

    if file_path:
        g.name = file_path
        from graph import SaveGraph
        SaveGraph(g)
        print(f"Grafo guardado como: {file_path}")
        messagebox.showinfo("Guardado", f"Grafo guardado como:\n{file_path}")

def mostrar_selector_espacio_aereo():
    ventana_selector = tk.Toplevel()
    ventana_selector.title("Selecciona el espacio aéreo")
    ventana_selector.geometry("300x150")

    tk.Label(ventana_selector, text="Selecciona el espacio aéreo:").pack(pady=10)

    opciones = ["Cataluña", "España", "ECAC"]
    seleccion = tk.StringVar(value=opciones[0])  # valor por defecto

    menu = tk.OptionMenu(ventana_selector, seleccion, *opciones)
    menu.pack(pady=5)

    def cargar_seleccion():
        eleccion = seleccion.get()
        if eleccion == "Cataluña":
            cargar_espacio_aereo("Cat")
        elif eleccion == "España":
            cargar_espacio_aereo("Spain")
        elif eleccion == "ECAC":
            cargar_espacio_aereo("ECAC")
        ventana_selector.destroy()

    tk.Button(ventana_selector, text="Cargar", command=cargar_seleccion).pack(pady=10)



menubar = tk.Menu(ventana)

# Menú Archivo
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Cargar espacio aéreo", command=mostrar_selector_espacio_aereo)
file_menu.add_command(label="Mostrar Graph 1", command=lambda: show_graph("graph.txt"))
file_menu.add_command(label="Reiniciar Graph 1", command=reiniciar_y_mostrar_grafo1)
file_menu.add_command(label="Cargar grafo", command=select_file)
file_menu.add_command(label="Cargar grafo en Google Earth", command=Google_Earth)
file_menu.add_command(label="Guardar grafo actual", command=guardar_grafo_en_archivo)
menubar.add_cascade(label="Archivo", menu=file_menu)

# Menú Crear
create_menu = tk.Menu(menubar, tearoff=0)
create_menu.add_command(label="Crear nodo", command=open_create_node_window)
create_menu.add_command(label="Crear segmento", command=open_create_segment_window)
create_menu.add_command(label="Crear nuevo grafo", command=crear_grafo_vacio)
menubar.add_cascade(label="Crear", menu=create_menu)

# Menú Filtros
filter_menu = tk.Menu(menubar, tearoff=0)
filter_menu.add_command(label="Filtrar por distancia", command=open_filter_window)
menubar.add_cascade(label="Filtros", menu=filter_menu)

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
tk.Button(sidebar, text="Mostrar en Google Earth", command=mostrar_grafo_en_google_earth, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Buscar nodos vecinos", command=get_neighbors, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Vecinos en Google Earth", command=exportar_vecinos_kml, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Alcance", command=show_reachability, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Alcance en Google Earth", command=exportar_reachability_kml, **boton_style).pack(pady=5)
tk.Label(sidebar, text="Nodo 1:", bg="#1f2f3f", fg="white").pack(pady=(15, 5), padx=10, anchor="w")
entry2 = tk.Entry(sidebar, width=25)
entry2.pack(pady=5, padx=10)
tk.Label(sidebar, text="Nodo 2:", bg="#1f2f3f", fg="white").pack(pady=(15, 5), padx=10, anchor="w")
entry3 = tk.Entry(sidebar, width=25)
entry3.pack(pady=5, padx=10)
tk.Button(sidebar, text="Camino más corto", command=show_shortest_path, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Shortest en Google Earth", command=export_shortest_path_kml, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Eliminar nodo", command=get_input_delete, **boton_style).pack(pady=5)
tk.Label(sidebar, text="Nombre del Segmento a eliminar:", bg="#1f2f3f", fg="white").pack(pady=(15, 5), padx=10, anchor="w")
entry4 = tk.Entry(sidebar, width=25)
entry4.pack(pady=3.5, padx=10)
tk.Button(sidebar, text="Eliminar Segmento", command=get_input_delete_s, **boton_style).pack(pady=5)
ventana.mainloop()