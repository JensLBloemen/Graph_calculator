from gui.gui import App
from gui.helper_functions.loadgraph import load_graph
from libs.operation import operation
from random import randint

W = load_graph("Vampire0.json")
for _ in range(3):
    V = load_graph(f"Vampire{randint(0,5)}.json")
    W = operation(V, W)
W.name = "out"
W.save()


if __name__ == "__main__":
    app = App()
    app.run()