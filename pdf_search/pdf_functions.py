import os
import requests
from bs4 import BeautifulSoup
import fitz  
import pytesseract
from PIL import Image
import io
import Levenshtein
import re
import database as db

DOWNLOAD_PATH = "downloaded_pdfs"

def extract_text_with_ocr(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        page_text = page.get_text()
        # Si la página no tiene texto (es una imagen/render), aplicamos OCR (Punto Extra)
        if not page_text.strip():
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            page_text = pytesseract.image_to_string(img, lang='spa') # Requiere tesseract instalado en el sistema
        text += page_text + "\n"
    doc.close()
    return text

def scrape_and_process(url_id, url_string):
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    
    try:
        response = requests.get(url_string, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pdf_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].lower().endswith('.pdf')]
        
        conn = db.get_db_connection()
        
        for link in pdf_links:
            # Manejar rutas relativas
            if not link.startswith('http'):
                link = url_string.rstrip('/') + '/' + link.lstrip('/')
                
            filename = link.split('/')[-1]
            filepath = os.path.join(DOWNLOAD_PATH, filename)
            
            # Descargar
            pdf_resp = requests.get(link, stream=True)
            with open(filepath, 'wb') as f:
                for chunk in pdf_resp.iter_content(8192):
                    f.write(chunk)
            
            # Extraer texto y procesar
            full_text = extract_text_with_ocr(filepath)
            word_count = len(full_text.split())
            
            # Buscar año con Regex (ej. 2024, 2025, 2026) en el texto o nombre
            year_match = re.search(r'(20\d{2})', filename)
            year = int(year_match.group(1)) if year_match else 2026 # Default o puedes buscar en el texto
            
            # Guardar en BD
            cursor = conn.execute('INSERT INTO documents (url_id, filename, year, word_count) VALUES (?, ?, ?, ?)', 
                                 (url_id, filename, year, word_count))
            doc_id = cursor.lastrowid
            
            # Dividir en bloques para Levenshtein
            chunk_length = 500 # Caracteres por bloque
            chunks = [full_text[i:i+chunk_length] for i in range(0, len(full_text), chunk_length)]
            for chunk in chunks:
                if chunk.strip():
                    conn.execute('INSERT INTO document_blocks (doc_id, text_block) VALUES (?, ?)', (doc_id, chunk))
        
        # Actualizar estatus
        conn.execute('UPDATE urls SET status = ? WHERE id = ?', ('scrappeada', url_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error en scrape_and_process: {e}")

def buscar_palabras(query, umbral):
    conn = db.get_db_connection()
    # Traemos los bloques y hacemos el JOIN para saber de qué archivo y URL vienen
    query_sql = '''
        SELECT b.text_block, d.filename, d.year, u.url
        FROM document_blocks b
        JOIN documents d ON b.doc_id = d.id
        JOIN urls u ON d.url_id = u.id
    '''
    blocks = conn.execute(query_sql).fetchall()
    conn.close()
    
    resultados = []
    query_lower = query.lower()
    
    for row in blocks:
        # Calcular ratio de Levenshtein
        ratio = Levenshtein.ratio(row['text_block'].lower(), query_lower)
        if ratio >= umbral:
            resultados.append({
                'block': row['text_block'],
                'filename': row['filename'],
                'year': row['year'],
                'url_origen': row['url'],
                'similitud': round(ratio * 100, 1) # Convertir a porcentaje
            })
            
    # Ordenar por mayor similitud
    return sorted(resultados, key=lambda x: x['similitud'], reverse=True)