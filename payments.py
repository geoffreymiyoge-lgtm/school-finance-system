import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import get_conn
from receipts import create_receipt
from config import DEFAULT_FEE


class PaymentsFrame(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.create_widgets()
        self.load_payments()

    def create_widgets(self):

        top = ttk.LabelFrame(
            self,
            text="Fee Payment"
        )

        top.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ttk.Label(
            top,
            text="Admission Number"
        ).grid(row=0, column=0)

        self.adm = ttk.Entry(
            top,
            width=25
        )

        self.adm.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            top,
            text="Amount"
        ).grid(row=0, column=2)

        self.amount = ttk.Entry(
            top,
            width=25
        )

        self.amount.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Button(
            top,
            text="Record Payment",
            command=self.record_payment
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        ttk.Button(
            top,
            text="Search Student",
            command=self.search_student
        ).grid(
            row=0,
            column=5,
            padx=10
        )

        self.student_info = ttk.Label(
            self,
            text="",
            foreground="blue"
        )

        self.student_info.pack(
            fill="x",
            padx=10,
            pady=5
        )

        columns = (
            "id",
            "adm",
            "date",
            "amount"
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("adm", text="Admission")
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount")

        self.tree.column("id", width=60)
        self.tree.column("adm", width=150)
        self.tree.column("date", width=150)
        self.tree.column("amount", width=150)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def search_student(self):

        adm = self.adm.get()

        if not adm:
            return

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM students
            WHERE admission_no=?
            """,
            (adm,)
        )

        row = cur.fetchone()

        conn.close()

        if not row:

            messagebox.showerror(
                "Error",
                "Student not found"
            )

            return

        paid = row[7]
        balance = DEFAULT_FEE - paid

        self.student_info.config(
            text=(
                f"Name: {row[1]} | "
                f"Paid: KSh {paid:,.2f} | "
                f"Balance: KSh {balance:,.2f}"
            )
        )

    def record_payment(self):

        adm = self.adm.get()

        if not adm:

            messagebox.showerror(
                "Error",
                "Admission number required"
            )

            return

        try:
            amount = float(
                self.amount.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid amount"
            )

            return

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM students
            WHERE admission_no=?
            """,
            (adm,)
        )

        student = cur.fetchone()

        if not student:

            conn.close()

            messagebox.showerror(
                "Error",
                "Student not found"
            )

            return

        cur.execute(
            """
            INSERT INTO payments(
                admission_no,
                date,
                amount
            )
            VALUES(?,?,?)
            """,
            (
                adm,
                str(datetime.now().date()),
                amount
            )
        )

        cur.execute(
            """
            UPDATE students
            SET paid = paid + ?
            WHERE admission_no=?
            """,
            (
                amount,
                adm
            )
        )

        conn.commit()

        cur.execute(
            """
            SELECT paid
            FROM students
            WHERE admission_no=?
            """,
            (adm,)
        )

        paid = cur.fetchone()[0]

        conn.close()

        balance = DEFAULT_FEE - paid

        pdf_file = create_receipt(
            adm,
            student[1],
            amount,
            balance
        )

        messagebox.showinfo(
            "Payment Recorded",
            (
                f"Payment saved successfully.\n\n"
                f"Receipt generated:\n"
                f"{pdf_file}"
            )
        )

        self.load_payments()

        self.amount.delete(0, tk.END)

        self.search_student()

    def load_payments(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_conn()
        cur = conn.cursor()

        rows = cur.execute(
            """
            SELECT *
            FROM payments
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=row
            )
