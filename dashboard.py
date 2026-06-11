import tkinter as tk
from tkinter import ttk

from database import get_conn

from students import StudentsFrame
from payments import PaymentsFrame
from expenses import ExpensesFrame
from loans import LoansFrame


class Dashboard:

    def __init__(self, root):

        self.root = root

        root.title(
            "Itierio Elck Primary Boarding School Finance System"
        )

        root.geometry("1400x800")

        # ==========================
        # HEADER
        # ==========================

        title = tk.Label(
            root,
            text="ITIERIO ELCK PRIMARY BOARDING SCHOOL",
            font=("Arial", 18, "bold"),
            fg="navy"
        )

        title.pack(pady=5)

        subtitle = tk.Label(
            root,
            text="School Finance Management System",
            font=("Arial", 11)
        )

        subtitle.pack()

        # ==========================
        # DASHBOARD SUMMARY
        # ==========================

        self.summary = tk.Label(
            root,
            text="Loading...",
            font=("Arial", 11, "bold"),
            bg="lightyellow",
            relief="solid",
            pady=10
        )

        self.summary.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Button(
            root,
            text="Refresh Dashboard",
            command=self.load_dashboard
        ).pack(pady=5)

        # ==========================
        # NOTEBOOK
        # ==========================

        self.notebook = ttk.Notebook(root)

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ==========================
        # TABS
        # ==========================

        self.students_tab = StudentsFrame(
            self.notebook
        )

        self.payments_tab = PaymentsFrame(
            self.notebook
        )

        self.expenses_tab = ExpensesFrame(
            self.notebook
        )

        self.loans_tab = LoansFrame(
            self.notebook
        )

        self.notebook.add(
            self.students_tab,
            text="Students"
        )

        self.notebook.add(
            self.payments_tab,
            text="Payments"
        )

        self.notebook.add(
            self.expenses_tab,
            text="Expenses"
        )

        self.notebook.add(
            self.loans_tab,
            text="Loans"
        )

        # ==========================
        # STATUS BAR
        # ==========================

        self.status = tk.Label(
            root,
            text="System Ready",
            anchor="w",
            relief="sunken"
        )

        self.status.pack(
            fill="x",
            side="bottom"
        )

        self.load_dashboard()

    def load_dashboard(self):

        conn = get_conn()
        cur = conn.cursor()

        students = cur.execute(
            """
            SELECT COUNT(*)
            FROM students
            """
        ).fetchone()[0]

        collected = cur.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM payments
            """
        ).fetchone()[0]

        expenses = cur.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM expenses
            """
        ).fetchone()[0]

        loans = cur.execute(
            """
            SELECT COALESCE(SUM(given),0)
            FROM loans
            """
        ).fetchone()[0]

        outstanding_loans = cur.execute(
            """
            SELECT COALESCE(
                SUM(given - repaid),
                0
            )
            FROM loans
            """
        ).fetchone()[0]

        expected_fees = cur.execute(
            """
            SELECT COALESCE(
                SUM(expected),
                0
            )
            FROM students
            """
        ).fetchone()[0]

        total_paid = cur.execute(
            """
            SELECT COALESCE(
                SUM(paid),
                0
            )
            FROM students
            """
        ).fetchone()[0]

        fee_balance = (
            expected_fees - total_paid
        )

        cash_balance = (
            collected
            - expenses
            - loans
        )

        self.summary.config(
            text=
            f"Students: {students}   |   "
            f"Collected: KSh {collected:,.2f}   |   "
            f"Expenses: KSh {expenses:,.2f}   |   "
            f"Loans Given: KSh {loans:,.2f}   |   "
            f"Outstanding Loans: KSh {outstanding_loans:,.2f}   |   "
            f"Fee Balance: KSh {fee_balance:,.2f}   |   "
            f"Cash Balance: KSh {cash_balance:,.2f}"
        )

        conn.close()

        self.status.config(
            text="Dashboard updated successfully"
        )


def start():

    root = tk.Tk()

    Dashboard(root)

    root.mainloop()
