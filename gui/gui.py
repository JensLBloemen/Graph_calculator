import tkinter as tk
import os
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from random import random
from gui.helper_functions.loadgraph import load_graph
from classes.graph import Graph
from classes.vertex import Vertex

from libs.chromaticpol import get_chromatic_polynomial, get_all_chromatic_polynomials
import threading
import queue
import tkinter.messagebox as mb


class App:
    def __init__(self):
        self.selected_vertex = None
        self.previous_selected = None

        # --- dragging state ---
        self._dragging = False
        self._drag_vertex = None
        self._drag_index = None
        self._pick_tol_px = 10  # grab radius in pixels

        # --- view freezing / padding ---
        self._frozen_xlim = None
        self._frozen_ylim = None
        self._pad_frac = 0.15   # 15% padding around the graph
        self._min_span = 0.25   # minimum width/height so view isn't cramped

        files = [f for f in os.listdir("graphs/") if os.path.isfile(os.path.join("graphs/", f))]

        i = 1
        while f"new_graph ({i}).json" in files:
            i += 1

        self.window = tk.Tk()
        self.graph = Graph(f"new_graph ({i}).json")  # start with empty graph
        self.window.title('Plotting in Tkinter')
        self.window.geometry("500x500")

        # buttons to manipulate the graphs
        btn_bar = tk.Frame(self.window)
        btn_bar.pack(fill="x", padx=10, pady=10)

        self.status = tk.Label(self.window, text="Ready")
        self.status.pack(pady=5)

        self.pb = ttk.Progressbar(self.window, mode="indeterminate")
        self.pb.pack(fill="x", padx=10, pady=5)

        plot_button = tk.Button(btn_bar, command=self.plot, height=2, width=10, text="Plot")
        delete_button = tk.Button(btn_bar, command=self.delete_vertex, height=2, width=10, text="Delete vertex")
        add_edge_button = tk.Button(btn_bar, command=self.add_edge, height=2, width=10, text="Add edge")
        add_vertex_button = tk.Button(btn_bar, command=self.add_vertex, height=2, width=10, text="Add vertex")
        save_button = tk.Button(btn_bar, command=self.save_graph, height=2, width=10, text="Save graph")
        del_edge_button = tk.Button(btn_bar, command=self.delete_edge, height=2, width=10, text="delete edge")
        contract_edge_button = tk.Button(btn_bar, command=self.contract_edge, height=2, width=10, text="contract edge")

        self.chrom_pol_button = tk.Button(
            btn_bar,
            command=self.chrom_pol,
            height=2,
            width=18,
            text="chromatic polynomial"
        )

        plot_button.grid(row=0, column=0, padx=5)
        add_vertex_button.grid(row=0, column=1, padx=5)
        delete_button.grid(row=0, column=2, padx=5)
        add_edge_button.grid(row=0, column=3, padx=5)
        save_button.grid(row=0, column=4, padx=5)
        del_edge_button.grid(row=0, column=5, padx=5)
        contract_edge_button.grid(row=0, column=6, padx=5)
        self.chrom_pol_button.grid(row=0, column=7, padx=5)

        for c in range(8):
            btn_bar.grid_columnconfigure(c, weight=1)

        def select(event):
            selected_item = combo_box.get()
            label.config(text="Selected Item: " + selected_item)
            self.graph = load_graph(selected_item)
            self.selected_vertex = None
            self.previous_selected = None
            self.plot()

        label = tk.Label(self.window, text="Selected Item: ")
        label.pack(pady=10)

        combo_box = ttk.Combobox(self.window, values=files, state='readonly')
        combo_box.pack(pady=5)
        combo_box.set("Select a graph")
        combo_box.bind("<<ComboboxSelected>>", select)

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.plot1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        toolbar.update()
        self.canvas.get_tk_widget().pack()

        # --- connect mouse events once (drag/select) ---
        self.fig.canvas.mpl_connect("button_press_event", self._on_press)
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_motion)
        self.fig.canvas.mpl_connect("button_release_event", self._on_release)

    # ---------------- Graph editing ----------------

    def add_vertex(self):
        vid = 1
        while vid in self.graph.ids:
            vid += 1
        new_vertex = Vertex(self.graph, (random(), random()), vid)
        self.graph.add_vertex(new_vertex)
        self.plot()

    def add_edge(self):
        if self.previous_selected is None or self.selected_vertex is None:
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

    def delete_edge(self):
        if self.previous_selected is None or self.selected_vertex is None:
            return
        self.graph.delete_edge((self.previous_selected, self.selected_vertex))
        self.plot()

    def contract_edge(self):
        if self.previous_selected is None or self.selected_vertex is None:
            return
        self.graph.contract_edge((self.previous_selected, self.selected_vertex))
        self.plot()

    def save_graph(self):
        self.selected_vertex = self.previous_selected = None
        self.plot()
        self.graph.save()
        self.fig.savefig(f"pics/{self.graph.name}", dpi = 300)

    # ---------------- Chromatic polynomial (kept from your code) ----------------

    def chrom_pol(self):
        m = len(self.graph.edges)
        if m > 30:
            mb.showwarning(
                "May be slow",
                f"This graph has {m} edges.\n"
                f"Deletion–contraction may explore up to ~2^{m} branches.\n"
                f"Progress will be shown; you can still use the UI."
            )

        self.chrom_pol_button.config(state="disabled")
        self.status.config(text="Computing chromatic polynomial...")
        self.pb.start(10)

        q = queue.Queue()

        def progress_cb(iters, stack_size):
            q.put(("progress", iters, stack_size))

        def worker():
            try:
                # poly = get_chromatic_polynomial(self.graph, progress_cb=progress_cb)


                polys = get_all_chromatic_polynomials(self.graph, progress_cb=progress_cb)
                # print(str(sum(polys)), str(get_chromatic_polynomial(self.graph)))
                # assert sum(polys) == poly
                # out = 'sut      polynomial\n'
                # for pol in polys:
                #     out += "111     " + str(pol)+"\n"

                rows = list(zip(["111", "112", "121", "122", "123"], polys))
                sut_w = 3
                pol_w = max(len(str(p)) for _, p in rows)

                out = "sut".ljust(sut_w) + "  " + "polynomial\n"
                out += "-" * (sut_w + 2 + max(pol_w, len("polynomial"))) + "\n"
                for sut, pol in rows:
                    out += f"{sut:>{sut_w}}  {str(pol):>{pol_w}}\n"

                q.put(("done", out))

                q.put(("done", out))

            except Exception as e:
                q.put(("error", str(e)))

        threading.Thread(target=worker, daemon=True).start()

        def poll():
            try:
                while True:
                    msg = q.get_nowait()
                    if msg[0] == "progress":
                        _, iters, stack_size = msg
                        self.status.config(text=f"Visited nodes: {iters:,} | Stack: {stack_size:,}")
                    elif msg[0] == "done":
                        _, poly = msg
                        self.pb.stop()
                        self.chrom_pol_button.config(state="normal")
                        self.status.config(text=f"Done: {poly}")
                        print(poly)
                        return
                    elif msg[0] == "error":
                        _, err = msg
                        self.pb.stop()
                        self.chrom_pol_button.config(state="normal")
                        self.status.config(text="Error")
                        mb.showerror("Chromatic polynomial error", err)
                        return
            except queue.Empty:
                pass

            self.window.after(50, poll)

        poll()

    # ---------------- Dragging/select helpers ----------------

    def _hit_test_vertex(self, event):
        """
        Return (vertex, index) if mouse is within tolerance of a vertex.
        Uses pixel distance so it works under zoom/pan.
        IMPORTANT: uses ALL vertices, including isolated ones.
        """
        if event.inaxes != self.plot1:
            return None, None

        vertices = list(self.graph.vertices)
        if not vertices:
            return None, None

        trans = self.plot1.transData
        v_pix = [trans.transform((v.location[0], v.location[1])) for v in vertices]

        mx, my = event.x, event.y
        best_i = None
        best_d2 = None

        for i, (px, py) in enumerate(v_pix):
            dx = px - mx
            dy = py - my
            d2 = dx * dx + dy * dy
            if best_d2 is None or d2 < best_d2:
                best_d2 = d2
                best_i = i

        if best_d2 is None:
            return None, None

        if best_d2 <= (self._pick_tol_px * self._pick_tol_px):
            return vertices[best_i], best_i

        return None, None

    def _on_press(self, event):
        if event.button != 1:
            return

        v, i = self._hit_test_vertex(event)
        if v is None:
            return

        self._dragging = True
        self._drag_vertex = v
        self._drag_index = i

        # freeze current view limits so nothing "jumps" while dragging
        self._frozen_xlim = self.plot1.get_xlim()
        self._frozen_ylim = self.plot1.get_ylim()

        self.previous_selected = self.selected_vertex
        self.selected_vertex = v

        self.plot(preserve_limits=True)

    def _on_motion(self, event):
        if not self._dragging:
            return
        if event.inaxes != self.plot1:
            return
        if event.xdata is None or event.ydata is None:
            return

        self._drag_vertex.location = (float(event.xdata), float(event.ydata))
        self.plot(preserve_limits=True)

    def _on_release(self, event):
        if event.button != 1:
            return

        self._dragging = False
        self._drag_vertex = None
        self._drag_index = None

        # allow recompute view after letting go
        self._frozen_xlim = None
        self._frozen_ylim = None

        self.plot(preserve_limits=False)

    # ---------------- Padded view helpers ----------------
    def _padded_limits(self, vertices):
        xs = [v.location[0] for v in vertices]
        ys = [v.location[1] for v in vertices]

        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        dx = max(xmax - xmin, 1e-9)
        dy = max(ymax - ymin, 1e-9)

        # ensure a minimum span so the plot isn’t cramped when vertices are close
        dx = max(dx, self._min_span)
        dy = max(dy, self._min_span)

        padx = dx * self._pad_frac
        pady = dy * self._pad_frac

        cx = 0.5 * (xmin + xmax)
        cy = 0.5 * (ymin + ymax)

        xlim = (cx - 0.5 * dx - padx, cx + 0.5 * dx + padx)
        ylim = (cy - 0.5 * dy - pady, cy + 0.5 * dy + pady)
        return xlim, ylim

    def _apply_padded_view(self):
        # IMPORTANT: use ALL vertices, including isolated ones
        vertices = list(self.graph.vertices)
        if not vertices:
            return
        xlim, ylim = self._padded_limits(vertices)
        self.plot1.set_xlim(xlim)
        self.plot1.set_ylim(ylim)

    # ---------------- Plot ----------------

    def plot(self, preserve_limits=False):
        frozen = preserve_limits and self._frozen_xlim is not None and self._frozen_ylim is not None
        if frozen:
            xlim, ylim = self._frozen_xlim, self._frozen_ylim
        else:
            xlim = ylim = None

        self.plot1.clear()
        self.plot1.set_title(self.graph.name)
        self.plot1.set_aspect("equal", adjustable="box")
        self.plot1.axis("off")

        vertices = list(self.graph.vertices)
        if vertices:
            x, y = zip(*(v.location for v in vertices))
            sc = self.plot1.scatter(x, y, s=6, c='b')

            # highlight selected vertex in red
            if self.selected_vertex in vertices:
                i = vertices.index(self.selected_vertex)
                fc = [(0, 0, 1, 1) for _ in range(len(vertices))]
                fc[i] = (1, 0, 0, 1)
                sc.set_facecolors(fc)

            for v in vertices:
                x0, y0 = v.location
                if v.id in {'s', 't', 'u'}:
                    self.plot1.annotate(
                        str(v.id),
                        (x0, y0),
                        textcoords="offset points",
                        xytext=(6, 6),
                        fontsize=10
                )

            for edge in self.graph.edges:
                u, v = tuple(edge)
                x1, y1 = u.location
                x2, y2 = v.location

                if v == self.selected_vertex:
                    u, v = v, u

                if edge == frozenset({self.previous_selected, self.selected_vertex}):
                    self.plot1.plot([x1, x2], [y1, y2], c='r')
                elif u == self.selected_vertex:
                    if v in u.neighbours:
                        self.plot1.plot([x1, x2], [y1, y2], c='g')

                
                else:
                    self.plot1.plot([x1, x2], [y1, y2], c='0')

        if frozen and xlim is not None and ylim is not None:
            self.plot1.set_xlim(xlim)
            self.plot1.set_ylim(ylim)
        else:
            self._apply_padded_view()

        self.canvas.draw()

    def run(self):
        self.window.mainloop()
