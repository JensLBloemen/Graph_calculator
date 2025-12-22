
import tkinter as tk
import os
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from gui.helper_functions.loadgraph import load_graph
from classes.graph import Graph

# plot function is created for 
# plotting the graph in 
# tkinter window








class App:
    def __init__(self):
        self.window = tk.Tk()
        self.graph = Graph()  # start with empty graph
        # setting the title 
        self.window.title('Plotting in Tkinter')

        # dimensions of the main window
        self.window.geometry("500x500")

        # button that displays the plot
        plot_button = tk.Button(master = self.window, 
                            command = self.plot,
                            height = 2, 
                            width = 10,
                            text = "Plot")


        plot_button.pack()
        def select(event):
            selected_item = combo_box.get()
            label.config(text="Selected Item: " + selected_item)
            self.graph = load_graph(selected_item)

        # Create a label
        label = tk.Label(self.window, text="Selected Item: ")
        label.pack(pady=10)

        # Create a Combobox widget
        combo_box = ttk.Combobox(self.window,
                                 values=[f for f in os.listdir("graphs/") if os.path.isfile(os.path.join("graphs/", f))],
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

    def plot(self):
    
        # the figure that will contain the plot
        
        self.plot1.clear()
        def onclick(event):

            if event.artist is not sc:
                return
            ind = event.ind  # indices of picked points (can be multiple)
            i = ind[0]
            print(f"Picked index={i}, (x,y)=()")
            selected_vertex = vertices[i]

            fc = [(0,1,0,1) for _ in range(len(vertices))]
            fc[i] = (1, 0, 0, 1)

            sc.set_facecolors(fc)
            self.fig.canvas.draw_idle()


        cid = self.fig.canvas.mpl_connect('pick_event', onclick)

        # fig.canvas.mpl_disconnect(cid)

        # adding the subplot
        

        vertices = [v for v in self.graph.vertices]
        if vertices:
            x, y = zip(*(v.location for v in vertices))

            sc = self.plot1.scatter(x, y, s=60, picker = True)

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