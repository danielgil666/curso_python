import os
import requests
from bs4 import BeautifulSoup
import fitz  
import pytesseract
from PIL import Image
import io
import Levenshtein
import re
import urllib3 # Importación nueva para silenciar advertencias SSL
import database as db

# Silenciar las advertencias de seguridad al usar verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOWNLOAD_PATH = "downloaded_pdfs"

def extract_text_with_ocr(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        page_text = page.get_text()
        if not page_text.strip():
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            page_text = pytesseract.image_to_string(img, lang='spa')
        text += page_text + "\n"
    doc.close()
    return text

def scrape_and_process(url_id, url_string):
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    
    try:
        # Agregamos verify=False para evitar problemas de certificados SSL
        response = requests.get(url_string, timeout=15, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pdf_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].lower().endswith('.pdf')]
        
        conn = db.get_db_connection()
        
        for link in pdf_links:
            if not link.startswith('http'):
                link = url_string.rstrip('/') + '/' + link.lstrip('/')
                
            filename = link.split('/')[-1]
            filepath = os.path.join(DOWNLOAD_PATH, filename)
            
            # También agregamos verify=False aquí en la descarga del archivo
            pdf_resp = requests.get(link, stream=True, verify=False)
            with open(filepath, 'wb') as f:
                for chunk in pdf_resp.iter_content(8192):
                    f.write(chunk)
            
            full_text = extract_text_with_ocr(filepath)
            word_count = len(full_text.split())
            
            year_match = re.search(r'(20\d{2})', filename)
            year = int(year_match.group(1)) if year_match else 2026 
            
            cursor = conn.execute('INSERT INTO documents (url_id, filename, year, word_count) VALUES (?, ?, ?, ?)', 
                                 (url_id, filename, year, word_count))
            doc_id = cursor.lastrowid
            
            chunk_length = 500 
            chunks = [full_text[i:i+chunk_length] for i in range(0, len(full_text), chunk_length)]
            for chunk in chunks:
                if chunk.strip():
                    conn.execute('INSERT INTO document_blocks (doc_id, text_block) VALUES (?, ?)', (doc_id, chunk))
        
        conn.execute('UPDATE urls SET status = ? WHERE id = ?', ('scrappeada', url_id))
        conn.commit()
        conn.close()
    except Exception as e:
        # Ahora el error se imprimirá más claro si vuelve a fallar
        print(f"Error procesando {url_string}: {e}")

def buscar_palabras(query, umbral):
    conn = db.get_db_connection()
    query_sql = '''
        SELECT b.text_block, d.filename, d.year, u.url
        FROM document_blocks b
        JOIN documents d ON b.doc_id = d.id
        JOIN urls u ON d.url_id = u.id
    '''
    blocks = conn.execute(query_sql).fetchall()
    conn.close()
    
    resultados = []
    # Limpiamos espacios extra en la búsqueda
    query_lower = query.lower().strip()
    query_words = query_lower.split()
    n_words = len(query_words)
    
    if n_words == 0:
        return []
        
    for row in blocks:
        text_block = row['text_block']
        block_lower = text_block.lower()
        block_words = block_lower.split()
        
        mejor_ratio = 0.0
        
        # VENTANA MÓVIL: Compara fragmentos del texto del mismo tamaño que la búsqueda
        if len(block_words) >= n_words:
            for i in range(len(block_words) - n_words + 1):
                # Armamos un fragmento de palabras 
                ventana = " ".join(block_words[i:i+n_words])
                ratio = Levenshtein.ratio(ventana, query_lower)
                
                # Guardamos el mejor puntaje encontrado en este bloque
                if ratio > mejor_ratio:
                    mejor_ratio = ratio
        elif len(block_words) > 0:
            # Caso raro: si el bloque es más corto que la búsqueda
            mejor_ratio = Levenshtein.ratio(block_lower, query_lower)
            
        # En lugar de usar round(mejor_ratio * 100, 3)
        porcentaje = mejor_ratio * 100
        
        # Formateo estricto a máximo 3 dígitos
        if porcentaje == 100.0:
            similitud_str = "100"
        else:
            similitud_str = f"{porcentaje:.1f}" # Ejemplo: 95.5
            
        if mejor_ratio >= umbral:
            clean_block = text_block.replace('\n', ' ').strip()
            
            resultados.append({
                'block': clean_block,
                'filename': row['filename'],
                'year': row['year'],
                'url_origen': row['url'],
                'similitud': similitud_str # Usamos el string formateado
            })
            
    # Ordenar desde el más similar (100%) hacia abajo
    return sorted(resultados, key=lambda x: x['similitud'], reverse=True)