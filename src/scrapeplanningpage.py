import requests
from bs4 import BeautifulSoup
import os

def download_pdf(url, link_text, folder):
    # Step 1: Send a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {url}")
        return
    
    # Step 2: Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 3: Find all anchor tags that contain links
    links = soup.find_all('a', href=True)
    
    # Step 4: Check each link to see if it contains the target text and points to a PDF
    for link in links:
        if link_text.lower() in link.get_text().lower() and link['href'].endswith('.pdf'):
            pdf_url = link['href']
            if not pdf_url.startswith('http'):
                # If the PDF link is relative, make it absolute
                pdf_url = os.path.join(url, pdf_url)
            

            # Step 5: Download the PDF
            print(f"Downloading PDF from {pdf_url}...")
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                pdf_filename = pdf_url.split('/')[-1]
                dest = os.path.join(folder, pdf_filename)
                print(f'Downloading to {dest}')
                with open( dest , 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"Downloaded PDF: {pdf_filename}")
            else:
                print(f"Failed to download the PDF: {pdf_url}")
            return
    print(f"No link found containing text '{link_text}' that points to a PDF.")

# Example usage
webpage_url = 'https://longmontcolorado.gov/planning-and-development-services/plans-and-reports/active-development-log-and-map/' 
text_to_search_for = 'Active Development Log'  
download_pdf(webpage_url, text_to_search_for, '.\\data')


