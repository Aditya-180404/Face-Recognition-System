from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import Toplevel
import threading

# Simulated user database
USER_DB = {
    "UIT": "1234",
    "TeamLooser":"12345"
}

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        
        # Background
        bg_img = Image.open(r"photo/11831.jpg").resize((1550, 800))
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
        
        # Login Frame
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=450)
        
        Label(frame, text="Get Started", font=("times new roman", 20, "bold"), fg="white", bg="black").place(x=95, y=60)
        Label(frame, text="Username", font=("times new roman", 15, "bold"), fg="white", bg="black").place(x=70, y=115)
        Label(frame, text="Password", font=("times new roman", 15, "bold"), fg="white", bg="black").place(x=70, y=185)
        
        self.username_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.username_entry.place(x=40, y=140, width=270)
        self.password_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.password_entry.place(x=40, y=210, width=270)
        
        # Buttons
        Button(frame, text="Login", command=self.login, font=("times new roman", 15, "bold"),
               bd=3, relief=RIDGE, fg="white", bg="red", activeforeground="white", activebackground="red")\
               .place(x=110, y=260, width=120, height=35)
        
        Button(frame, text="Forgot Password", font=("times new roman", 10, "bold"),
               borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black",
               command=self.forgot_password).place(x=15, y=340, width=160)
        
        self.root.bind('<Return>', lambda event: self.login())
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
        elif username in USER_DB and USER_DB[username] == password:
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.root.withdraw()
            threading.Thread(target=self.open_main_system).start()
        else:
            messagebox.showerror("Invalid", "Invalid username or password")
    
    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Please contact the administrator to reset your password.")
    
    def open_main_system(self):
        from main import Face_Recognition_System
        main_window = Toplevel()
        Face_Recognition_System(main_window)


if __name__ == "__main__":
    root = Tk()
    LoginWindow(root)
    root.mainloop()
