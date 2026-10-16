import tkinter as tk
from database import init_db
from app import GymApp

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()