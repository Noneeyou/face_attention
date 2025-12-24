import tkinter as tk
from tkinter import filedialog, messagebox

from attendance.attendance_manager import AttendanceManager
from face.face_capture import FaceCapture
from face.face_recognizer import FaceRecognizer


class AttendanceUI:
    def __init__(self, master, db):
        self.db = db
        self.manager = AttendanceManager(db)
        self.recognizer = FaceRecognizer()
        self.match_threshold = 0.5

        self.win = tk.Toplevel(master)
        self.win.title("Face Check-in")
        self.win.geometry("340x240")
        self.win.resizable(False, False)

        tk.Label(
            self.win,
            text="Face Check-in",
            font=("Arial", 12, "bold")
        ).pack(pady=12)

        tk.Label(
            self.win,
            text="Press C to capture face, Q to quit camera."
        ).pack(pady=6)

        tk.Button(
            self.win,
            text="Capture & Check-in",
            width=20,
            command=self.capture_and_checkin
        ).pack(pady=16)

        tk.Button(
            self.win,
            text="Select Image & Check-in",
            width=20,
            command=self.select_image_and_checkin
        ).pack(pady=4)

        self.result_label = tk.Label(self.win, text="", fg="green")
        self.result_label.pack(pady=10)

    def capture_and_checkin(self):
        try:
            capturer = FaceCapture()
            face_img = capturer.capture_face("Check-in Capture")
            self._check_in_with_face(face_img)
        except Exception as exc:
            messagebox.showerror("Check-in Error", str(exc))

    def select_image_and_checkin(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not file_path:
            return
        try:
            capturer = FaceCapture()
            face_img = capturer.capture_from_file(file_path)
            self._check_in_with_face(face_img)
        except Exception as exc:
            messagebox.showerror("Check-in Error", str(exc))

    def _check_in_with_face(self, face_img):
        encoding = self.recognizer.extract_encoding(face_img)
        candidates = self.db.get_all_face_encodings()
        person_id, score = self.recognizer.compare(encoding, candidates)
        if person_id is None or score is None or score < self.match_threshold:
            score_txt = f"{score:.2f}" if score is not None else "N/A"
            self.result_label.config(text=f"No match found (best: {score_txt}).", fg="red")
            return
        time_str = self.manager.check_in(person_id)
        person = self.db.get_person(person_id)
        name = person[1] if person else f"ID {person_id}"
        self.result_label.config(
            text=f"Check-in success: {name} @ {time_str}",
            fg="green"
        )
        messagebox.showinfo("Check-in Success", f"{name} 签到成功！时间：{time_str}")
