import tkinter as tk
from tkinter import ttk

from database import init_db
from tab_view import add_tab
from tabs import TABS


class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Treniņu un uztura pārvaldība")
        self.root.geometry("900x650")
        init_db()

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        for tab in TABS:
            add_tab(notebook, **tab)
