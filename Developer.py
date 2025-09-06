from tkinter import *
from PIL import Image, ImageTk
import subprocess
import sys

class Developer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Title
        title_label = Label(
            self.root,
            text="Team Loosars Developers",
            bg="grey",
            fg="blue",
            font=("times new roman", 20, "bold")
        )
        title_label.place(x=0, y=0, width=1530, height=100)

        # Home button image
        img = Image.open(r"photo/images.jpeg").resize((70, 70), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        b1 = Button(title_label, image=self.photoimg, command=self.go_to_home, cursor="hand2")
        b1.place(x=10, y=0, width=70, height=70)

        self.home_button = Button(
            title_label, text="Home", command=self.go_to_home,
            cursor="hand2", font=("times new roman", 13, "bold"),
            bg="lavender", fg="black"
        )
        self.home_button.place(x=10, y=70, width=70, height=30)

        # Background image
        bg_image = Image.open(r"photo/developer.jpg").resize((1530, 790), Image.LANCZOS)
        self.photo_bg = ImageTk.PhotoImage(bg_image)
        background_label = Label(self.root, image=self.photo_bg)
        background_label.place(x=0, y=100, width=1530, height=700)

        # Developers info
        developers = [
            {"x": 0, "y": 110, "image": "Aditya.jpg", "role": "TEAM ADMIN", "name": "Aditya Roy"},
            {"x": 395, "y": 110, "image": "Samaresh.jpg", "role": "TEAM MEMBER", "name": "Samaresh Debnath"},
            {"x": 790, "y": 110, "image": "Subhasis.jpg", "role": "TEAM MEMBER", "name": "Subhasis Mahato"},
            {"x": 1180, "y": 110, "image": "Deepanjan.jpg", "role": "TEAM MEMBER", "name": "Deepanjan Seth"},
        ]

        for dev in developers:
            self.create_dev_frame(background_label, dev["x"], dev["y"], dev["image"], dev["role"], dev["name"])

    def create_dev_frame(self, parent, x, y, image_file, role, name):
        frame = Frame(parent, bd=2, bg="lavender")
        frame.place(x=x, y=y, width=350, height=500)

        img = Image.open(f"photo/{image_file}").resize((350, 250), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        Label(frame, image=photo).place(x=0, y=0, width=350, height=250)
        setattr(self, f"photo_{name.replace(' ', '_')}", photo)  # prevent garbage collection

        Label(frame, text=role, font=("times new roman", 20, "bold"),
              bg="lavender", fg="blue").place(relx=0.5, y=255, anchor="n")
        Label(frame, text=f"NAME : {name}", font=("times new roman", 20, "bold"),
              bg="lavender", fg="blue").place(x=5, y=295)
        Label(frame, text="DEPT : Information Technology", font=("times new roman", 18, "bold"),
              bg="lavender", fg="blue").place(x=5, y=335)
        Label(frame, text="Year : 1st Year", font=("times new roman", 18, "bold"),
              bg="lavender", fg="blue").place(x=5, y=375)
        Label(frame, text="College : University Institute of Technology,BU",
              font=("times new roman", 18, "bold"), bg="lavender", fg="blue",
              wraplength=330, justify="center").place(x=5, y=415)

    def go_to_home(self):
        """Close Developer window and open main.py as a separate process."""
        self.root.destroy()
        subprocess.Popen([sys.executable, "main.py"])


if __name__ == "__main__":
    root = Tk()
    app = Developer(root)
    root.mainloop()
