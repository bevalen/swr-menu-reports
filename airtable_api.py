import requests
import config

# Airtable API Key
api_key = config.airtable_api_key

def fetch_airtable_records(base_id, table_name):
    # Airtable API endpoint for the specified base and table
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    # Headers containing the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Send a GET request to fetch records
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Extract records from the response
        records = data.get("records", [])

        # List to store all records
        all_records = []

        # Process the retrieved records
        for record in records:
            fields = record.get("fields", {})
            # Append the fields to the list
            all_records.append(fields)

        # Return the list of all records
        return all_records

    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")