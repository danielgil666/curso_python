""" book_functions.py
    Contains functions to work with Book objects
"""
from Book import Book

def get_genres(books: list[Book]) -> list[str]:
    """Get all unique genres from a list of Book objects"""
    genres = set()
    for book in books:
        genres.add(book.genre)
    return sorted(list(genres))

def create_author_dictionary(books: list[Book]) -> dict[str, list[Book]]:
    """Create a dictionary of authors and their books"""
    author_dict = {}
    for book in books:
        # Guardar por nombre completo (en minúsculas)
        full_name = book.author.lower().strip()
        if full_name not in author_dict:
            author_dict[full_name] = []
        author_dict[full_name].append(book)
        
        # Guardar por nombres individuales para búsquedas parciales
        author_names = full_name.split(" ")
        if len(author_names) >= 2:
            for name in author_names:   
                if len(name) > 2: # Evitar conectores cortos como "de"
                    if name not in author_dict:
                        author_dict[name] = []
                    if book not in author_dict[name]:
                        author_dict[name].append(book)
    return author_dict

def create_book_dictionary(book_list: list) -> dict[str, Book]:
    """Create a dictionary of books and their ids"""
    book_dict = {}
    for book in book_list:
        book_dict[str(book.id)] = book
    return book_dict