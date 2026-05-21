from bs4 import BeautifulSoup
import os
from markitdown import MarkItDown
import requests
from sympy import content
import Levenshtein


class pdf_document:
    def __init__(self, url,pdf_path,markdown_path):
        self.url = url
        self.pdf_path = pdf_path
        self.markdown_path = markdown_path
        self.content = None
        self.convert_pdf_to_markdown()

    def convert_pdf_to_markdown(self):
        try:
            converter = MarkItDown()
            result = converter.convert(self.pdf_path)
            markwdown_content = result.markdown or result.text_content
            with open(self.markdown_path, 'w', encoding='utf-8') as f:
                f.write(markwdown_content)
            self.content = markwdown_content
        except Exception as e:
            print(f"Error converting PDF to Markdown: {e}")

def get_webpage(url):
    try:
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
        
def extract_pdf_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.lower().endswith('.pdf'):
            pdf_links.append(href)
    return pdf_links
    
def download_pdf(url, filename):
    try:
        response = requests.get(url, stream=True, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Check if the request was successful
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the PDF: {e}")

def get_pdfs(url = "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"):
        download_path = "pdfs"
        markdown_path = "markdown_files"
        if not os.path.exists(download_path):
            os.makedirs(download_path, exist_ok=True)  # Create the directory if it doesn't exist
        if not os.path.exists(markdown_path):
            os.makedirs(markdown_path, exist_ok=True)  # Create the directory if it doesn't exist
        html = get_webpage(url)
        if not html:
            print(f"Failed to retrieve the webpage: {url}")
            exit(1)
        pdf_links = extract_pdf_links(html)
        pdf_dict = {}
        for link in pdf_links:
            print(link)
            filename = link.split('/')[-1]  # Extract the filename from the URL
            downloaded_file = os.path.join(download_path, filename)
            download_pdf(link, downloaded_file)
            markdown_file = os.path.join(markdown_path, f"{os.path.splitext(filename)[0]}.md")
            pdf_doc = pdf_document(link, downloaded_file, markdown_file)
            pdf_dict [filename] = pdf_doc
            print(f"Downloaded: {filename}")
        return pdf_dict

def buscar_palabras_ratio(frases:list, frase_a_buscar:str, umbral:float=0.50)->list:
    """ Busca una frase en una lista de frases """
    frases_encontradas = []
    frase_a_buscar = frase_a_buscar.lower()
    for frase in frases:
        frase_lower = frase.frase.lower()
        ratio = Levenshtein.ratio(frase_lower, frase_a_buscar)
        if ratio >= umbral:
            frase.ratio = ratio
            frases_encontradas.append(frase)
    return frases_encontradas

def main():
    pdf_dictionary = get_pdfs()
    print(pdf_dictionary.keys())
    main_dictionary = {}
    for key, pdf_doc in pdf_dictionary.items():
        content = pdf_doc.content
        chunk_length = 20
        chunks = [content[i:i+chunk_length] for i in range (0, len(content), chunk_length)]  # Split the content into chunks based on the specified length and filter out empty chunks
        for chunk in chunks:
            if chunk not in main_dictionary:
                main_dictionary[chunk] = [key]
            else:
                main_dictionary[chunk].append(key)

if __name__ == "__main__":
    main()