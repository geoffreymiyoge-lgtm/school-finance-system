import tkinter as tk
from tkinter import messagebox
from database import get_conn

class LoginWindow:

    def __init__(self, root, success_callback):
        self.root = root
        self.success_callback = success_callback

        tk.Label(root,text="Username").pack(pady=5)

        self.user = tk.Entry(root)
        self.user.pack()

        tk.Label(root,text="Password").pack()

        self.password = tk.Entry(root,show="*")
        self.password.pack()

        tk.Button(
            root,
            text="Login",
            command=self.login
        ).pack(pady=10)

    def login(self):

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE username=? AND password=?
            """,
            (
                self.user.get(),
                self.password.get()
            )
        )

        row = cur.fetchone()

        conn.close()

        if row:
            self.success_callback()
        else:
            messagebox.showerror(
                "Login",
                "Invalid username/password"
            )
