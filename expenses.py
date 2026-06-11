import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import get_conn


class ExpensesFrame(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):

        top = ttk.LabelFrame(
            self,
            text="School Expenses"
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            top,
            text="Description"
        ).grid(row=0, column=0, padx=5)

        self.desc = ttk.Entry(
            top,
            width=40
        )

        self.desc.grid(
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
            width=20
        )

        self.amount.grid(
            row=0,
            column=3,
            padx=5
        )

        ttk.Button(
            top,
            text="Add Expense",
            command=self.add_expense
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        ttk.Button(
            top,
            text="Delete Selected",
            command=self.delete_expense
        ).grid(
            row=0,
            column=5,
            padx=10
        )

        columns = (
            "id",
            "date",
            "description",
            "amount"
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

    def add_expense(self):

        description = self.desc.get()

        if not description:

            messagebox.showerror(
                "Error",
                "Description required"
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
            INSERT INTO expenses(
                date,
                description,
                amount
            )
            VALUES(?,?,?)
            """,
            (
                str(datetime.now().date()),
                description,
                amount
            )
        )

        conn.commit()
        conn.close()

        self.load_expenses()

        self.desc.delete(0, tk.END)
        self.amount.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Expense saved"
        )

    def delete_expense(self):

        selected = self.tree.focus()

        if not selected:
            return

        expense_id = self.tree.item(
            selected
        )["values"][0]

        if not messagebox.askyesno(
            "Delete",
            "Delete selected expense?"
        ):
            return

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM expenses
            WHERE id=?
            """,
            (expense_id,)
        )

        conn.commit()
        conn.close()

        self.load_expenses()

    def load_expenses(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_conn()
        cur = conn.cursor()

        rows = cur.execute(
            """
            SELECT *
            FROM expenses
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
