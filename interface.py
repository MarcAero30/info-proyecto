import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

#Graficos es el archivo donde estan los graficos
#mostrar_grafico son las funciones del otro archivo
from graph import (
    Plot,
    LoadGraph
)
# Crear ventana principal
ventana = tk.Tk()
ventana.title("Ventana de Tkinter")
ventana.geometry("400x300")  # Ancho x Alto
ventana.configure(bg="#339fff")
g = None

def select_file():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog
    file_path = filedialog.askopenfilename()

    # Print the selected file path
    if file_path:
        print(f"Selected file: {os.path.basename(file_path)}")
        Plot(LoadGraph(os.path.basename(file_path)), ventana)
    else:
        print("No file selected")

def get_input_closest():
    user_input = entry.get()  # Retrieve the input text from the Entry widget
    x, y = busca_encuentra(user_input)
    print(x, ", ", y)
    print(f"User input: {user_input}")

def get_input_delete():
    user_input = entry.get()
    print(f"User input: {user_input}")

def show_graph(g_name):
    g = LoadGraph(g_name)
    Plot(g, ventana)

#Colores de los botones
color_boton_1 = "#b04c0b"
color_boton_2 = "#b04c0b"
color_boton_3 = "#b04c0b"
color_boton_4 = "#b04c0b"


# Crear botones
label = tk.Label(ventana, text="Selected Node: ")

boton1 = tk.Button(ventana, text="Mostrar Graph 1",command=lambda: show_graph("graph"),width=20,
                   bg=color_boton_1, fg="white")
boton2 = tk.Button(ventana, text="Mostrar Graph 2",command= lambda: show_graph("graph2"),width=20,
                   bg=color_boton_2, fg="white")
boton3 = tk.Button(ventana, text="Abrir archivo",command=lambda: select_file(),width=20,
                   bg=color_boton_3, fg="white")
entry = tk.Entry(ventana, width=30)
button = tk.Button(ventana, text="Buscar más cercano", command=get_input_closest)
entry = tk.Entry(ventana, width=30)
button = tk.Button(ventana, text="Eliminar segmento", command=get_input_delete)



# Ubicar botones en la ventana
label.grid(row=1, column=1, padx=40, pady=10)
boton1.grid(row=1, column=3, padx=40, pady=10)
boton2.grid(row=2, column=3, padx=40, pady=10)
boton3.grid(row=3, column=3, padx=10, pady=10)
entry.grid(row=4, column=3, padx=40, pady=10)
button.grid(row=5, column=3, padx=40, pady=10)

# Iniciar el bucle principal
ventana.mainloop()
