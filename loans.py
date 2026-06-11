import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import get_conn


class LoansFrame(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.create_widgets()
        self.load_loans()

    def create_widgets(self):

        form = ttk.LabelFrame(
            self,
            text="Teacher Loans"
        )

        form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            form,
            text="Teacher Name"
        ).grid(row=0, column=0)

        self.teacher = ttk.Entry(
            form,
            width=30
        )

        self.teacher.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Label(
            form,
            text="Loan Amount"
        ).grid(row=0, column=2)

        self.amount = ttk.Entry(
            form,
            width=20
        )

        self.amount.grid(
            row=0,
            column=3,
            padx=5
        )

        ttk.Button(
            form,
            text="Give Loan",
            command=self.give_loan
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        ttk.Label(
            form,
            text="Repayment"
        ).grid(row=1, column=0)

        self.repay_amount = ttk.Entry(
            form,
            width=20
        )

        self.repay_amount.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            form,
            text="Record Repayment",
            command=self.record_repayment
        ).grid(
            row=1,
            column=2,
            padx=10
        )

        columns = (
            "id",
            "teacher",
            "date",
            "given",
            "repaid",
            "balance"
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(
                col,
                text=col.upper()
            )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def give_loan(self):

        teacher = self.teacher.get()

        if not teacher:

            messagebox.showerror(
                "Error",
                "Teacher name required"
            )

            return

        try:
            amount = float(
                self.amount.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid amount"
            )

            return

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO loans(
                teacher,
                date,
                given,
                repaid
            )
            VALUES(?,?,?,0)
            """,
            (
                teacher,
                str(datetime.now().date()),
                amount
            )
        )

        conn.commit()
        conn.close()

        self.load_loans()

        self.teacher.delete(0, tk.END)
        self.amount.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Loan recorded"
        )

    def record_repayment(self):

        selected = self.tree.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a loan first"
            )

            return

        try:
            repayment = float(
                self.repay_amount.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid repayment amount"
            )

            return

        loan_id = self.tree.item(
            selected
        )["values"][0]

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE loans
            SET repaid = repaid + ?
            WHERE id=?
            """,
            (
                repayment,
                loan_id
            )
        )

        conn.commit()
        conn.close()

        self.load_loans()

        self.repay_amount.delete(
            0,
            tk.END
        )

        messagebox.showinfo(
            "Success",
            "Repayment recorded"
        )

    def load_loans(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_conn()
        cur = conn.cursor()

        rows = cur.execute(
            """
            SELECT *
            FROM loans
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        for row in rows:

            balance = row[3] - row[4]

            self.tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    balance
                )
            )
