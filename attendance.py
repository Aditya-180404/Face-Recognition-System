import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class Attendance:
    def __init__(self, root=None):
        self.root = root
        self.filename = "attendance.csv"

        # Ensure CSV file exists with header
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Department", "Date", "Time"])

        # GUI mode (opened from main.py)
        if self.root:
            self.root.title("Attendance Records")
            self.root.geometry("700x400")

            # Table
            self.tree = ttk.Treeview(
                self.root,
                columns=("ID", "Name", "Dept", "Date", "Time"),
                show="headings",
            )
            self.tree.heading("ID", text="ID")
            self.tree.heading("Name", text="Name")
            self.tree.heading("Dept", text="Department")
            self.tree.heading("Date", text="Date")
            self.tree.heading("Time", text="Time")
            self.tree.pack(fill="both", expand=True)

            # Buttons
            btn_frame = tk.Frame(self.root)
            btn_frame.pack(fill="x", pady=5)

            tk.Button(btn_frame, text="Refresh", command=self.load_attendance,
                      bg="blue", fg="white").pack(side="left", padx=5)
            tk.Button(btn_frame, text="Export CSV", command=self.export_csv,
                      bg="green", fg="white").pack(side="left", padx=5)

            self.load_attendance()

    # ---------------- Mark Attendance ----------------
    def mark_attendance(self, id, name, dept):
        """Mark attendance into CSV file (called from face recognition)."""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Check if already marked today
        already_marked = False
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if len(row) >= 4 and row[0] == str(id) and row[3] == date_str:
                    already_marked = True
                    break

        if not already_marked:
            with open(self.filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([id, name, dept, date_str, time_str])

            print(f"✅ Attendance marked: {id}, {name}, {dept}, {date_str} {time_str}")
            if self.root:
                messagebox.showinfo("Attendance", f"{name} marked present!")
        else:
            print(f"ℹ️ {name} already marked for {date_str}")

    # ---------------- Load Attendance into GUI ----------------
    def load_attendance(self):
        if not self.root:
            return
        for row in self.tree.get_children():
            self.tree.delete(row)

        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                self.tree.insert("", "end", values=row)

    # ---------------- Export Attendance CSV ----------------
    def export_csv(self):
        if not os.path.exists(self.filename):
            messagebox.showerror("Error", "No attendance data found!")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if save_path:
            with open(self.filename, "r") as src, open(save_path, "w", newline="") as dst:
                dst.write(src.read())
            messagebox.showinfo("Export", f"Attendance exported to {save_path}")


# ---------------- Run Directly (for testing) ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Attendance(root)
    root.mainloop()
