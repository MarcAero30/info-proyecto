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

def select_file():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog
    file_path = filedialog.askopenfilename()

    # Print the selected file path
    if file_path:
        print(f"Selected file: {os.path.basename(file_path)}")
        Plot(LoadGraph(os.path.basename(file_path)))
    else:
        print("No file selected")

#Colores de los botones
color_boton_1 = "#b04c0b"
color_boton_2 = "#b04c0b"
color_boton_3 = "#b04c0b"
color_boton_4 = "#b04c0b"


# Crear botones
boton1 = tk.Button(ventana, text="Mostrar Graph 1",command=lambda: Plot(LoadGraph("graph")),width=20,
                   bg=color_boton_1, fg="white")
boton2 = tk.Button(ventana, text="Mostrar Graph 2",command= lambda: Plot(LoadGraph("graph2")),width=20,
                   bg=color_boton_2, fg="white")
boton3 = tk.Button(ventana, text="Abrir archivo",command=lambda: select_file(),width=20,
                   bg=color_boton_3, fg="white")
# boton4 = tk.Button(ventana, text="Botón 4",command= mostrar_grafico_node, width=20,
#                    bg=color_boton_4, fg="white")

# Ubicar botones en la ventana
boton1.grid(row=1, column=3, padx=40, pady=10)
boton2.grid(row=1, column=5, padx=40, pady=10)
boton3.grid(row=3, column=3, padx=10, pady=10)
# boton4.grid(row=3, column=5, padx=10, pady=10)

# Iniciar el bucle principal
ventana.mainloop()
