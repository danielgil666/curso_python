"""book_functions.py
Contains functions to work with Book objects
"""

from Book import Book
from Book import load_books

def get_genres(book:list[Book])->list[str]:
    """Get a list of unique genres from a list of books."""
    genres = set()
    for b in book:
        genres.add(b.genre)
    return sorted(genres)
def create_author_dictionary(book:list[Book])->dict[str, list[Book]]:
    """Create a dictionary where the keys are authors and the values are lists of books by that author."""
    author_dict = {}
    for b in books:
        if b.author not in author_dict:
            author_dict[b.author.lower()] = []
        author_dict[b.author.lower()].append(b)
        author_names= b.author.lower().split(" ")
        if len(author_names) >= 2:
                for name in author_names:
                    if name not in author_dict:
                        author_dict[name] = []
                    author_dict[name].append(b)
           
    return author_dict

if __name__ == "__main__":
    books=load_books(r"C:\Users\Daniel Gil\Downloads\booklist2000.csv")
    print(get_genres(books))
    author_dict = create_author_dictionary(books)
    print(author_dict["sandra"][0])