import requests
import csv
import datetime
import os
from polygon import RESTClient

# Specific start and end dates for the data you want to fetch
date_start = "2023-07-19"
date_end = "2024-01-19"

# Polygon API URL for the specific range
api_key = "YOURKEY"
url = f"https://api.polygon.io/v2/aggs/ticker/C:EURUSD/range/1/minute/{date_start}/{date_end}?adjusted=true&sort=asc&limit=120&apiKey={api_key}"

# Make the API request
response = requests.get(url)

# Define the file saving location and name
save_location = r'drive:filelocation-for-saving'
filename = f"{date_start}_to_{date_end}_yourfilename.csv"
filepath = os.path.join(save_location, filename)

# Process the response
if response.status_code == 200:
    json_response = response.json()
    print("response: ", json_response)

    if "results" in json_response:
        data = json_response["results"]

        try:
            with open(filepath, "w", newline="") as csvfile:  # Use "w" to write a new file
                print(f"Saving data to file: {filepath}")
                writer = csv.writer(csvfile)#, delimiter=';'
                writer.writerow([
                        "timestamp",
                        "volume",
                        "volume_weighted",
                        "open",
                        "close",
                        "high",
                        "low",
                        "num_items"
                ])  # Write header
                for item in data:
                    writer.writerow([
                        item["t"],
                        item["v"],
                        item["vw"],
                        item["o"],
                        item["c"],
                        item["h"],
                        item["l"],
                        item["n"]
                    ])
        except Exception as e:
            print(f"An error occurred while saving: {e}")
    print(f"Data saved for {date_start} to {date_end} in {filename}")
else:
    print(f"API request failed with status code {response.status_code}")