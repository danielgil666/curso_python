import requests
from bs4 import BeautifulSoup
import os

def get_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    
def  extract_pdf_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    pdf_link = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            pdf_link.append(href)
    return pdf_link

def download_pdf(url, filename):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        with open(filename, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the PDF: {e}")

if __name__ == "__main__":
    url = "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"
    html = get_webpage(url)
    if not html:
        print("Failed to retrieve the webpage.")
        exit(1)
    pdf_links = extract_pdf_links(html)
    for link in pdf_links:
        print(link)
        filename = link.split('/')[-1]  # Get the filename from the URL
        download_pdf(link, f"pdfs_{filename}")  # Save the PDF in the 'pdfs' directory
        print(f"Downloaded: {filename}")