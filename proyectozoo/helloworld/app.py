from flask import Flask, render_template, request
from Book import Book, load_books
from book_functions import create_author_dictionary, create_book_dictionary

app = Flask(__name__)

filename = 'C:\\Users\\emili\\OneDrive\\Desktop\\Curso_python ( no borrar )\\curso_python\\Books\\booklist2000.csv'
books = load_books(filename)
book_dict = create_book_dictionary(books)
author_dict = create_author_dictionary(books)

@app.route('/')
def index():   
    return render_template('index.html')

@app.route('/search_by_author', methods=['GET','POST'])
def search_by_author():
    if request.method == 'POST':
        author = request.form['author']
        books_list = author_dict.get(author.lower(), [])
        return render_template('search_by_author.html', books_list=books_list)
    else:
        return render_template('search_by_author.html', books_list=books[:10])
    
@app.route('/book/<string:book_id>')
def book_detail(book_id): 
    books = book_dict.get(book_id)
    print(books)
    return render_template('book_detail.html', book=books)
    

if __name__ == '__main__':
    app.run(debug=True)