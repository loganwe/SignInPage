import tkinter as tk
from tkinter import messagebox
import json
import os
import bcrypt

class SignInApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign In")
        self.root.geometry("300x200")
        
        # Load accounts or create empty dict if file doesn't exist
        self.accounts_file = os.path.join(os.path.dirname(__file__), "accounts.json")
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, "r") as f:
                self.accounts = json.load(f)
        else:
            self.accounts = {}
        
        # Username label and entry
        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        
        # Password label and entry
        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        
        # Sign In button
        tk.Button(root, text="Sign In", command=self.sign_in).pack(pady=10)
    
    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        if username in self.accounts:
            stored_hash = self.accounts[username]["password_hash"].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                messagebox.showinfo("Success", f"Welcome, {username}!")
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignInApp(root)
    root.mainloop()