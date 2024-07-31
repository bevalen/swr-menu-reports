from airtable_api import fetch_airtable_records
import config

base_id = config.airtable_locations_base_id
table_name = config.airtable_locations_table_name

def get_locations():
    locations = fetch_airtable_records(base_id, table_name)
    # print("Here's your records!", locations)
    return locations

if __name__ == "__main__":
    raise RuntimeError("This script should not be executed directly. Please import it as a module.")