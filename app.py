import tkinter as tk
from tkinter import messagebox, ttk
from database import init_db, run_query, get_data

class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Datubāzes Sistēma")
        self.root.geometry("600x520")
        init_db()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Cilu konfigurācija ar visiem laukiem
        self.add_tab("Lietotāji", "users", 
                     ["Vārds", "E-pasts", "Parole"], 
                     ["username", "email", "password_hash"], [0, 1, 1])
        
        self.add_tab("Vingrinājumi", "exercises", 
                     ["Nosaukums", "Apraksts", "Muskuļu grupa"], 
                     ["name", "description", "muscle_group"], [0, 0, 0])
        
        self.add_tab("Treniņi", "workouts", 
                     ["Lietotājs ID", "Treniņa nosaukums", "Piezīmes"], 
                     ["user_id", "session_name", "notes"], [0, 0, 0])
        
        self.add_tab("Piegājieni", "workout_sets", 
                     ["Treniņa ID", "Vingrinājuma ID", "Piegājiena Nr", "Svars (kg)", "Atkārtojumi"], 
                     ["workout_id", "exercise_id", "set_number", "weight_kg", "reps"], [0, 0, 0, 0, 0])
        
        self.add_tab("Rekordi", "personal_records", 
                     ["Lietotājs ID", "Vingrinājuma ID", "Svars (kg)", "Atkārtojumi"], 
                     ["user_id", "exercise_id", "weight_kg", "reps"], [0, 0, 0, 0])
        
        self.add_tab("Uzturs", "meal_logs", 
                     ["Lietotājs ID", "Ēdienreize", "Kalorijas", "Olbaltumvielas (g)", "Ogļhidrāti (g)", "Tauki (g)"], 
                     ["user_id", "meal_name", "calories", "protein_g", "carbs_g", "fats_g"], [0, 0, 0, 0, 0, 0])
        
        self.add_tab("Profili", "user_profiles", 
                     ["Lietotājs ID", "Augums (cm)", "Mērķa svars (kg)", "Mērķi"], 
                     ["user_id", "height_cm", "target_weight_kg", "fitness_goals"], [0, 0, 0, 0])
        
        self.add_tab("Mērījumi", "body_measurements", 
                     ["Lietotājs ID", "Svars (kg)", "Tauku %", "Viduklis (cm)"], 
                     ["user_id", "weight_kg", "body_fat_pct", "waist_cm"], [0, 0, 0, 0])

    def add_tab(self, title, table, labels, fields, is_password):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)

        f = tk.Frame(tab)
        f.pack(pady=5)
        
        entries = {}
        for i, (label, field, pwd) in enumerate(zip(labels, fields, is_password)):
            tk.Label(f, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            e = tk.Entry(f, width=25, show="*" if pwd else "")
            e.grid(row=i, column=1, padx=5, pady=2)
            entries[field] = e

        output = tk.Text(tab, height=9, width=65)
        output.pack(pady=5)

        def save():
            vals = [e.get().strip() for e in entries.values()]
            if not vals[0]:
                messagebox.showerror("Kļūda", "Aizpildi obligātos laukus!")
                return
            try:
                placeholders = ", ".join(["?"] * len(vals))
                cols = ", ".join(fields)
                run_query(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", tuple(vals))
                messagebox.showinfo("Veiksme", "Dati saglabāti!")
                for e in entries.values(): e.delete(0, tk.END)
                load()
            except Exception as ex:
                messagebox.showerror("Kļūda", str(ex))

        def load():
            output.delete("1.0", tk.END)
            for row in get_data(f"SELECT * FROM {table}"):
                output.insert(tk.END, f"{row}\n")

        tk.Button(tab, text="Saglabāt", command=save, bg="#4CAF50", fg="white", width=15).pack(pady=2)
        tk.Button(tab, text="Atsvaidzināt", command=load, width=15).pack(pady=2)
        load()