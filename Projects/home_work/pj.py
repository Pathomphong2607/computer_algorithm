import customtkinter as ctk
import csv
from datetime import datetime

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

transactions = []

# ------------------------
# FILE SYSTEM
# ------------------------

def load_from_file():
    transactions.clear()
    try:
        with open("transactions.csv","r",encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append({
                    "type": row["type"],
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "date": row["date"]
                })
    except FileNotFoundError:
        pass


def save_to_file():
    with open("transactions.csv","w",newline="",encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=["type","amount","category","date"])
        writer.writeheader()
        writer.writerows(transactions)

# ------------------------
# ADD TRANSACTION
# ------------------------

def add_transaction(t_type):

    amount = amount_entry.get()
    category = category_entry.get()

    if amount == "" or category == "":
        return

    transactions.append({
        "type": t_type,
        "amount": float(amount),
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    save_to_file()
    refresh_table()

    amount_entry.delete(0,"end")
    category_entry.delete(0,"end")

# ------------------------
# SUMMARY PERIOD
# ------------------------

def summary_period(period):

    now = datetime.now()

    income = 0
    expense = 0
    category_total = {}

    for t in transactions:

        t_date = datetime.strptime(t["date"],"%Y-%m-%d")

        match = False

        if period == "day":
            match = t_date.date() == now.date()

        elif period == "week":
            match = t_date.isocalendar()[1] == now.isocalendar()[1] and t_date.year == now.year

        elif period == "month":
            match = t_date.month == now.month and t_date.year == now.year

        if match:

            if t["type"] == "income":
                income += t["amount"]

            elif t["type"] == "expense":

                expense += t["amount"]

                cat = t["category"]

                if cat not in category_total:
                    category_total[cat] = 0

                category_total[cat] += t["amount"]

    result = f"\nIncome : {int(income)}"
    result += f"\nExpense : {int(expense)}"
    result += f"\nBalance : {int(income-expense)}\n"

    if category_total:

        max_value = max(category_total.values())

        max_categories = [c for c,v in category_total.items() if v == max_value]

        result += "\nMost Expense Category\n"

        for c in max_categories:
            result += f"{c} = {int(max_value)}\n"

    result_box.delete("1.0","end")
    result_box.insert("end",result)

# ------------------------
# SHOW ALL
# ------------------------

def show_all_transactions():

    result_box.delete("1.0","end")

    for t in transactions:

        line = f'{t["date"]} | {t["type"]} | {t["category"]} | {int(t["amount"])}\n'

        result_box.insert("end",line)

# ------------------------
# MONTH WITH MAX EXPENSE
# ------------------------

def max_expense_month():

    month_total = {}

    for t in transactions:

        if t["type"] == "expense":

            date = datetime.strptime(t["date"],"%Y-%m-%d")

            key = date.strftime("%Y-%m")

            if key not in month_total:
                month_total[key] = 0

            month_total[key] += t["amount"]

    if not month_total:
        return

    max_value = max(month_total.values())

    max_months = [m for m,v in month_total.items() if v == max_value]

    result_box.delete("1.0","end")

    result_box.insert("end","Month with highest expense\n")

    for m in max_months:
        result_box.insert("end",f"{m} = {int(max_value)}\n")

# ------------------------
# SUMMARY TOTAL
# ------------------------

def calculate_summary():

    income = 0
    expense = 0

    for t in transactions:

        if t["type"] == "income":
            income += t["amount"]

        elif t["type"] == "expense":
            expense += t["amount"]

    balance = income - expense

    income_label.configure(text=f"Income : {int(income)}")
    expense_label.configure(text=f"Expense : {int(expense)}")
    balance_label.configure(text=f"Balance : {int(balance)}")

# ------------------------
# REFRESH TABLE
# ------------------------

def refresh_table():

    load_from_file()

    for row in table_frame.winfo_children():
        row.destroy()

    for t in transactions:

        text = f'{t["date"]} | {t["type"]} | {t["category"]} | {int(t["amount"])}'

        label = ctk.CTkLabel(table_frame,text=text,anchor="w")
        label.pack(fill="x",padx=5,pady=2)

    calculate_summary()

# ------------------------
# UI
# ------------------------

app = ctk.CTk()
app.geometry("750x650")
app.title("รายรับ-รายจ่าย")

title = ctk.CTkLabel(app,text="รายรับ-รายจ่าย",font=("Arial",26))
title.pack(pady=15)

# Input

amount_entry = ctk.CTkEntry(app,placeholder_text="Amount")
amount_entry.pack(pady=5)

category_entry = ctk.CTkEntry(app,placeholder_text="Category")
category_entry.pack(pady=5)

# Buttons

btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame,text="Add Income",
command=lambda:add_transaction("income")).pack(side="left",padx=10)

ctk.CTkButton(btn_frame,text="Add Expense",
command=lambda:add_transaction("expense")).pack(side="left",padx=10)

# Summary

summary_frame = ctk.CTkFrame(app)
summary_frame.pack(pady=10)

income_label = ctk.CTkLabel(summary_frame,text="Income : 0")
income_label.pack()

expense_label = ctk.CTkLabel(summary_frame,text="Expense : 0")
expense_label.pack()

balance_label = ctk.CTkLabel(summary_frame,text="Balance : 0")
balance_label.pack()

# Menu

menu_frame = ctk.CTkFrame(app)
menu_frame.pack(pady=10)

ctk.CTkButton(menu_frame,text="Summary Day",
command=lambda:summary_period("day")).pack(side="left",padx=5)

ctk.CTkButton(menu_frame,text="Summary Week",
command=lambda:summary_period("week")).pack(side="left",padx=5)

ctk.CTkButton(menu_frame,text="Summary Month",
command=lambda:summary_period("month")).pack(side="left",padx=5)

ctk.CTkButton(menu_frame,text="Show All",
command=show_all_transactions).pack(side="left",padx=5)

ctk.CTkButton(menu_frame,text="Max Expense Month",
command=max_expense_month).pack(side="left",padx=5)

# Table

table_frame = ctk.CTkScrollableFrame(app,width=600,height=200)
table_frame.pack(pady=10)

# Result

result_box = ctk.CTkTextbox(app,width=600,height=120)
result_box.pack(pady=10)

# Credit Name (ชื่อด้านล่าง)

credit_label = ctk.CTkLabel(
    app,
    text="Developed by Pathomphong Phuengprakhon",
    font=("Arial",13),
    text_color="gray"
)
credit_label.pack(pady=10)

refresh_table()

app.mainloop()