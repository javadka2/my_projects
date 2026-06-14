import json
import os
import datetime

class BankAccount:
    def __init__(self, account_number, holder_name, balance=0):
        if balance < 0:
            raise ValueError("Initial balance can't be negative.")
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        self.transaction_history = []
        self.record_transaction('Initial Balance', balance)

    def record_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append({
            "timestamp": timestamp,
            "type": transaction_type,
            "amount": amount,
            "current_balance": self.balance
        })

    def deposit(self, amount):
        if amount <= 0:
            print('Deposit amount must be greater than 0.')
            return False
        self.balance += amount
        self.record_transaction('Deposit', amount)
        print(f"Amount: {amount} deposited. New balance: {self.balance}")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return False
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        self.balance -= amount
        self.record_transaction('Withdrawal', amount)
        print(f"Amount: {amount} withdrawn. New balance: {self.balance}")
        return True

    def get_balance(self):
        return self.balance

    def show_info(self):
        print("-----------")
        print(f"Account Number: {self.account_number}")
        print(f"Holder Name: {self.holder_name}")
        print(f"Balance: {self.balance}")
        print("-----------")

    def show_transactions(self):
        print("Transaction History:")
        if not self.transaction_history:
            print("No transactions found.")
            return
        for t in self.transaction_history:
            print(f"- {t['timestamp']} | Type: {t['type']} | Amount: {t['amount']} | Balance after: {t['current_balance']}")

def save_accounts_to_file(accounts, filename="accounts.json"):
    data = {}
    try:
        for acc_num, acc_obj in accounts.items():
            data[acc_num] = {
                "holder_name": acc_obj.holder_name,
                "balance": acc_obj.balance,
                "transaction_history": acc_obj.transaction_history
            }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving accounts to file: {e}")
        return False

def load_accounts_from_file(filename="accounts.json"):
    if not os.path.exists(filename):
        print(f"No existing account file found at {filename}. Starting fresh.")
        return {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}. File might be corrupted. Starting fresh.")
        return {}
    except Exception as e:
        print(f"Error loading accounts from file: {e}")
        return {}

    accounts = {}
    for acc_num, acc_data in data.items():
        try:
            if "holder_name" in acc_data and "balance" in acc_data and "transaction_history" in acc_data:
                acc = BankAccount(
                    acc_num,
                    acc_data["holder_name"],
                    acc_data["balance"]
                )
                acc.transaction_history = acc_data["transaction_history"]
                accounts[acc_num] = acc
            else:
                print(f"Skipping account {acc_num} due to missing data.")
        except Exception as e:
            print(f"Error processing account {acc_num}: {e}")

    print(f"Loaded {len(accounts)} accounts.")
    return accounts

def display_menu():
    print("""
    ===== Managing Your Bank Account =====
    1 - Create Account
    2 - Deposit
    3 - Withdraw
    4 - Check Balance
    5 - Show Transactions
    6 - Show Account Info
    7 - Delete Account  
    8 - Exit           
    """)

def main():
    accounts = load_accounts_from_file()

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            acc_num = input("Enter account number: ")
            name = input("Enter account holder's name: ")
            try:
                balance_str = input("Enter initial balance (default 0): ")
                balance = int(balance_str) if balance_str else 0
                
                if acc_num in accounts:
                    print("Account number already exists!")
                else:
                    new_account = BankAccount(acc_num, name, balance)
                    accounts[acc_num] = new_account
                    if save_accounts_to_file(accounts):
                         print("Account created successfully and saved.")
                    else:
                         print("Account created, but failed to save.")
            except ValueError:
                print("Invalid input for balance. Please enter a number.")
            except Exception as e:
                print(f"An error occurred during account creation: {e}")

        elif choice == "2": 
            acc_num = input("Enter account number: ")
            if acc_num not in accounts:
                print("Account not found.")
                continue
            try:
                amount_str = input("Enter amount to deposit: ")
                amount = int(amount_str)
                if accounts[acc_num].deposit(amount):
                    if save_accounts_to_file(accounts):
                        print("Deposit successful and saved.")
                    else:
                        print("Deposit successful, but failed to save.")
            except ValueError:
                print("Invalid input for amount. Please enter a number.")
            except Exception as e:
                print(f"An error occurred during deposit: {e}")

        elif choice == "3":
            acc_num = input("Enter account number: ")
            if acc_num not in accounts:
                print("Account not found.")
                continue
            try:
                amount_str = input("Enter amount to withdraw: ")
                amount = int(amount_str)
                if accounts[acc_num].withdraw(amount):
                    if save_accounts_to_file(accounts):
                        print("Withdrawal successful and saved.")
                    else:
                        print("Withdrawal successful, but failed to save.")
            except ValueError:
                print("Invalid input for amount. Please enter a number.")
            except Exception as e:
                print(f"An error occurred during withdrawal: {e}")

        elif choice == "4":
            acc_num = input("Enter account number: ")
            if acc_num not in accounts:
                print("Account not found.")
                continue
            print(f"Balance: {accounts[acc_num].get_balance()}")

        elif choice == "5":
            acc_num = input("Enter account number: ")
            if acc_num not in accounts:
                print("Account not found.")
                continue
            accounts[acc_num].show_transactions()

        elif choice == "6":
            acc_num = input("Enter account number: ")
            if acc_num not in accounts:
                print("Account not found.")
                continue
            accounts[acc_num].show_info()

        elif choice == "7":
            acc_num = input("Enter the account number to delete: ")
            if acc_num not in accounts:
                print("Account not found. Nothing to delete.")
            else:
                confirm = input(f"Are you sure you want to delete account {acc_num} for {accounts[acc_num].holder_name}? (yes/no): ").lower()
                if confirm == 'yes':
                    del accounts[acc_num]
                    if save_accounts_to_file(accounts):
                        print(f"Account {acc_num} deleted successfully .")
                    else:
                        print(f"Account {acc_num} deleted, but failed to save changes.")
                else:
                    print("Account deletion cancelled.")

        elif choice == "8":
            if save_accounts_to_file(accounts):
                print("Goodbye!")
            else:
                print("Could not save changes. Goodbye anyway!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

main()