# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
from face.face_capture import FaceCapture
from face.face_recognizer import FaceRecognizer

class RegisterUI:
    def __init__(self, master, db):
        self.db = db
        self.face_encoding = None

        self.win = tk.Toplevel(master)
        self.win.title("Register Person")
        self.win.geometry("320x300")
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
            text="Capture Face (Press C)",
            width=20,
            command=self.capture_face
        ).pack(pady=(15, 0))

        tk.Button(
            self.win,
            text="Select Face Image",
            width=20,
            command=self.select_face_image
        ).pack(pady=(6, 0))

        tk.Button(
            self.win,
            text="Save",
            width=15,
            command=self.save_person
        ).pack(pady=20)

    def capture_face(self):
        try:
            capturer = FaceCapture()
            recognizer = FaceRecognizer()
            if capturer.detector is None:
                messagebox.showwarning(
                    "Warning",
                    "Face detector model not found. Using full image for encoding."
                )
            face_img = capturer.capture_face()
            self.face_encoding = recognizer.extract_encoding(face_img)
            messagebox.showinfo("Success", "Face captured successfully.")
        except Exception as exc:
            messagebox.showerror("Capture Error", str(exc))

    def select_face_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not file_path:
            return
        try:
            capturer = FaceCapture()
            recognizer = FaceRecognizer()
            if capturer.detector is None:
                messagebox.showwarning(
                    "Warning",
                    "Face detector model not found. Using full image for encoding."
                )
            face_img = capturer.capture_from_file(file_path)
            self.face_encoding = recognizer.extract_encoding(face_img)
            messagebox.showinfo("Success", "Face image loaded successfully.")
        except Exception as exc:
            messagebox.showerror("Image Error", str(exc))

    def save_person(self):
        name = self.entry_name.get().strip()
        job_id = self.entry_job.get().strip()
        dept = self.entry_dept.get().strip()

        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        if self.face_encoding is None:
            messagebox.showerror("Error", "Please capture face data first.")
            return

        person_id = self.db.add_person(name, job_id, dept)
        self.db.add_face_encoding(person_id, self.face_encoding)
        messagebox.showinfo("Success", f"Register success (ID = {person_id})")
        self.win.destroy()
    
