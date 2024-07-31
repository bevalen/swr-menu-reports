from airtable_api import fetch_airtable_records

base_id = "app7BSyVijivj6p83"
table_name = "Routes"

def get_routes():
    routes = fetch_airtable_records(base_id, table_name)
    # print("Here's your records!", routes)
    return routes

if __name__ == "__main__":
    raise RuntimeError("This script should not be executed directly. Please import it as a module.")