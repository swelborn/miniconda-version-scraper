import requests
from bs4 import BeautifulSoup
import json

# URL of the Miniconda repo
url = "https://repo.anaconda.com/miniconda/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the response content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the rows in the table
rows = soup.find_all('tr')

# Initialize an empty dictionary to hold our mappings
mappings = {}

# Iterate over the rows
for row in rows:
    # Find all the cells in the row
    cells = row.find_all('td')
    # If there are at least 3 cells (we need name, last modified, and SHA256)...
    if len(cells) >= 3:
        # Get the name of the file
        name = cells[0].text
        # If the name indicates that this is a Miniconda installer...
        if "Linux" in name and "sh" in name and "latest" not in name and "py" in name:
            print(name)
            # Extract the platform from the name
            platform = name.split("-")[-1].split(".")[0]
            # Extract the Python version from the name
            py_version = name.split("py")[1].split("_")[0]
            # Get the SHA256 checksum from the third cell
            sha256 = cells[3].text
            # Create a nested dictionary entry if it doesn't exist
            if platform not in mappings:
                mappings[platform] = {}
            # Add the Python version, Miniconda version, and SHA256 checksum to our mappings
            if py_version not in mappings[platform]:
                mappings[platform][py_version] = (name, sha256)

# Print the mappings
print(json.dumps(mappings, indent=4))

# Optionally, write the mappings to a JSON file
with open('mappings.json', 'w') as f:
    json.dump(mappings, f, indent=4)

