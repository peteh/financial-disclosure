import requests
import os
import zipfile
import xml.etree.ElementTree as ET
import logging
import pdfplumber

# Configure the logging settings
logging.basicConfig(level=logging.INFO)

DATA_DIR = "data"

data_year = 2024

def download_index(data_year):
  index_url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{data_year}FD.zip"
  r = requests.get(index_url, allow_redirects=True)
  storage_path = f"{DATA_DIR}/{data_year}"
  index_file_path = f"{storage_path}/{data_year}FD.zip"
  if not os.path.exists(storage_path):
      os.makedirs(storage_path)
  with open(index_file_path, 'wb') as fp:
      fp.write(r.content)

  with zipfile.ZipFile(index_file_path, 'r') as zip_ref:
      zip_ref.extractall(storage_path)

def download_reports(data_year):
  storage_path = f"{DATA_DIR}/{data_year}"
  index_xml_path = f"{storage_path}/{data_year}FD.xml"
  tree = ET.parse(index_xml_path)

  # Get the root element of the tree
  root = tree.getroot()

  # Iterate over each 'Member' element
  for member in root.findall('Member'):
    # Access and print each data field
    prefix = member.find('Prefix').text
    last = member.find('Last').text
    first = member.find('First').text
    suffix = member.find('Suffix').text
    filing_type = member.find('FilingType').text
    state_dst = member.find('StateDst').text
    year = member.find('Year').text
    filing_date = member.find('FilingDate').text
    doc_id = member.find('DocID').text

    # Print or process the data as needed
    print(f"Prefix: {prefix}, Last: {last}, First: {first}, Suffix: {suffix}, FilingType: {filing_type}, StateDst: {state_dst}, Year: {year}, FilingDate: {filing_date}, DocID: {doc_id}")
    download_report(data_year, doc_id)

def download_report(data_year, doc_id):
  report_url = f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{data_year}/{doc_id}.pdf"
  storage_path = f"{DATA_DIR}/{data_year}/reports"
  report_file_path = f"{storage_path}/{doc_id}.pdf"
  if os.path.exists(report_file_path):
    logging.info(f"{doc_id}.pdf already downloaded - skipping...")
    return False
  if not os.path.exists(storage_path):
    os.makedirs(storage_path)
  r = requests.get(report_url, allow_redirects=True)
  with open(report_file_path, 'wb') as fp:
    fp.write(r.content)

def process_report_plumber(data_year, doc_id):
  storage_path = f"{DATA_DIR}/{data_year}/reports"
  report_file_path = f"{storage_path}/{doc_id}.pdf"
  with pdfplumber.open(report_file_path) as pdf:
    # Select the first page (you can adjust the page number as needed)
    page = pdf.pages[0]

    # Extract the table data (adjust rect parameter as needed to fit the table area)
    table = page.extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"})

    # Assuming the first row contains headers, you can access them like this
    headers = table[0]
    logging.debug(headers)

    # Iterate through the table rows and extract the fields
    for row in table[1:]:
        id = row[0]
        owner = row[1]
        asset = row[2]
        transaction_type = row[3]
        date = row[4]
        notification_date = row[5]
        # ... (access other fields)

        # Print or process the extracted fields as needed
        logging.info(f"ID: {id}")
        logging.info(f"Owner: {owner}")
  
process_report_plumber("2024", "20023767")
#download_reports("2024")