
import tkinter as tk
import os
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from random import random
from gui.helper_functions.loadgraph import load_graph
from classes.graph import Graph
from classes.vertex import Vertex

# plot function is created for 
# plotting the graph in 
# tkinter window

class App:
    def __init__(self):
        self.selected_vertex = None
        self.previous_selected = None

        files = [f for f in os.listdir("graphs/") if os.path.isfile(os.path.join("graphs/", f))]

        i = 1
        while f"new_graph ({i}).json" in files:
            i += 1

        self.window = tk.Tk()
        self.graph = Graph(f"new_graph ({i}).json")  # start with empty graph
        # setting the title 
        self.window.title('Plotting in Tkinter')

        # dimensions of the main window
        self.window.geometry("500x500")

        # buttons to manipulate the graphs
        btn_bar = tk.Frame(self.window)
        btn_bar.pack(fill="x", padx=10, pady=10)

        plot_button = tk.Button(btn_bar, 
                            command = self.plot,
                            height = 2, 
                            width = 10,
                            text = "Plot")

        delete_button = tk.Button(btn_bar, 
                            command = self.delete_vertex,
                            height = 2, 
                            width = 10,
                            text = "Delete vertex")

        add_edge_button = tk.Button(btn_bar, 
                            command = self.add_edge,
                            height = 2, 
                            width = 10,
                            text = "Add edge")

        add_vertex_button = tk.Button(btn_bar, 
                            command = self.add_vertex,
                            height = 2, 
                            width = 10,
                            text = "Add vertex")

        save_button = tk.Button(btn_bar, 
                                    command = self.save_graph,
                                    height = 2, 
                                    width = 10,
                                    text = "Save graph")


        # put them next to each other
        plot_button.grid(row=0, column=0, padx=5)
        add_vertex_button.grid(row=0, column=1, padx=5)
        delete_button.grid(row=0, column=2, padx=5)
        add_edge_button.grid(row=0, column=3, padx=5)
        save_button.grid(row=0, column=4, padx=5)

        for c in range(5):
            btn_bar.grid_columnconfigure(c, weight=1)


        def select(event):
            selected_item = combo_box.get()
            label.config(text="Selected Item: " + selected_item)
            self.graph = load_graph(selected_item)

        # Create a label
        label = tk.Label(self.window, text="Selected Item: ")
        label.pack(pady=10)

        # Create a Combobox widget
        combo_box = ttk.Combobox(self.window,
                                 values=files,
                                 state='readonly')
        combo_box.pack(pady=5)

        # Set default value
        combo_box.set("Select a graph")

        # Bind event to selection
        combo_box.bind("<<ComboboxSelected>>", select)

        self.fig = Figure(figsize = (5, 5),
                    dpi = 100)
        self.plot1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig,
                                master = self.window)  


        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas,
                                    self.window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()

    def add_vertex(self):
        id = 1
        while id in self.graph.ids:
            id += 1 
        new_vertex = Vertex(self.graph, (random(),random()), id)
        self.graph.add_vertex(new_vertex)
        self.plot()

    def add_edge(self):
        if self.previous_selected is None:
            return
        self.selected_vertex.add_neighbour(self.previous_selected)
        self.plot()

    def delete_vertex(self):
        if self.selected_vertex is None:
            return
        self.graph.delete_vertex(self.selected_vertex)
        self.selected_vertex = None
        self.previous_selected = None
        self.plot()

    def save_graph(self):
        self.graph.save()

    def plot(self):
    
        # the figure that will contain the plot
        
        self.plot1.clear()
        def onclick(event):

            if event.artist is not sc:
                return
            ind = event.ind  # indices of picked points (can be multiple)
            i = ind[0]

            self.previous_selected = self.selected_vertex

            self.selected_vertex = vertices[i]
            

            fc = [(0,0,1,1) for _ in range(len(vertices))]
            fc[i] = (1, 0, 0, 1)

            sc.set_facecolors(fc)
            self.fig.canvas.draw_idle()


        

        # fig.canvas.mpl_disconnect(cid)

        # adding the subplot
        

        vertices = [v for v in self.graph.vertices]
        if vertices:
            x, y = zip(*(v.location for v in vertices))

            sc = self.plot1.scatter(x, y, s=60, picker = True, c='b')
            cid = self.fig.canvas.mpl_connect('pick_event', onclick)

            for edge in self.graph.edges:
                x1, y1 = edge[0].location
                x2, y2 = edge[1].location
                
                self.plot1.plot([x1, x2], [y1, y2])
                

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        
        self.canvas.draw()

    def run(self):
        # run the gui
        self.window.mainloop()
