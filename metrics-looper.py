import requests
from bs4 import BeautifulSoup
import csv
import re 
import urllib.parse
from urllib.parse import urlparse

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

    # Parse the URL
    parsed_url = urlparse(href)

    # Get the path segment
    path = parsed_url.path

    # Remove the leading slash and trailing slash (if present)
    path = path.strip('/')

    # Split the path into segments
    segments = path.split('/')

    # Find the desired segment containing "cond%C3%A9-nast"
    last_segment = segments[-1]

    # Find and replace special characters
    decoded_segment = urllib.parse.unquote(last_segment)
    decoded_segment = decoded_segment.replace('-',' ')
    decoded_segment = decoded_segment.title()

    # Send a GET request to the link URL
    link_response = requests.get(href)
    link_soup = BeautifulSoup(link_response.text, "html.parser")
    
    # Find the element with class "result text-center col""
    metric_containers = link_soup.find_all(class_="result text-center col")
    
    # Store each metric, result_label, and result_desc element as a separate record in the data list
    for element in metric_containers:
        metric = element.find(class_='metric').get_text(strip=True)
        result_label = element.find(class_='result-label').get_text(strip=True)
        result_desc = element.find(class_='result-desc').get_text(strip=True)
        data.append((decoded_segment, metric + ' ' + result_label + ' ' + result_desc, href))

# Store data in a CSV file
filename = "scraped_metrics.csv"
with open(filename, "w", newline=None, encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Case Study", "Metric", "URL"])  # Write header
    writer.writerows(data)  # Write data rows

print(f"Data has been stored in '{filename}' successfully.")
