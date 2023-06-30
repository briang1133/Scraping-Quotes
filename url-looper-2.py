import requests
from bs4 import BeautifulSoup
import csv
import re 

url = "https://www.getdbt.com/success-stories/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

# Find all elements with class "link-text-primary"
link_elements = soup.find_all(class_="link-text-primary")

# Prepare data list for CSV
data = []

# Loop through each link
for link in link_elements:
    href = 'https://www.getdbt.com'+link.get("href")
    
    # Send a GET request to the link URL
    link_response = requests.get(href)
    link_soup = BeautifulSoup(link_response.text, "html.parser")
    
    # Find the element with class "success-content col-lg-9"
    content_element = link_soup.find(class_="success-content col-lg-9")
    
    # Find all text within quotation marks
    #quotes = content_element.find_all(string=lambda t: isinstance(t, str) and '"' in t)
    quotes = re.findall(r'“([^”]*?,”[^”]*?\.|[^”]*?\.”)', content_element.get_text())
    
    # Store each quote as a separate record in the data list
    for quote in quotes:
        quote = quote.replace('\n', '')
        data.append((href, quote.strip()))

# Store data in a CSV file
filename = "scraped_data_2.csv"
with open(filename, "w", newline=None, encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Href", "Quote"])  # Write header
    writer.writerows(data)  # Write data rows

print(f"Data has been stored in '{filename}' successfully.")
