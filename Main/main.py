import json
import random
import string
from pathlib import Path

class Bank:
    DATABASE = 'data.json'
    MAX_DEPOSIT = 10000
    data = []

    def __init__(self):
        """Load database on object creation."""
        if Path(self.DATABASE).exists():
            try:
                with open(self.DATABASE) as fs:
                    Bank.data = json.load(fs)
            except json.JSONDecodeError:
                Bank.data = []
        else:
            Bank.data = []

    @staticmethod
    def __update():
        """Save current data to file."""
        with open(Bank.DATABASE, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)

    @staticmethod
    def __accountgenerate():
        """Generate random account number."""
        alpha = random.choices(string.ascii_letters, k=3)
        nums = random.choices(string.digits, k=3)
        spchar = random.choices("@$%^&*", k=1)
        acc_id = alpha + nums + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

    @staticmethod
    def __get_user():
        """Common function to get user data by acc no and pin."""
        accnumber = input("Please tell your account number: ").strip()
        try:
            pin = int(input("Please enter your PIN: ").strip())
        except ValueError:
            print("PIN must be numeric.")
            return None

        userdata = [u for u in Bank.data if u["acc.no"] == accnumber and u["pin"] == pin]
        return userdata[0] if userdata else None

    def Createaccount(self):
        """Create a new bank account."""
        name = input("Enter name: ").strip()
        try:
            age = int(input("Enter age: ").strip())
        except ValueError:
            print("Age must be a number.")
            return

        email = input("Enter email: ").strip()
        try:
            pin = int(input("Enter your 4-digit PIN: ").strip())
        except ValueError:
            print("PIN must be numeric.")
            return

        if age < 18 or len(str(pin)) != 4:
            print("Sorry, not eligible to create an account.")
            return

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "acc.no": Bank.__accountgenerate(),
            "balance": 0
        }

        Bank.data.append(info)
        Bank.__update()
        print("\nAccount created successfully!")
        for k, v in info.items():
            print(f"{k}: {v}")
        print("Please note down your account number.")

    def Depositmoney(self):
        """Deposit money into an account."""
        user = self.__get_user()
        if not user:
            print("Sorry, no matching account found.")
            return

        try:
            amount = int(input("How much you want to deposit: ").strip())
        except ValueError:
            print("Amount must be numeric.")
            return

        if amount <= 0 or amount > self.MAX_DEPOSIT:
            print(f"Deposit must be between 1 and {self.MAX_DEPOSIT}.")
            return

        user["balance"] += amount
        Bank.__update()
        print("Deposit successful!")

    def Withdrawmoney(self):
        """Withdraw money from an account."""
        user = self.__get_user()
        if not user:
            print("Sorry, no matching account found.")
            return

        try:
            amount = int(input("How much you want to withdraw: ").strip())
        except ValueError:
            print("Amount must be numeric.")
            return

        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if user["balance"] < amount:
            print("Sorry, insufficient balance.")
            return

        user["balance"] -= amount
        Bank.__update()
        print("Withdrawal successful!")

    def Details(self):
        """Display account details."""
        user = self.__get_user()
        if not user:
            print("Sorry, no matching account found.")
            return

        print("\nAccount Information:")
        for k, v in user.items():
            print(f"{k}: {v}")

    def UpdateDetails(self):
        """Update account name, email, or PIN."""
        user = self.__get_user()
        if not user:
            print("No such user found.")
            return

        print("You can change name, email, and PIN. Leave blank to keep unchanged.")
        new_name = input("New name: ").strip()
        new_email = input("New email: ").strip()
        new_pin = input("New PIN (4 digits): ").strip()

        if new_name:
            user["name"] = new_name
        if new_email:
            user["email"] = new_email
        if new_pin.isdigit() and len(new_pin) == 4:
            user["pin"] = int(new_pin)
        elif new_pin:
            print("Invalid PIN format. Skipping PIN change.")

        Bank.__update()
        print("Details updated successfully.")

    def DeleteAccount(self):
        """Delete a bank account."""
        user = self.__get_user()
        if not user:
            print("No such account found.")
            return

        confirm = input("Press Y to confirm deletion: ").strip().upper()
        if confirm == "Y":
            Bank.data.remove(user)
            Bank.__update()
            print("Account deleted successfully.")
        else:
            print("Account deletion cancelled.")



if __name__ == "__main__":
    bank = Bank()
    menu = {
        1: bank.Createaccount,
        2: bank.Depositmoney,
        3: bank.Withdrawmoney,
        4: bank.Details,
        5: bank.UpdateDetails,
        6: bank.DeleteAccount
    }

    print("\nBank Management System")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Details")
    print("5. Update Details")
    print("6. Delete Account")

    try:
        choice = int(input("Enter choice: "))
        menu.get(choice, lambda: print("Invalid choice"))()
    except ValueError:
        print("Please enter a number from 1 to 6.")
