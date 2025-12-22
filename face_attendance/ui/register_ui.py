# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

class RegisterUI:
    def __init__(self, master, db):
        self.db = db

        self.win = tk.Toplevel(master)
        self.win.title("Register Person")
        self.win.geometry("320x240")
        self.win.resizable(False, False)

        tk.Label(self.win, text="Name").pack(pady=(15, 0))
        self.entry_name = tk.Entry(self.win, width=30)
        self.entry_name.pack()

        tk.Label(self.win, text="Job ID").pack(pady=(10, 0))
        self.entry_job = tk.Entry(self.win, width=30)
        self.entry_job.pack()

        tk.Label(self.win, text="Department").pack(pady=(10, 0))
        self.entry_dept = tk.Entry(self.win, width=30)
        self.entry_dept.pack()

        tk.Button(
            self.win,
            text="Save",
            width=15,
            command=self.save_person
        ).pack(pady=20)

    def save_person(self):
        name = self.entry_name.get().strip()
        job_id = self.entry_job.get().strip()
        dept = self.entry_dept.get().strip()

        if not name:
            messagebox.showerror("Error", "Name is required")
            return

        person_id = self.db.add_person(name, job_id, dept)
        messagebox.showinfo("Success", f"Register success (ID = {person_id})")
        self.win.destroy()
    