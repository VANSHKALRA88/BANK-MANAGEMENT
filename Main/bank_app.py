import json
import random
import string
from pathlib import Path
import streamlit as st


DATABASE = 'data.json'
MAX_DEPOSIT = 10000


def load_data():
    if Path(DATABASE).exists():
        try:
            with open(DATABASE) as fs:
                return json.load(fs)
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    with open(DATABASE, 'w') as fs:
        json.dump(data, fs, indent=4)

def generate_account():
    alpha = random.choices(string.ascii_letters, k=3)
    nums = random.choices(string.digits, k=3)
    spchar = random.choices("@$%^&*", k=1)
    acc_id = alpha + nums + spchar
    random.shuffle(acc_id)
    return "".join(acc_id)

def find_user(acc_no, pin, data):
    return next((u for u in data if u["acc.no"] == acc_no and u["pin"] == pin), None)


st.set_page_config(page_title="Bank Management System", layout="centered")
st.title("🏦 Bank Management System")

menu = ["Create Account", "Deposit Money", "Withdraw Money", "View Details", "Update Details", "Delete Account"]
choice = st.sidebar.radio("Menu", menu)

data = load_data()


if choice == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password", max_chars=4)

    if st.button("Create Account"):
        if age < 18:
            st.error("Must be at least 18 years old.")
        elif not pin.isdigit() or len(pin) != 4:
            st.error("PIN must be exactly 4 digits.")
        else:
            account = {
                "name": name,
                "age": int(age),
                "email": email,
                "pin": int(pin),
                "acc.no": generate_account(),
                "balance": 0
            }
            data.append(account)
            save_data(data)
            st.success(f"Account created successfully! Your Account No: {account['acc.no']}")


elif choice == "Deposit Money":
    st.subheader("Deposit Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1, step=1)

    if st.button("Deposit"):
        user = find_user(acc_no, int(pin) if pin.isdigit() else -1, data)
        if not user:
            st.error("Account not found or incorrect PIN.")
        elif amount > MAX_DEPOSIT:
            st.error(f"Cannot deposit more than {MAX_DEPOSIT}.")
        else:
            user["balance"] += amount
            save_data(data)
            st.success(f"Deposited {amount} successfully! New Balance: {user['balance']}")


elif choice == "Withdraw Money":
    st.subheader("Withdraw Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1, step=1)

    if st.button("Withdraw"):
        user = find_user(acc_no, int(pin) if pin.isdigit() else -1, data)
        if not user:
            st.error("Account not found or incorrect PIN.")
        elif amount > user["balance"]:
            st.error("Insufficient balance.")
        else:
            user["balance"] -= amount
            save_data(data)
            st.success(f"Withdrawn {amount} successfully! New Balance: {user['balance']}")


elif choice == "View Details":
    st.subheader("View Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Get Details"):
        user = find_user(acc_no, int(pin) if pin.isdigit() else -1, data)
        if not user:
            st.error("Account not found or incorrect PIN.")
        else:
            st.json(user)


elif choice == "Update Details":
    st.subheader("Update Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Fetch Account"):
        st.session_state.user = find_user(acc_no, int(pin) if pin.isdigit() else -1, data)
        if not st.session_state.user:
            st.error("Account not found or incorrect PIN.")

    if "user" in st.session_state and st.session_state.user:
        user = st.session_state.user
        new_name = st.text_input("New Name", value=user["name"])
        new_email = st.text_input("New Email", value=user["email"])
        new_pin = st.text_input("New PIN (4 digits)", type="password", max_chars=4)

        if st.button("Update"):
            if new_name:
                user["name"] = new_name
            if new_email:
                user["email"] = new_email
            if new_pin.isdigit() and len(new_pin) == 4:
                user["pin"] = int(new_pin)
            save_data(data)
            st.success("Account updated successfully!")


elif choice == "Delete Account":
    st.subheader("Delete Account")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        user = find_user(acc_no, int(pin) if pin.isdigit() else -1, data)
        if not user:
            st.error("Account not found or incorrect PIN.")
        else:
            data.remove(user)
            save_data(data)
            st.success("Account deleted successfully!")
            
