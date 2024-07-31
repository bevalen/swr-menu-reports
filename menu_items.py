import config

# This file contains all four menus (Weeks one and two for both suppliers)
from airtable_api import fetch_airtable_records

base_id = config.airtable_menu_base_id
table_name = config.airtable_menu_table_name

menu_items = fetch_airtable_records(base_id, table_name)
# print("Here's your records!", menu_items)

# Create a dictionary to hold the menu items for each supplier
hanna_bros_menu = {
    "Week One": [],
    "Week Two": []
}

carlyles_menu = {
    "Week One": [],
    "Week Two": []
}

carlyles_menu_reports = {
    "Week One": {
        "Sunday": [],
        "Monday": [],
        "Wednesday": [],
    },
    "Week Two": {
        "Sunday": [],
        "Monday": [],
        "Wednesday": []
    }
}

# Process the retrieved menu items
for item in menu_items:
    # Get the supplier, week number, and report day
    supplier = item.get("Customer")
    week = item.get("Week")
    report_day = item.get("Report Day")
    # Append the item to the appropriate supplier's menu
    if supplier == "Hanna Bros.":
        hanna_bros_menu[week].append(item)
    elif supplier == "Carlyles":
        carlyles_menu[week].append(item)
        # Also append the item to the appropriate report day for Carlyles
        carlyles_menu_reports[week][report_day].append(item)

# Print carlyles menu reports for Monday only
print(carlyles_menu_reports["Week One"]["Sunday"])