
from tkinter import * 
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


    # adding the subplot
    plot1 = fig.add_subplot(111)


    for vertex in graph.vertices:
        x, y = vertex.location
    # plotting the graph
        plot1.scatter(x, y)
    
    for edge in graph.edges:
        print(edge)
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
        self.window = Tk()

        # setting the title 
        self.window.title('Plotting in Tkinter')
        pass





        # dimensions of the main window
        self.window.geometry("500x500")

        # button that displays the plot
        plot_button = Button(master = self.window, 
                            command = lambda: plot(self.window, graph),
                            height = 2, 
                            width = 10,
                            text = "Plot")

        # place the button 
        # in main window
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