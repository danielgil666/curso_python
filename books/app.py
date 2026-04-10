from flask import Flask, render_template, request
from Book import load_books 
from book_functions import create_author_dictionary, create_book_dictionary
import os

app = Flask(__name__)

# Configuración de ruta automática
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(BASE_DIR, 'booklist2000.csv')
print(f"Archivo de libros: {filename}")
# Carga inicial de datos
print("--- Iniciando sistema ---")
all_books = load_books(filename)
author_dict = create_author_dictionary(all_books)
book_dict = create_book_dictionary(all_books)

print(f"Carga completa: {len(all_books)} libros listos.")
print(f"Diccionario de autores: {len(author_dict)} entradas.")

@app.route('/')
def index():
    return render_template('new_index.html')

@app.route('/search_by_author', methods=['GET', 'POST'])
def search_by_author():
    if request.method == 'POST':
        author_query = request.form.get('author', '').lower().strip()
        # Búsqueda en el diccionario de autores
        results = author_dict.get(author_query, [])
        print(f"Búsqueda: '{author_query}' - Encontrados: {len(results)}")
        return render_template('search_by_author.html', books_list=results, query=author_query)
    
    # Si es GET, muestra los primeros 10 libros
    return render_template('search_by_author.html', books_list=all_books[:10])

@app.route('/search_by_title', methods=['GET', 'POST'])
def search_by_title():
    if request.method == 'POST':
        title_query = request.form.get('title', '').lower().strip()
        
        # Filtramos la lista de libros buscando coincidencias en el título
        # Esto encontrará libros que contengan la palabra buscada
        results = [book for book in all_books if title_query in book.title.lower()]
        
        print(f"Búsqueda por título: '{title_query}' - Encontrados: {len(results)}")
        return render_template('search_by_title.html', books_list=results, query=title_query)
    
    # Si es GET (al entrar por primera vez), puedes mostrar los primeros 10 o ninguno
    return render_template('search_by_title.html', books_list=all_books[:10])

@app.route('/book/<book_id>')
def book_detail(book_id):
    book = book_dict.get(str(book_id))
    return render_template('book_detail.html', book=book)
 
if __name__ == '__main__':
    app.run(debug=True)