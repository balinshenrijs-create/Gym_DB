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
        values = [entry.get().strip() for entry in entries.values()]
        if not values[0]:
            messagebox.showerror("Trūkst datu", "Aizpildi pirmo obligāto lauku!")
            return
        try:
            placeholders = ", ".join("?" for _ in values)
            run_query(
                f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})",
                tuple(values),
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
