import tkinter as tk
from tkinter import messagebox, filedialog
import os

from graph import (
    Plot,
    LoadGraph,
    PlotNode,
    DeleteNode,
    FindCoordinates
)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Graph Viewer")
ventana.geometry('1500x800')
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
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {os.path.basename(file_path)}")
        Plot(LoadGraph(os.path.basename(file_path)), main_area, label, x_interface, y_interface)
    else:
        print("No file selected")

def get_neighbors():
    PlotNode(g, label.cget("text").split(": ")[1])

def get_input_delete():
    global g
    DeleteNode(g, label.cget("text").split(": ")[1])
    show_graph("graph")

def show_graph(g_name):
    global g
    g = LoadGraph(g_name)
    Plot(g, main_area, label, x_interface, y_interface)

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

tk.Button(sidebar, text="Mostrar Graph 1", command=lambda: show_graph("graph"), **boton_style).pack(pady=5)
tk.Button(sidebar, text="Mostrar Graph 2", command=lambda: show_graph("graph2"), **boton_style).pack(pady=5)
tk.Button(sidebar, text="Abrir archivo", command=select_file, **boton_style).pack(pady=5)

# Entrada de texto
tk.Label(sidebar, text="Nombre del nodo:", bg="#1f2f3f", fg="white").pack(pady=(15, 5), padx=10, anchor="w")
entry = tk.Entry(sidebar, width=25)
entry.pack(pady=5, padx=10)

tk.Button(sidebar, text="Buscar nodos vecinos", command=get_neighbors, **boton_style).pack(pady=5)
tk.Button(sidebar, text="Eliminar nodo", command=get_input_delete, **boton_style).pack(pady=5)

# Loop
ventana.mainloop()
