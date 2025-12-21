
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

# plot function is created for 
# plotting the graph in 
# tkinter window




def plot(window, graph):

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
    
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
        fig.canvas.draw_idle()


    cid = fig.canvas.mpl_connect('pick_event', onclick)

    # fig.canvas.mpl_disconnect(cid)

    # adding the subplot
    plot1 = fig.add_subplot(111)

    vertices = [v for v in graph.vertices]
    print(vertices)
    print(*(v.location for v in vertices))
    x, y = zip(*(v.location for v in vertices))

    sc = plot1.scatter(x, y, s=60, picker = True)

    for edge in graph.edges:
        x1, y1 = edge[0].location
        x2, y2 = edge[1].location
        
        plot1.plot([x1, x2], [y1, y2])

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()



class App:
    def __init__(self, graph):
        self.window = tk.Tk()

        # setting the title 
        self.window.title('Plotting in Tkinter')

        # dimensions of the main window
        self.window.geometry("500x500")

        # button that displays the plot
        plot_button = tk.Button(master = self.window, 
                            command = lambda: plot(self.window, graph),
                            height = 2, 
                            width = 10,
                            text = "Plot")


        plot_button.pack()
        def select(event):
            selected_item = combo_box.get()
            label.config(text="Selected Item: " + selected_item)
        # Create a label
        label = tk.Label(self.window, text="Selected Item: ")
        label.pack(pady=10)

        # Create a Combobox widget
        combo_box = ttk.Combobox(self.window, values=["Option 1", "Option 2", "Option 3"], state='readonly')
        combo_box.pack(pady=5)

        # Set default value
        combo_box.set("Option 1")

        # Bind event to selection
        combo_box.bind("<<ComboboxSelected>>", select)

    def run(self):
        # run the gui
        self.window.mainloop()