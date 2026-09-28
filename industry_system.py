import json
import tkinter as tk
from tkinter import messagebox


# ============
# LOAD DATABASE
# =============

try:

    with open("companies.json", "r") as file:

        companies = json.load(file)

except FileNotFoundError:

    companies = {}



# ===========
# SAVE DATABASE
# =============

def save_database():

    with open("companies.json", "w") as file:

        json.dump(companies, file, indent=4)



# =========
# SEARCH COMPANY
# ==========

def search_company():

    company_name = entry_search.get()

    company_key = company_name.lower().replace(" ", "_")

    if company_key in companies:

        company = companies[company_key]

        result = f"""
Company Name: {company_name.title()}

Sector: {company['sector']}

Headquarters: {company['headquarters']}

Key Fact: {company['key_fact']}

Year Founded: {company['year_founded']}

CEO: {company['ceo']}

Industry Role: {company['industry_role']}
"""

        text_output.delete("1.0", tk.END)

        text_output.insert(tk.END, result)

    else:

        messagebox.showerror(
            "Error",
            "Company not found."
        )



# =========
# ADD COMPANY
# =======

def add_company():

    name = entry_name.get()

    sector = entry_sector.get()

    headquarters = entry_headquarters.get()

    key_fact = entry_key_fact.get()

    year_founded = entry_year.get()

    ceo = entry_ceo.get()

    industry_role = entry_role.get()

    company_key = name.lower().replace(" ", "_")

    companies[company_key] = {

        "sector": sector,

        "headquarters": headquarters,

        "key_fact": key_fact,

        "year_founded": year_founded,

        "ceo": ceo,

        "industry_role": industry_role
    }

    save_database()

    messagebox.showinfo(
        "Success",
        "Company added successfully."
    )



# =============
# LIST COMPANIES
# =============

def list_companies():

    text_output.delete("1.0", tk.END)

    text_output.insert(
        tk.END,
        "AVAILABLE COMPANIES\n\n"
    )

    for company in companies:

        formatted = company.replace(
            "_",
            " "
        ).title()

        text_output.insert(
            tk.END,
            f"- {formatted}\n"
        )



# ==========
# MAIN WINDOW
# ==========

window = tk.Tk()

window.title(
    "Petroleum Industry Management System"
)

window.geometry("700x700")



# ==============
# SEARCH SECTION
# =============

label_search = tk.Label(
    window,
    text="Search Company"
)

label_search.pack()

entry_search = tk.Entry(
    window,
    width=40
)

entry_search.pack()

button_search = tk.Button(
    window,
    text="Search",
    command=search_company
)

button_search.pack()



# ==================
# ADD COMPANY SECTION
# ==================

tk.Label(
    window,
    text="\nAdd New Company"
).pack()

entry_name = tk.Entry(window, width=40)
entry_name.pack()
entry_name.insert(0, "Company Name")

entry_sector = tk.Entry(window, width=40)
entry_sector.pack()
entry_sector.insert(0, "Sector")

entry_headquarters = tk.Entry(window, width=40)
entry_headquarters.pack()
entry_headquarters.insert(0, "Headquarters")

entry_key_fact = tk.Entry(window, width=40)
entry_key_fact.pack()
entry_key_fact.insert(0, "Key Fact")

entry_year = tk.Entry(window, width=40)
entry_year.pack()
entry_year.insert(0, "Year Founded")

entry_ceo = tk.Entry(window, width=40)
entry_ceo.pack()
entry_ceo.insert(0, "CEO")

entry_role = tk.Entry(window, width=40)
entry_role.pack()
entry_role.insert(0, "Industry Role")

button_add = tk.Button(
    window,
    text="Add Company",
    command=add_company
)

button_add.pack()



# ===========
# LIST BUTTON
# ===========

button_list = tk.Button(
    window,
    text="List Companies",
    command=list_companies
)

button_list.pack()



# ============
# OUTPUT AREA
# ===========

text_output = tk.Text(
    window,
    height=20,
    width=80
)

text_output.pack()


# =================
# START APPLICATION
# =================

window.mainloop()