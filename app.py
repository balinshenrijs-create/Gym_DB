import tkinter as tk
from tkinter import ttk
from database import init_db
from tab_view import add_tab
from tabs import TABS


class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Treniņu un uztura pārvaldība")
        self.root.geometry("950x700")
        self.root.minsize(800, 600)
        init_db()

        # Modern styling
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TNotebook.Tab", padding=[14, 8], font=("Segoe UI", 10, "bold"))

        # Main layout container
        container = ttk.Frame(root, padding=10)
        container.pack(fill="both", expand=True)

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)

        for tab in TABS:
            add_tab(notebook, **tab)

        # Status bar
        status = ttk.Label(root, text="Gatavs | Datubāze ielādēta", relief="sunken", anchor="w", padding=(10, 4))
        status.pack(side="bottom", fill="x")


if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()