import os
import streamlit as st

# Description: Configuration file for the app

# Airtable Information
airtable_api_key = st.secrets["airtable_api_key"]
airtable_routes_base_id = st.secrets["airtable_routes_base_id"]
airtable_routes_table_name = st.secrets["airtable_routes_table_name"]
airtable_locations_base_id = st.secrets["airtable_locations_base_id"]
airtable_locations_table_name = st.secrets["airtable_locations_table_name"]
airtable_menu_base_id = st.secrets["airtable_menu_base_id"]
airtable_menu_table_name = st.secrets["airtable_menu_table_name"]
airtable_test_base_id = st.secrets["airtable_test_base_id"]