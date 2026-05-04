import sys
from datetime import datetime

class BankAccount:
    def __init__(self, name, pin, initial_balance=0.0):
        self.name = name
        self.pin = pin
        self.balance = initial_balance
        self.transactions = []
        if initial_balance > 0:
            self._add_transaction("Initial Deposit", initial_balance)

    def _add_transaction(self, t_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({"type": t_type, "amount": amount, "timestamp": timestamp})

    def verify_pin(self, pin):
        return self.pin == pin

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._add_transaction("Deposit", amount)
            print(f"\n✅ Successfully deposited ${amount:.2f}")
            self.display_balance()
        else:
            print("\n❌ Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self._add_transaction("Withdrawal", amount)
                print(f"\n✅ Successfully withdrew ${amount:.2f}")
                self.display_balance()
            else:
                print(f"\n❌ Insufficient funds. Your current balance is ${self.balance:.2f}")
        else:
            print("\n❌ Withdrawal amount must be positive.")

    def display_balance(self):
        print(f"💰 Current Balance: ${self.balance:.2f}")

    def show_transaction_history(self):
        print("\n--- Transaction History ---")
        if not self.transactions:
            print("No transactions yet.")
        else:
            for t in self.transactions:
                print(f"[{t['timestamp']}] {t['type']}: ${t['amount']:.2f}")
        print("---------------------------")


def main():
    print("🏦 Welcome to the Simple Banking App!")
    
    # Account Creation
    print("\n--- Create Your Account ---")
    name = input("Enter your name: ")
    while True:
        pin = input("Create a 4-digit PIN: ")
        if len(pin) == 4 and pin.isdigit():
            break
        print("❌ PIN must be exactly 4 digits. Please try again.")
    
    account = BankAccount(name, pin)
    print(f"\n✅ Account created successfully for {name}!")

    # Main Banking Loop
    while True:
        print("\n=== Main Menu ===")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. View Transaction History")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")

        if choice == '5':
            print("\nThank you for using our banking app. Goodbye! 👋")
            break
        
        if choice in ['1', '2', '3', '4']:
            # Require PIN for all sensitive operations
            entered_pin = input("\n🔒 Enter your PIN to continue: ")
            if not account.verify_pin(entered_pin):
                print("❌ Incorrect PIN. Access denied.")
                continue
            
            if choice == '1':
                try:
                    amount = float(input("Enter amount to deposit: $"))
                    account.deposit(amount)
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number.")
            
            elif choice == '2':
                try:
                    amount = float(input("Enter amount to withdraw: $"))
                    account.withdraw(amount)
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number.")
            
            elif choice == '3':
                print(f"\nAccount Holder: {account.name}")
                account.display_balance()
                
            elif choice == '4':
                account.show_transaction_history()
        else:
            print("❌ Invalid choice. Please select an option from 1 to 5.")

if __name__ == "__main__":
    main()
