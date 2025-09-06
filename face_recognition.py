from tkinter import *
from PIL import Image, ImageTk
import cv2
import os
import subprocess
import tkinter as tk
import mysql.connector
from attendance import Attendance  # Import Attendance class


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1530x790+0+0")

        title_lbl = Label(self.root, text="FACE RECOGNITION",
                          font=("times new roman", 30, "bold"),
                          bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_left = Image.open(r"photo\1_RZc0lk7gkMGXv6nEOwc7Ng.jpg")
        img_left = img_left.resize((650, 700), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        lbl_left = Label(self.root, image=self.photoimg_left)
        lbl_left.place(x=0, y=55, width=650, height=700)

        img_right = Image.open(r"photo\2401770.jpg")
        img_right = img_right.resize((950, 700), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)
        lbl_right = Label(self.root, image=self.photoimg_right)
        lbl_right.place(x=650, y=55, width=950, height=700)

        btn_face = Button(lbl_right, text="Face Recognition", command=self.face_recog,
                          font=("times new roman", 15, "bold"), bg="blue", fg="white")
        btn_face.place(x=375, y=550, width=200, height=45)

        btn_exit = Button(lbl_right, text="Exit", command=self.back_to_main,
                          font=("times new roman", 15, "bold"), bg="blue", fg="white")
        btn_exit.place(x=375, y=600, width=200, height=45)

    # ---------------- Fetch Student Details ----------------
    def get_student_details(self, student_id):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345678", 
                database="face recognition system"  
            )
            cursor = conn.cursor()
            cursor.execute("SELECT Name, Dep FROM student WHERE Student_id=%s", (student_id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                return result[0], result[1]   # (Name, Dep)
            else:
                return None, None
        except Exception as e:
            print("Database error:", e)
            return None, None

    # ---------------- Face Recognition ----------------
    def face_recog(self):
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)
        cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("❌ Failed to grab frame")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 10)

            for (x, y, w, h) in faces:
                id, predict = clf.predict(gray[y:y+h, x:x+w])
                confidence = int(100 * (1 - predict / 300))

                if confidence > 70:
                    name, dept = self.get_student_details(id)
                    if name:
                        cv2.putText(img, f"ID:{id} | {name} | {dept}", (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                        # ---- Mark attendance ----
                        root = tk.Tk()
                        root.withdraw()
                        app = Attendance(root)
                        app.mark_attendance(id, name, dept)
                        root.destroy()
                    else:
                        cv2.putText(img, "Unknown", (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                else:
                    cv2.putText(img, "Unknown", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

            cv2.imshow("Face Recognition", img)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == 13:  # ESC or Enter to exit
                break

        video_cap.release()
        cv2.destroyAllWindows()

    def back_to_main(self):
        self.root.destroy()
        subprocess.Popen(["python", "main.py"])


# ---------------- Main ----------------
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
