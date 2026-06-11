import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_conn
from config import DEFAULT_FEE


class StudentsFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        # Form frame
        form = ttk.LabelFrame(self, text="Student Registration")
        form.pack(fill="x", padx=10, pady=10)

        # Form fields
        fields = [
            ("Admission No:", "adm", 0),
            ("Full Name:", "name", 1),
            ("Grade:", "grade", 2),
            ("Stream:", "stream", 3),
            ("Parent Name:", "parent", 4),
            ("Phone:", "phone", 5),
        ]

        self.entries = {}

        for label, key, row in fields:
            ttk.Label(form, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="e")
            self.entries[key] = ttk.Entry(form, width=30)
            self.entries[key].grid(row=row, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Student", command=self.update_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Student", command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)

        # Search
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_students())
        ttk.Button(search_frame, text="Clear Search", command=self.load_students).pack(side="left", padx=5)

        # Treeview
        columns = ("admission_no", "name", "grade", "stream", "parent", "phone", "expected", "paid", "balance")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        headings = {
            "admission_no": "Admission No",
            "name": "Name",
            "grade": "Grade",
            "stream": "Stream",
            "parent": "Parent",
            "phone": "Phone",
            "expected": "Expected Fee",
            "paid": "Paid",
            "balance": "Balance"
        }

        for col, heading in headings.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=100 if col not in ["name", "parent"] else 150)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def add_student(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}

        if not data["adm"] or not data["name"]:
            messagebox.showerror("Error", "Admission Number and Name are required")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO students(admission_no, name, grade, stream, parent, phone, expected, paid)
                VALUES(?,?,?,?,?,?,?,0)
            """, (data["adm"], data["name"], data["grade"], data["stream"], 
                  data["parent"], data["phone"], DEFAULT_FEE))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully")
            self.clear_form()
            self.load_students()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Admission number already exists")
        finally:
            conn.close()

    def update_student(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a student to update")
            return

        adm = self.tree.item(selected)["values"][0]
        data = {key: entry.get().strip() for key, entry in self.entries.items()}

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE students
            SET name=?, grade=?, stream=?, parent=?, phone=?
            WHERE admission_no=?
        """, (data["name"], data["grade"], data["stream"], data["parent"], data["phone"], adm))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student updated successfully")
        self.load_students()

    def delete_student(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a student to delete")
            return

        if messagebox.askyesno("Confirm", "Delete this student and all their payment records?"):
            adm = self.tree.item(selected)["values"][0]
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM payments WHERE admission_no=?", (adm,))
            cur.execute("DELETE FROM students WHERE admission_no=?", (adm,))
            conn.commit()
            conn.close()
            self.load_students()
            self.clear_form()

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def search_students(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_students()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_conn()
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT *, (expected - paid) as balance
            FROM students
            WHERE admission_no LIKE ? OR name LIKE ? OR parent LIKE ?
            ORDER BY name
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")).fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_conn()
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT *, (expected - paid) as balance
            FROM students
            ORDER BY name
        """).fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected)["values"]
            self.entries["adm"].delete(0, tk.END)
            self.entries["adm"].insert(0, values[0])
            self.entries["name"].delete(0, tk.END)
            self.entries["name"].insert(0, values[1])
            self.entries["grade"].delete(0, tk.END)
            self.entries["grade"].insert(0, values[2])
            self.entries["stream"].delete(0, tk.END)
            self.entries["stream"].insert(0, values[3])
            self.entries["parent"].delete(0, tk.END)
            self.entries["parent"].insert(0, values[4])
            self.entries["phone"].delete(0, tk.END)
            self.entries["phone"].insert(0, values[5])
            self.entries["adm"].config(state="readonly")
