from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import Toplevel
from student import Student
from Developer import Developer
from Train import Train
from attendance import Attendance
import os
import subprocess
import platform

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1530x790+0+0")

        # ---------------- First Row Images ----------------
        self.add_top_images()

        # ---------------- Background Image ----------------
        img_bg = Image.open(r"photo/11831.jpg")
        img_bg = img_bg.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photo_bg = ImageTk.PhotoImage(img_bg)
        bg_img = Label(self.root, image=self.photo_bg)
        bg_img.place(x=0, y=130, width=1530, height=710)

        # ---------------- Title Label ----------------
        title_lbl = Label(
            bg_img,
            text="FACE  RECOGNITION  ATTENDANCE  SYSTEM  SOFTWARE",
            font=("times new roman", 30, "bold"),
            bg="lavender",
            fg="blue"
        )
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # ---------------- Time Display ----------------
        lbl_time = Label(title_lbl, font=("times new roman", 14, "bold"),
                         background='lavender', foreground='blue')
        lbl_time.place(x=1380, y=5, width=150, height=40)
        self.update_time(lbl_time)

        # ---------------- Buttons ----------------
        self.add_buttons(bg_img)

    # ---------------- Top Row Images ----------------
    def add_top_images(self):
        images = [
            r"photo/face-recognition-personal-identification-collage (4).jpg",
            r"photo/face-recognition-personal-identification-collage.jpg",
            r"photo/face-recognition-personal-identification-collage (3).jpg"
        ]
        for i, img_path in enumerate(images):
            img = Image.open(img_path)
            img = img.resize((500, 130), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = Label(self.root, image=photo)
            lbl.image = photo
            lbl.place(x=i*500, y=0, width=500, height=130)

    # ---------------- Update Time ----------------
    def update_time(self, lbl):
        from time import strftime
        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)
        time()

    # ---------------- Add Buttons ----------------
    def add_buttons(self, bg_img):
        btn_data = [
            ("Student Details", r"photo/group-young-students-front-school-building.jpg", self.open_student, 200, 100),
            ("Face Detector", r"photo/face-recognition-personal-identification-collage (2).jpg", self.open_face_recognizer, 500, 100),
            ("Attendance", r"photo/Choosing-The-Right-Attendance-Management-System.jpg", self.open_attendance, 800, 100),
            ("Help Desk", r"photo/man-working-call-center-office.jpg", self.open_helpdesk, 1100, 100),
            ("Train Data", r"photo/gps-system-smart-car.jpg", self.open_train, 200, 380),
            ("Photos", r"photo/close-up-man-robotic-process-automation-concept.jpg", self.open_photos, 500, 380),
            ("Developer", r"photo/developer.jpg", self.open_developer, 800, 380),
            ("Exit", r"photo/escape-concept-illustration_114360-5786.jpg", self.exit_app, 1100, 380)
        ]

        for name, img_path, cmd, x, y in btn_data:
            img = Image.open(img_path).resize((220, 220))
            photo = ImageTk.PhotoImage(img)
            btn = Button(bg_img, image=photo, command=cmd, cursor="hand2")
            btn.image = photo
            btn.place(x=x, y=y, width=220, height=220)

            btn_txt = Button(bg_img, text=name, command=cmd,
                             cursor="hand2", font=("times new roman", 15, "bold"),
                             bg="black", fg="white")
            btn_txt.place(x=x, y=y+200, width=220, height=40)

    # ---------------- Button Commands ----------------
    def open_student(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def open_face_recognizer(self):
        self.root.destroy()
        subprocess.Popen(["python", "face_recognition.py"])

    def open_attendance(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def open_helpdesk(self):
        self.new_window = Toplevel(self.root)
        try:
            from chatbot import Chatbot
            self.app = Chatbot(self.new_window)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open chatbot: {e}")

    def open_train(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def open_photos(self):
        folder_path = "data"
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", folder_path])
        else:
            subprocess.call(["xdg-open", folder_path])

    def open_developer(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)

    def exit_app(self):
        confirm = messagebox.askyesno("Face Recognition", "Do you want to exit the project?")
        if confirm:
            self.root.destroy()


# ---------------- Main ----------------
if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition_System(root)
    root.mainloop()
