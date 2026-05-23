import sqlite3
import os

DB_PATH = 'database/searcher.db'

def get_db_connection():
    # Asegura que la carpeta exista antes de conectar
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Tabla de URLs a scrapear
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'no escrapeada'
        )
    ''')
    # Tabla de Documentos
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            filename TEXT NOT NULL,
            year INTEGER,
            word_count INTEGER,
            FOREIGN KEY (url_id) REFERENCES urls (id)
        )
    ''')
    # Tabla de Bloques de Texto para búsqueda
    c.execute('''
        CREATE TABLE IF NOT EXISTS document_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            text_block TEXT NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents (id)
        )
    ''')
    conn.commit()
    conn.close()

# --- Funciones Auxiliares ---
def add_url(url):
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO urls (url) VALUES (?)', (url,))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        pass # La URL ya existe

def get_all_urls():
    conn = get_db_connection()
    urls = conn.execute('SELECT * FROM urls').fetchall()
    conn.close()
    return urls

def get_dashboard_stats():
    conn = get_db_connection()
    total_docs = conn.execute('SELECT COUNT(*) FROM documents').fetchone()[0]
    total_words = conn.execute('SELECT SUM(word_count) FROM documents').fetchone()[0] or 0
    docs_by_year = conn.execute('SELECT year, COUNT(*) as count FROM documents GROUP BY year ORDER BY year DESC').fetchall()
    conn.close()
    return total_docs, total_words, docs_by_year

def get_urls_with_documents():
    conn = get_db_connection()
    # Obtenemos URLs
    urls = conn.execute('SELECT * FROM urls').fetchall()
    
    # Obtenemos todos los documentos
    docs = conn.execute('SELECT id, url_id, filename FROM documents').fetchall()
    conn.close()
    
    # Armamos un diccionario para agrupar fácilmente en Jinja
    resultado = []
    for url in urls:
        url_dict = dict(url)
        # Filtramos los documentos que pertenecen a esta URL
        url_dict['documents'] = [d['filename'] for d in docs if d['url_id'] == url['id']]
        resultado.append(url_dict)
        
    return resultado