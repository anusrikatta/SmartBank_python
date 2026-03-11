import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ANU BANK")
        self.root.geometry("500x500")
        self.root.configure(bg="#1e1e2f")   # dark background
        self.root.resizable(False, False)

        self.accounts = {}
        self.load_accounts()
        self.show_login()
    def load_accounts(self):
        try:
            with open("accounts.txt", "r") as file:
                for line in file:
                    name, acc, balance, pin = line.strip().split(",")
                    self.accounts[acc] = {
                        "name": name,
                        "balance": float(balance),
                        "pin": pin
                    }
        except FileNotFoundError:
            pass

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg="#2c2c3e", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="ANU BANK LOGIN",
                 font=("Arial", 18, "bold"),
                 bg="#2c2c3e", fg="white").pack(pady=20)

        tk.Label(frame, text="Account Number",
                 bg="#2c2c3e", fg="white").pack()
        self.acc_entry = tk.Entry(frame, width=25)
        self.acc_entry.pack(pady=5)

        tk.Label(frame, text="PIN",
                 bg="#2c2c3e", fg="white").pack()
        self.pin_entry = tk.Entry(frame, show="*", width=25)
        self.pin_entry.pack(pady=5)

        tk.Button(frame, text="Login",
                  bg="#4CAF50", fg="white",
                  width=20,
                  command=self.login).pack(pady=10)

        tk.Button(frame, text="Register",
                  bg="#2196F3", fg="white",
                  width=20,
                  command=self.show_register).pack(pady=5)

    def show_register(self):
        self.clear_screen()

        tk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.root, text="Name").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="Account Number").pack()
        self.new_acc_entry = tk.Entry(self.root)
        self.new_acc_entry.pack()

        tk.Label(self.root, text="Initial Balance").pack()
        self.balance_entry = tk.Entry(self.root)
        self.balance_entry.pack()

        tk.Label(self.root, text="PIN").pack()
        self.new_pin_entry = tk.Entry(self.root, show="*")
        self.new_pin_entry.pack()

        tk.Button(self.root, text="Create Account", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_login).pack()

    def login(self):
        acc = self.acc_entry.get()
        pin = self.pin_entry.get()

        if acc in self.accounts and self.accounts[acc]["pin"] == pin:
            self.current_account = acc
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def register(self):
        name = self.name_entry.get()
        acc = self.new_acc_entry.get()
        balance = self.balance_entry.get()
        pin = self.new_pin_entry.get()

        if acc in self.accounts:
            messagebox.showerror("Error", "Account already exists")
            return

        self.accounts[acc] = {
            "name": name,
            "balance": float(balance),
            "pin": pin
        }

        with open("accounts.txt", "a") as file:
            file.write(f"{name},{acc},{balance},{pin}\n")

        messagebox.showinfo("Success", "Account Created Successfully")
        self.show_login()
    def check_balance(self):
        balance = self.accounts[self.current_account]["balance"]
        messagebox.showinfo("Balance", f"Your current balance is ₹{balance}")
    def show_dashboard(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg="#2c2c3e", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        name = self.accounts[self.current_account]["name"]

        tk.Label(frame, text=f"Welcome {name}",
                 font=("Arial", 16, "bold"),
                 bg="#2c2c3e", fg="white").pack(pady=20)

        tk.Button(frame, text="Check Balance",
                  bg="#9C27B0", fg="white",
                  width=20,
                  command=self.check_balance).pack(pady=5)

        tk.Button(frame, text="Deposit",
                  bg="#4CAF50", fg="white",
                  width=20,
                  command=self.deposit).pack(pady=5)

        tk.Button(frame, text="Withdraw",
                  bg="#f44336", fg="white",
                  width=20,
                  command=self.withdraw).pack(pady=5)

        tk.Button(frame, text="Logout",
                  bg="gray", fg="white",
                  width=20,
                  command=self.show_login).pack(pady=15)
    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")

        if amount is not None and amount > 0:
            # Update balance
            self.accounts[self.current_account]["balance"] += amount
            self.update_balance()

            # Get current date & time
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save transaction
            with open("transactions.txt", "a") as file:
                file.write(f"{self.current_account},Deposit,{amount},{now}\n")

            messagebox.showinfo("Success", "Amount Deposited Successfully")
    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")

        if amount is not None and amount > 0:
            if amount <= self.accounts[self.current_account]["balance"]:
                self.accounts[self.current_account]["balance"] -= amount
                self.update_balance()
                messagebox.showinfo("Success", "Amount Withdrawn Successfully")
            else:
                messagebox.showerror("Error", "Insufficient Balance")
    def update_balance(self):
        with open("accounts.txt", "w") as file:
            for acc, data in self.accounts.items():
                file.write(f"{data['name']},{acc},{data['balance']},{data['pin']}\n")
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Transaction History")
        history_window.geometry("400x300")

        tk.Label(history_window, text="Transaction History", font=("Arial", 14)).pack()

        try:
            with open("transactions.txt", "r") as file:
                for line in file:
                    acc, ttype, amount, date = line.strip().split(",")
                    if acc == self.current_account:
                        tk.Label(history_window, text=f"{ttype} ₹{amount} on {date}").pack()
        except FileNotFoundError:
            tk.Label(history_window, text="No Transactions Found").pack()

root = tk.Tk()
app = BankingApp(root)
root.mainloop()
