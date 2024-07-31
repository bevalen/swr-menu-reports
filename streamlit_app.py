import pandas as pd
import date_change_function as dcf
import locations
import os
import streamlit as st

# Specify the full path of the downloads folder
downloads_folder = os.path.expanduser("~/Downloads/")

# Title of the app
st.title("Seventh Wave Refreshments")
st.subheader("Menu Reports Processor")
st.markdown("*Built by Ben Valentin (Ben@BenValentin.me)*")
st.markdown("---")

# Allow the user to upload their file
uploaded_file = st.file_uploader("Upload report", type=["xlsx"])

# Check if the user has clicked the button
if st.button("Process Data"):
    # Check if the user has uploaded a file
    if uploaded_file is None:
        st.write("Please upload a file to continue.")
        st.stop()

    st.write("Processing data...")
    
    print()
    print("Processing data...")
    print()

    # Load the Excel file
    df = pd.read_excel(uploaded_file, header=1)

    # Get a list of locations using the new_routes function
    locations = locations.get_locations()

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

    # Create a new column to store the route for each location with a default "Unknown Route"
    hanna_bros_sales.loc[:, 'Route'] = "Unknown Route"
    carlyles_sales.loc[:, 'Route'] = "Unknown Route"

    # Iterate through the locations to assign routes based on location
    for location in locations:
        # Extract necessary details from each location
        location_name = location['Location']
        route_name = location['Name (from Route)'][0]

        # Directly assign route names based on the 'Location' column match
        # Then adjust for special cases ("StateFarm" logic) within the same loop
        if "StateFarm" in location_name:
            # Special handling for "StateFarm" in route names
            hanna_bros_sales.loc[hanna_bros_sales['Location'] == location_name, 'Route'] = "Route 7"
            carlyles_sales.loc[carlyles_sales['Location'] == location_name, 'Route'] = "Route 3"
        else:
            # General case: Assign the route based on the location match
            hanna_bros_sales.loc[hanna_bros_sales['Location'] == location_name, 'Route'] = route_name
            carlyles_sales.loc[carlyles_sales['Location'] == location_name, 'Route'] = route_name

    # Create new dataframe of all the unique Product Names for each supplier
    hanna_bros_products = hanna_bros_sales['Product Name'].unique()
    carlyles_products = carlyles_sales['Product Name'].unique()

    # Createa  new dataframe for all the unique Locations separated by Route Name
    # Example: Route 1: [CKS 350, CKS 351, CKS 352]
    hanna_bros_locations = hanna_bros_sales.groupby('Route')['Location'].unique().reset_index()
    carlyles_locations = carlyles_sales.groupby('Route')['Location'].unique().reset_index()

    # Add a new column to store the total sales count
    hanna_bros_sales.loc[:, 'Total Sales'] = 0
    carlyles_sales.loc[:, 'Total Sales'] = 0

    # Create a new dataframe to store the total sales for each product per location
    # Example: Route 1, CKS 350, Dilly Bites, 02/19/24, Monday, 5
    hanna_bros_sales = hanna_bros_sales.groupby(['Route', 'Location', 'Product Name', 'Date', 'Day of Week']).size().reset_index(name='Total Sales')
    carlyles_sales = carlyles_sales.groupby(['Route', 'Location', 'Product Name', 'Date', 'Day of Week']).size().reset_index(name='Total Sales')

    # Download the hanna report
    # hanna_bros_sales.to_excel(os.path.join(downloads_folder, "hanna_bros_sales_TEST.xlsx"), index=False)

    # Create a new dataframe for specific reports for Carlyles
    # If the report is for a specific day, then filter the dataframe to only include the specific day
    # Report one is for Monday and Tuesday
    # Report two is for Tuesday and Wednesday (Duplicate of the Tuesday sales that also appear in report one)
    # Report three is for Thursday, Friday, Saturday, and Sunday
    # Create a new dataframe for the specific reports
    carlyles_report_sunday = carlyles_sales[carlyles_sales['Day of Week'].isin(['Monday', 'Tuesday', 'Wednesday'])].copy()
    carlyles_report_wednesday = carlyles_sales[carlyles_sales['Day of Week'].isin(['Thursday', 'Friday', 'Saturday', 'Sunday'])].copy()

    def save_reports_by_route_to_excel(sales_data, report_name, downloads_folder):
        # Get all unique product names across the entire dataset
        all_product_names = pd.unique(sales_data['Product Name'])
        
        # Create a summary pivot table for total sales by product name across all locations
        summary_pivot = sales_data.pivot_table(values='Total Sales', index='Product Name', aggfunc='sum', fill_value=0)
        
        # Ensure the summary pivot includes all product names
        summary_pivot = summary_pivot.reindex(all_product_names, fill_value=0)
        
        # Add a row for the total number of items at the end of the summary pivot
        summary_pivot.loc['Total Number of Items'] = summary_pivot.sum()
        
        filename = f"{report_name}.xlsx"
        full_path = os.path.join(downloads_folder, filename)
        
        with pd.ExcelWriter(full_path) as writer:
            # Save the summary pivot table as the first sheet
            summary_pivot.to_excel(writer, sheet_name='Total Sales Summary')
            
            # Get all unique routes
            unique_routes = sales_data['Route'].unique()
            
            for route in unique_routes:
                # Filter the data for the current route
                route_data = sales_data[sales_data['Route'] == route]
                
                # Create the pivot table for the current route
                pivot_df = route_data.pivot_table(values='Total Sales', index='Product Name', columns='Location', aggfunc='sum', fill_value=0)
                
                # Reindex the pivot table to include all product names, filling missing entries with 0
                pivot_df = pivot_df.reindex(all_product_names, fill_value=0)
                
                # Add a row for the total number of items at the end of the pivot table
                pivot_df.loc['Total Number of Items'] = pivot_df.sum()
                
                # Save the pivot table as a separate sheet named after the route
                # Ensure sheet name is within Excel's limit (31 characters)
                sheet_name = str(route)[:31]  # Convert route to string in case it's not, and ensure it's within Excel's limit
                pivot_df.to_excel(writer, sheet_name=sheet_name)

    # Download the reports with todays date in the filename
    # The date should be formatted as "MM-DD-YY"
    todays_date = dcf.get_todays_date()
    save_reports_by_route_to_excel(hanna_bros_sales, f"Hanna Bros. Sales {todays_date}", downloads_folder)
    save_reports_by_route_to_excel(carlyles_report_sunday, f"Carlyles Report Sunday {todays_date}", downloads_folder)
    save_reports_by_route_to_excel(carlyles_report_wednesday, f"Carlyles Report Wednesday {todays_date}", downloads_folder)


    print()
    print("Reports have been saved to the Downloads folder.")
    print()
    st.write("Reports have been saved to the Downloads folder.")