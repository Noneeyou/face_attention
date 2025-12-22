# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from ui.register_ui import RegisterUI

class MainUI:
    def __init__(self, db):
        self.db = db

        self.root = tk.Tk()
        self.root.title("Face Attendance System")
        self.root.geometry("360x240")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="Face Attendance System",
            font=("Arial", 14, "bold")
        ).pack(pady=16)

        tk.Button(
            self.root,
            text="Register Person",
            width=20,
            command=self.open_register
        ).pack(pady=6)

        tk.Button(
            self.root,
            text="Face Check-in",
            width=20,
            command=lambda: None
        ).pack(pady=6)

        tk.Button(
            self.root,
            text="Attendance Report",
            width=20,
            command=lambda: None
        ).pack(pady=6)


        tk.Label(
            self.root,
            text="Step 1: Main UI & Database Init (Done)",
            fg="gray"
        ).pack(pady=12)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_register(self):
        RegisterUI(self.root, self.db)
        

    def on_close(self):
        self.db.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
