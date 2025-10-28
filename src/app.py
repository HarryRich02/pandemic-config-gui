import tkinter as tk
import tknodesystem as tkns


class application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.pane = tk.PanedWindow(self, orient="horizontal", sashrelief="raised")
        self.pane.pack(fill="both", expand=True)

        leftFrame = tk.Frame(self.pane, bg="#f0f0f0")
        label = tk.Label(leftFrame, text="Settings")
        label.pack(pady=20)

        self.textBox = tk.Text(leftFrame, wrap="word")
        self.textBox.pack(padx=10, pady=10, fill="both", expand=True)

        rightFrame = tk.Frame(self.pane, bg="#d9d9d9")
        self.canvas = tkns.NodeCanvas(rightFrame)
        self.canvas.pack(fill="both", expand=True)

        self.pane.add(leftFrame, minsize=250)
        self.pane.add(rightFrame)

        menu = tkns.NodeMenu(self.canvas)
        menu.add_node(label="NodeValue", command=lambda: tkns.NodeValue(self.canvas))
        menu.add_node(
            label="NodeOperation", command=lambda: tkns.NodeOperation(self.canvas)
        )
        menu.add_node(
            label="NodeCompile", command=lambda: tkns.NodeCompile(self.canvas)
        )

        self.after(
            100, lambda: self.pane.sash_place(0, self.master.winfo_width() // 2, 0)
        )


def run_app():
    root = tk.Tk()
    root.title("Pandemic Config GUI")
    root.geometry("1920x1080")

    app = application(master=root)
    app.mainloop()
