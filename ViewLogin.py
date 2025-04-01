from tkinter import ttk, messagebox
import tkinter as tk

class LoginView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Login Application")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_widgets()

        self.controller = controller  # Store a reference to the controller
    def create_widgets(self):
        # Add widgets for the login view using grid layout
        tk.Label(self, text="Username:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Helvetica", 12), width=20)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(self, text="Password:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.password_entry = tk.Entry(self, textvariable=self.password_var, show="*", font=("Helvetica", 12), width=20)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        self.login_button = ttk.Button(self, text="LOGIN", command=self.login, style="TButton")
        self.login_button.grid(row=2, column=1, pady=20, padx=10, sticky="e")

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10, background="#4CAF50", foreground="BLACK")

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        # Notify the controller about the login attempt
        self.controller.login(username, password)

    def show_message(self, message):
        messagebox.showinfo("Login Result", message)