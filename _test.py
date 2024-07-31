import pandas as pd
import date_change_function as dcf
import locations
import os

print()
print("Processing data...")
print()

# Specify the full path of the downloads folder
downloads_folder = os.path.expanduser("~/Downloads/")

# Load the Excel file
df = pd.read_excel('sales.xlsx', header=1)

# Get a list of locations using the new_routes function
locations = locations.get_locations()

# Example output:
# {'Route': ['reczppzP1HAp6H7E7'], 'Location': 'CKS 350', 'Driver (from Route)': ['Roger'], 'Name (from Route)': ['Route 1']}

# Filter the rows into two separate dataframes. One for the "Hanna Bros." supplier and one for the "Carlyles" supplier
# The can be found by checking the "Product Name" column for the supplier's name
hanna_bros_sales = df[df['Product Name'].str.contains("Hanna Bros.")].copy()
carlyles_sales = df[df['Product Name'].str.contains("Carlyles")].copy()

# Convert the date into a day of the week and add it as a new column
hanna_bros_sales.loc[:, 'Day of Week'] = hanna_bros_sales['Date'].apply(dcf.get_day_of_week)
carlyles_sales.loc[:, 'Day of Week'] = carlyles_sales['Date'].apply(dcf.get_day_of_week)

# Add new column with suppliers name
hanna_bros_sales.loc[:, 'Supplier'] = "Hanna Bros."
carlyles_sales.loc[:, 'Supplier'] = "Carlyles"

# Remove all columns except for "Product Name", "Day of Week", "Date" and "Location"
hanna_bros_sales = hanna_bros_sales[["Product Name", "Day of Week", "Date", "Location", "Supplier"]]
carlyles_sales = carlyles_sales[["Product Name", "Day of Week", "Date", "Location", "Supplier"]]

# Remove the suppliers name from each product name, and be sure to trim the whitespace
hanna_bros_sales['Product Name'] = hanna_bros_sales['Product Name'].str.replace("Hanna Bros.", "").str.strip()
carlyles_sales['Product Name'] = carlyles_sales['Product Name'].str.replace("Carlyles", "").str.strip()