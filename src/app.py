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
        label = tk.Label(
            leftFrame, text="Settings", font=("Segoe UI", 14), bg="#f0f0f0"
        )
        label.pack(pady=(20, 10))

        self.disease_settings(leftFrame)
        saveButton = tk.Button(
            leftFrame, text="Save Configuration", command=self.on_run
        )
        saveButton.pack(pady=10)

        rightFrame = tk.Frame(self.pane, bg="#d9d9d9")
        self.canvas = tkns.NodeCanvas(rightFrame)
        self.canvas.pack(fill="both", expand=True)

        self.pane.add(leftFrame, minsize=250)
        self.pane.add(rightFrame)

        menu = tkns.NodeMenu(self.canvas)
        menu.add_node(label="Start State", command=lambda: tkns.NodeValue(self.canvas))
        menu.add_node(
            label="Transition State",
            command=lambda: tkns.NodeOperation(
                self.canvas, inputs=1, multiple_connection=True
            ),
        )
        menu.add_node(
            label="End State",
            command=lambda: tkns.NodeCompile(self.canvas, multiple_connection=True),
        )

        self.after(
            100, lambda: self.pane.sash_place(0, self.master.winfo_width() // 3, 0)
        )

    def disease_settings(self, frame):
        nameLabel = tk.Label(frame, text="Name:", bg="#f0f0f0")
        nameLabel.pack(anchor="w", padx=10)
        self.nameEntry = tk.Entry(frame)
        self.nameEntry.pack(fill="x", padx=10, pady=(0, 10))

        dlsLabel = tk.Label(frame, text="Default Lowest Stage:", bg="#f0f0f0")
        dlsLabel.pack(anchor="w", padx=10)
        dlsOptions = [
            "recovered",
            "healthy",
            "exposed",
            "asymptomatic",
            "mild",
            "severe",
            "hospitalised",
            "intensive_care",
            "dead_home",
            "dead_hospital",
            "dead_icu",
        ]
        self.dlsVar = tk.StringVar(value=dlsOptions[0])
        dlsMenu = tk.OptionMenu(frame, self.dlsVar, *dlsOptions)
        dlsMenu.pack(fill="x", padx=10, pady=(0, 10))

        mmstLabel = tk.Label(frame, text="Max Mild Symptom Tag:", bg="#f0f0f0")
        mmstLabel.pack(anchor="w", padx=10)
        mmstOptions = [
            "recovered",
            "healthy",
            "exposed",
            "asymptomatic",
            "mild",
            "severe",
            "hospitalised",
            "intensive_care",
            "dead_home",
            "dead_hospital",
            "dead_icu",
        ]
        self.mmstVar = tk.StringVar(value=mmstOptions[0])
        mmstMenu = tk.OptionMenu(frame, self.mmstVar, *mmstOptions)
        mmstMenu.pack(fill="x", padx=10, pady=(0, 10))

    def on_run(self):
        name = self.nameEntry.get()
        dls = self.dlsVar.get()
        mmst = self.mmstVar.get()

        print(f"Name: {name}")
        print(f"Default Lowest Stage: {dls}")
        print(f"Max Mild Symptom Tag: {mmst}")


def run_app():
    root = tk.Tk()
    root.title("Pandemic Config GUI")
    root.geometry("1920x1080")

    app = application(master=root)
    app.mainloop()
