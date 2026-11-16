import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from database import get_data, run_query


def add_tab(notebook, title, table, labels, fields, passwords, query, columns):
    tab = ttk.Frame(notebook, padding=6)
    notebook.add(tab, text=title)

    ttk.Label(tab, text="Jauns ieraksts").pack(anchor="w")
    form = ttk.Frame(tab)
    form.pack(anchor="w", fill="x", pady=(4, 8))
    entries = {}
    for row, (label, field, password) in enumerate(zip(labels, fields, passwords)):
        ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=2)
        entry = ttk.Entry(form, width=28, show="*" if password else "")
        entry.grid(row=row, column=1, sticky="w", pady=2)
        entries[field] = entry

    frame = ttk.Frame(tab)
    frame.pack(fill="both", expand=True)
    column_ids = [column[0] for column in columns]
    records = ttk.Treeview(frame, columns=column_ids, show="headings", selectmode="browse")
    for column_id, heading, width in columns:
        records.heading(column_id, text=heading)
        records.column(column_id, width=width, minwidth=65, anchor="w")

    vertical = ttk.Scrollbar(frame, orient="vertical", command=records.yview)
    horizontal = ttk.Scrollbar(frame, orient="horizontal", command=records.xview)
    records.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    records.grid(row=0, column=0, sticky="nsew")
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal.grid(row=1, column=0, sticky="ew")
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    status = ttk.Label(tab)
    status.pack(anchor="w", pady=(4, 0))

    def load():
        records.delete(*records.get_children())
        rows = get_data(query)
        for row in rows:
            records.insert(
                "", tk.END, values=tuple("—" if value is None or value == "" else value for value in row)
            )
        status.config(text=f"Ierakstu skaits: {len(rows)}")

    def save():
        raw_values = [entry.get().strip() for entry in entries.values()]
        if not raw_values[0]:
            messagebox.showerror("Trūkst datu", "Aizpildi pirmo obligāto lauku!")
            return
        
        processed_values = []
        for field_name, val in zip(fields, raw_values):
            if not val:
                processed_values.append(None)  # Ja lauks ir tukšs, saglabājam NULL
                continue
                
            # Pārbaudām, vai laukam jābūt skaitliskam
            if any(k in field_name for k in ["weight", "reps", "calories", "protein", "carbs", "fats", "height", "pct", "cm", "seconds", "number", "id"]):
                try:
                    # Konvertējam uz float, ja ir decimāldaļa, vai int, ja vesels skaitlis
                    if "." in val or "," in val:
                        num_val = float(val.replace(",", "."))
                    else:
                        num_val = int(val)
                    
                    # Visaptverošas limitu un reālistisku mērījumu pārbaudes:
                    if "weight" in field_name or "target_weight" in field_name:
                        if num_val < 20 or num_val > 500:
                            messagebox.showerror("Nederīga vērtība", "Svaram jābūt reālistiskā diapazonā no 20 līdz 500 kg!")
                            return
                    
                    if "height" in field_name:
                        if num_val < 50 or num_val > 250:
                            messagebox.showerror("Nederīga vērtība", "Augumam jābūt robežās no 50 līdz 250 cm!")
                            return
                    
                    if "body_fat_pct" in field_name:
                        if num_val < 2 or num_val > 70:
                            messagebox.showerror("Nederīga vērtība", "Tauku procentam jābūt reālistiskam (no 2% līdz 70%)!")
                            return
                    
                    if any(c in field_name for c in ["chest_cm", "waist_cm", "hips_cm"]):
                        if num_val < 30 or num_val > 300:
                            messagebox.showerror("Nederīga vērtība", "Ķermeņa apkārtmēram jābūt robežās no 30 līdz 300 cm!")
                            return
                    
                    if "reps" in field_name:
                        if num_val < 1 or num_val > 1000:
                            messagebox.showerror("Nederīga vērtība", "Atkārtojumu skaitam jābūt vismaz 1!")
                            return
                    
                    if "set_number" in field_name:
                        if num_val < 1 or num_val > 100:
                            messagebox.showerror("Nederīga vērtība", "Piegājiena numuram jābūt no 1 līdz 100!")
                            return

                    if "calories" in field_name:
                        if num_val < 0 or num_val > 10000:
                            messagebox.showerror("Nederīga vērtība", "Kaloriju skaitam jābūt no 0 līdz 10000 kcal!")
                            return

                    if any(nutrient in field_name for nutrient in ["protein_g", "carbs_g", "fats_g"]):
                        if num_val < 0 or num_val > 2000:
                            messagebox.showerror("Nederīga vērtība", "Uzturvielu gramiem jābūt reālistiskās robežās (līdz 2000g)!")
                            return

                    if "rest_seconds" in field_name:
                        if num_val < 0 or num_val > 3600:
                            messagebox.showerror("Nederīga vērtība", "Atpūtas laikam jābūt no 0 līdz 3600 sekundēm!")
                            return

                    processed_values.append(num_val)
                except ValueError:
                    messagebox.showerror("Kļūda", f"Laukā '{field_name}' ir jāievada derīgs skaitlis!")
                    return
            else:
                processed_values.append(val)

        try:
            placeholders = ", ".join("?" for _ in processed_values)
            run_query(
                f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})",
                tuple(processed_values),
            )
            messagebox.showinfo("Saglabāts", "Ieraksts veiksmīgi saglabāts.")
            for entry in entries.values():
                entry.delete(0, tk.END)
            load()
        except sqlite3.Error as error:
            messagebox.showerror("Neizdevās saglabāt", str(error))

    buttons = ttk.Frame(tab)
    buttons.pack(anchor="w", pady=(6, 0))
    ttk.Button(buttons, text="Saglabāt", command=save).pack(side="left")
    ttk.Button(buttons, text="Atjaunot", command=load).pack(side="left", padx=(6, 0))
    load()
